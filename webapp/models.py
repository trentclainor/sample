# -*- coding: utf-8 -*-
import string
import random
from datetime import datetime
from sqlalchemy import Column, Integer, TIMESTAMP, Enum, String, Text, DateTime, \
    Boolean, Sequence, Index, Date, ForeignKey
from sqlalchemy.ext.associationproxy import association_proxy
from werkzeug.security import generate_password_hash, check_password_hash
# from webapp.extensions.db import Model
from flask import abort
from flask.ext.login import UserMixin, AnonymousUserMixin
from flask.ext.babel import gettext as _
from .extensions import db
from .helpers import generate_random
from . import dictionary
from . import exception

ROLES = set(k[0] for k in dictionary.ROLES)
STATUSES = set(k[0] for k in dictionary.STATUSES)
CONVERSATION_STATUSES = set(k[0] for k in dictionary.CONVERSATION_STATUSES)
CLICK_STATUSES = set(k[0] for k in dictionary.CLICK_STATUSES)
STATUSES_BLOCKED = set(k[0] for k in dictionary.STATUSES_BLOCKED)
STATUSES_DELETED = set(k[0] for k in dictionary.STATUSES_DELETED)
SECTION_TYPES = set(k[0] for k in dictionary.SECTION_TYPES)
CHANNEL_TYPES = set(k[0] for k in dictionary.CHANNEL_TYPES)
COST_TYPES = set(k[0] for k in dictionary.COST_TYPES)
MODERATION = set(k[0] for k in dictionary.MODERATION)


class FakeDeleteMixin(object):

    def delete(self, commit=True):
        self.status = 'deleted'
        return commit and db.session.commit()

    def is_deleted(self):
        return self.status == 'deleted'


class ModelMixin(object):
    __table_args__ = {'mysql_charset': 'utf8', 'mysql_engine': 'InnoDB'}
    __mapper_args__ = {'always_refresh': True}

    id = Column(Integer(), primary_key=True)

    def get_id(self):
        return self.id

    def is_active(self):
        return self.status == 'active'

    def is_blocked(self):
        return self.status == 'blocked'

    @classmethod
    def get(cls, id):
        if any((isinstance(id, basestring) and id.isdigit(), isinstance(id, (int, float))),):
            return cls.query.get(int(id))
        return None

    @classmethod
    def get_or_404(cls, id):
        if any((isinstance(id, basestring) and id.isdigit(), isinstance(id, (int, float))),):
            return cls.query.get_or_404(int(id))
        return abort(404)

    def update(self, commit=True, **kwargs):
        for attr, value in kwargs.iteritems():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def block(self, commit=True):
        self.status = 'blocked'
        return commit and db.session.commit()

    def activate(self, commit=True):
        self.status = 'active'
        return commit and db.session.commit()

    def delete(self, commit=True):
        db.session.delete(self)
        return commit and db.session.commit()


class Feedback(ModelMixin, db.Model):
    __tablename__ = 'feedbacks'

    user_id = Column(Integer, default=0, nullable=False)
    name = Column(String(255), default='', nullable=False)
    mail = Column(String(255), default='', nullable=False)
    text = Column(Text(), default='', nullable=False)
    status = Column(Enum(*STATUSES, name='status'), default='active', nullable=False)
    updated = Column(TIMESTAMP, default=datetime.now, nullable=False)
    created = Column(TIMESTAMP, default=datetime.now, nullable=False)

    def __unicode__(self):
        return "%s, %s" % (self.name, self.mail)


class ScenarioSection(db.Model):
    __tablename__ = 'scenario_sections'

    scenario_id = Column(Integer(), ForeignKey('scenarios.id'), primary_key=True)
    section_id = Column(Integer(), ForeignKey('sections.id'), primary_key=True)
    count = Column(Integer(), default=0, nullable=False)

    scenario = db.relationship("Scenario",
                               backref=db.backref("scenario_sections", cascade="all, delete-orphan"),
                               order_by="Scenario.name")
    section = db.relationship("Section",
                              backref=db.backref("scenario_sections", cascade="all, delete-orphan"),
                              order_by="Section.name")

    def __init__(self, section=None, scenario=None, count=None):
        self.section = section
        self.scenario = scenario
        self.count = count


class Link(db.Model):
    __tablename__ = 'links'

    scenario_id = Column(Integer(), ForeignKey('scenarios.id',
                                               onupdate="cascade", ondelete='restrict'), primary_key=True)
    channel_id = Column(Integer(), ForeignKey('channels.id',
                                              onupdate="cascade", ondelete='restrict'), primary_key=True)
    alias = Column(String(32), default=None, nullable=True, unique=True)
    url = Column(Text(), default='', nullable=False)
    status = Column(Enum(*STATUSES_DELETED, name='status'), default='active', nullable=False)
    updated = Column(TIMESTAMP, default=datetime.now, nullable=False)
    created = Column(TIMESTAMP, default=datetime.now, nullable=False)

    scenario = db.relationship("Scenario",
                               backref=db.backref("links", cascade="all, delete-orphan"),
                               order_by="Scenario.name")
    channel = db.relationship("Channel",
                              backref=db.backref("links", cascade="all, delete-orphan"),
                              order_by="Channel.name")

    def __init__(self, channel=None, scenario=None):
        self.channel = channel
        self.scenario = scenario
        self.alias = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32))


class Section(FakeDeleteMixin, ModelMixin, db.Model):
    __tablename__ = 'sections'
    __table_args__ = (
         db.UniqueConstraint("client_id", "alias"),
    )
    per_page = 20

    id = Column(Integer(), primary_key=True)
    client_id = Column(Integer(), ForeignKey('users.id', onupdate="cascade", ondelete='restrict'))
    order = Column(Integer(), default=0, nullable=False)
    name = Column(String(255), nullable=False)
    alias = Column(String(255), nullable=False)
    section_type = Column(Enum(*SECTION_TYPES, name='section_type'), nullable=True)
    wildcard = Column(String(255), nullable=True)
    hits = Column(Integer, default=0, nullable=False)
    status = Column(Enum(*STATUSES_DELETED, name='status'), default='active', nullable=False)
    updated = Column(DateTime, default=datetime.now)
    created = Column(DateTime, default=datetime.now)

    client = db.relationship('User', back_populates="sections")

    scenarios = association_proxy('scenario_sections', 'scenario')

    def __unicode__(self):
        return "%s" % self.name


class ReportScenarioChannel(db.Model):
    __tablename__ = 'report_scenario_channels'
    __table_args__ = {'mysql_charset': 'utf8', 'mysql_engine': 'InnoDB'}
    per_page = 100

    scenario_id = Column(Integer(), ForeignKey('scenarios.id', onupdate="no action", ondelete='restrict'),
                         autoincrement=False, primary_key=True)
    channel_id = Column(Integer(), ForeignKey('channels.id', onupdate="cascade", ondelete='restrict'),
                        autoincrement=False, primary_key=True)
    clicks = Column(Integer, default=0, nullable=False)
    convs = Column(Integer, default=0, nullable=False)
    cost = Column(Integer, default=0, nullable=False)
    payout = Column(Integer, default=0, nullable=False)
    day = Column(Date, primary_key=True)

    def __unicode__(self):
        return "%s" % self.day


class ReportScenario(db.Model):
    __tablename__ = 'report_scenarios'
    __table_args__ = {'mysql_charset': 'utf8', 'mysql_engine': 'InnoDB'}
    per_page = 100

    scenario_id = Column(Integer(), ForeignKey('scenarios.id', onupdate="no action", ondelete='restrict'),
                         autoincrement=False, primary_key=True)
    clicks = Column(Integer, default=0, nullable=False)
    convs = Column(Integer, default=0, nullable=False)
    cost = Column(Integer, default=0, nullable=False)
    payout = Column(Integer, default=0, nullable=False)
    day = Column(Date, primary_key=True)

    def __unicode__(self):
        return "%s" % self.day


class ReportChannel(db.Model):
    __tablename__ = 'report_channels'
    __table_args__ = {'mysql_charset': 'utf8', 'mysql_engine': 'InnoDB'}
    per_page = 100

    channel_id = Column(Integer(), ForeignKey('channels.id', onupdate="cascade", ondelete='restrict'),
                        autoincrement=False, primary_key=True)
    clicks = Column(Integer, default=0, nullable=False)
    convs = Column(Integer, default=0, nullable=False)
    cost = Column(Integer, default=0, nullable=False)
    payout = Column(Integer, default=0, nullable=False)
    day = Column(Date, primary_key=True)

    def __unicode__(self):
        return "%s" % self.day


class Scenario(FakeDeleteMixin, ModelMixin, db.Model):
    __tablename__ = 'scenarios'
    per_page = 100

    id = Column(Integer(), primary_key=True)
    client_id = Column(Integer(), ForeignKey('users.id', onupdate="cascade", ondelete='restrict'))
    name = Column(String(255), nullable=False)
    cost_type = Column(Enum(*COST_TYPES, name="cost_type"), nullable=True)
    price = Column(Integer, default=0, nullable=False)
    moderation = Column(Enum(*MODERATION, name="moderation"), nullable=False)
    total_count = Column(Integer, default=0, nullable=False)
    count_unique = Column(Boolean, default=0, nullable=False)
    clicks = Column(Integer, default=0, nullable=False)
    convs = Column(Integer, default=0, nullable=False)
    cost = Column(Integer, default=0, nullable=False)
    status = Column(Enum(*STATUSES, name='status'), default='active', nullable=False)
    updated = Column(TIMESTAMP, default=datetime.now, nullable=False)
    created = Column(TIMESTAMP, default=datetime.now, nullable=False)

    client = db.relationship('User', back_populates="scenarios")

    sections = association_proxy('scenario_sections', 'section')
    links = association_proxy('links', 'channel')

    section_cnt = db.column_property(
        db.select([db.func.count(ScenarioSection.section_id)])
        .where(ScenarioSection.scenario_id == id)
        .correlate_except(ScenarioSection))
    channel_cnt = db.column_property(
        db.select([db.func.count(Link.channel_id)])
        .where(Link.scenario_id == id)
        .correlate_except(Link))

    def get_price(self):
        return "%0.2f" % (self.price / 100.0)

    def get_cost_type(self):
        return dict(dictionary.COST_TYPES)[self.cost_type]

    def get_moderation(self):
        return dict(dictionary.MODERATION)[self.moderation]

    def __unicode__(self):
        return "%s" % self.name


class Channel(FakeDeleteMixin, ModelMixin, db.Model):
    __tablename__ = 'channels'
    per_page = 100

    id = Column(Integer(), primary_key=True)
    partner_id = Column(Integer(), ForeignKey('users.id', onupdate="cascade", ondelete='restrict'))
    name = Column(String(255), nullable=False, unique=True)
    channel_type = Column(Enum(*CHANNEL_TYPES, name="channel_type"), nullable=True)
    url = Column(Text(), nullable=False)
    price = Column(Integer, nullable=False)
    clicks = Column(Integer, nullable=False)
    convs = Column(Integer, nullable=False)
    status = Column(Enum(*STATUSES, name='status'), default='active', nullable=False)
    updated = Column(DateTime, default=datetime.now)
    created = Column(DateTime, default=datetime.now)

    partner = db.relationship('User', back_populates="channels", order_by="User.name")

    scenarios = association_proxy('links', 'scenario')

    def get_price(self):
        return "%0.2f" % (self.price / 100.0)

    def get_channel_type(self):
        return dict(dictionary.CHANNEL_TYPES)[self.channel_type]

    def __unicode__(self):
        return "%s" % self.name


class ChannelCustomPayout(db.Model):
    __tablename__ = 'channel_custom_payouts'
    per_page = 100

    channel_id = Column(Integer(), ForeignKey('channels.id', onupdate="cascade", ondelete='restrict'),
                        primary_key=True)
    day = Column(Date, primary_key=True)
    amount = Column(Integer, nullable=False)
    description = Column(String(255), nullable=False)
    updated = Column(DateTime, default=datetime.now)
    created = Column(DateTime, default=datetime.now)

    channel = db.relationship('Channel')

    def get_amount(self):
        return "%0.2f" % (self.amount / 100.0)

    def __unicode__(self):
        return "%s (%s)" % (self.channel_id, self.day)


class CodeTemplate(ModelMixin, db.Model):
    __tablename__ = 'code_templates'
    per_page = 50

    name = Column(String(255), default='', nullable=False, unique=True)
    template = Column(Text(), default='', nullable=False)
    template_static = Column(Text(), default='', nullable=False)
    updated = Column(TIMESTAMP, default=datetime.now, nullable=False)
    created = Column(TIMESTAMP, default=datetime.now, nullable=False)

    def __unicode__(self):
        return "%s" % self.name


class Parameter(ModelMixin, db.Model):
    __tablename__ = 'system_parameters'
    per_page = 1000

    name = Column(String(255), default='', nullable=False)
    key = Column(String(255), default='', nullable=False, unique=True)
    value = Column(Text(), default='', nullable=False)
    updated = Column(TIMESTAMP, default=datetime.now, nullable=False)
    created = Column(TIMESTAMP, default=datetime.now, nullable=False)

    @classmethod
    def get_by_key(cls, key):
        return cls.query.filter_by(key=key).one()

    def __unicode__(self):
        return "%s" % self.name


class ClicksLog(ModelMixin, db.Model):
    __tablename__ = 'clicks_log'
    per_page = 20

    uid = Column(String(32), nullable=False)
    ip = Column(String(15), nullable=False)
    user_agent = Column(String(255), nullable=False)
    referer = Column(Text(), nullable=False)
    link = Column(Text(), nullable=False)
    channel_id = Column(Integer(), ForeignKey('channels.id', onupdate="cascade", ondelete='restrict'))
    scenario_id = Column(Integer(), ForeignKey('scenarios.id', onupdate="cascade", ondelete='restrict'))
    payout = Column(Integer, nullable=False)
    cost = Column(Integer, nullable=False)
    reported = Column(Integer, nullable=False)
    status = Column(Enum(*CLICK_STATUSES, name='clicks_status'), default='new', nullable=False)
    updated = Column(DateTime, default=datetime.now)
    created = Column(DateTime, default=datetime.now)

    channel = db.relationship("Channel")
    scenario = db.relationship("Scenario")

    def __unicode__(self):
        return "%s" % self.id

    def is_new(self):
        return self.status == 'new'

    def is_accepted(self):
        return self.status == 'accepted'

    def is_rejected(self):
        return self.status == 'rejected'

    def accept(self, commit=True):
        if self.status == 'rejected' and self.reported == 1:
            self.reported = 3
        self.status = 'accepted'
        return commit and db.session.commit()

    def reject(self, commit=True):
        if self.status == 'accepted' and self.reported == 1:
            self.reported = 3
        self.status = 'rejected'
        return commit and db.session.commit()


class ConversionsLog(ModelMixin, db.Model):
    __tablename__ = 'conversions_log'
    per_page = 20

    click_id = Column(Integer(), ForeignKey('clicks_log.id', onupdate="cascade", ondelete='restrict'))
    uid = Column(String(32), nullable=False)
    ip = Column(String(15), nullable=False)
    user_agent = Column(String(255), nullable=False)
    referer = Column(Text(), nullable=False)
    channel_id = Column(Integer(), ForeignKey('channels.id', onupdate="cascade", ondelete='restrict'))
    scenario_id = Column(Integer(), ForeignKey('scenarios.id', onupdate="cascade", ondelete='restrict'))
    payout = Column(Integer, nullable=False)
    cost = Column(Integer, nullable=False)
    reported = Column(Integer, nullable=False)
    status = Column(Enum(*CONVERSATION_STATUSES, name='conversation_status'), default='new', nullable=False)
    updated = Column(DateTime, default=datetime.now)
    created = Column(DateTime, default=datetime.now)

    click_log = db.relationship("ClicksLog")
    channel = db.relationship("Channel")
    scenario = db.relationship("Scenario")

    def is_new(self):
        return self.status == 'new'

    def is_accepted(self):
        return self.status == 'accepted'

    def is_rejected(self):
        return self.status == 'rejected'

    def accept(self, commit=True):
        if self.status == 'rejected' and self.reported == 1:
            self.reported = 0
        self.status = 'accepted'
        return commit and db.session.commit()

    def reject(self, commit=True):
        if self.status == 'accepted' and self.reported == 1:
            self.reported = 3
        self.status = 'rejected'
        return commit and db.session.commit()

    def __unicode__(self):
        return "%s" % self.id


class HitsLog(ModelMixin, db.Model):
    __tablename__ = 'hits_log'
    per_page = 20

    link_id = Column(Integer, nullable=False)
    click_id = Column(Integer, primary_key=True)
    client_id = Column(Integer, nullable=False)
    section_id = Column(Integer, nullable=False)
    uid = Column(String(32), nullable=False)
    ip = Column(String(15), nullable=False)
    user_agent = Column(String(255), nullable=False)
    referer = Column(Text(), nullable=False)
    reported = Column(Boolean, nullable=False)
    status = Column(Integer, nullable=False)
    created = Column(DateTime, default=datetime.now)

    def __unicode__(self):
        return "%s" % self.name


class UserHelperMixin(object):
    role = ""

    def get_role(self):
        if self.role:
            return self.role
        return ''

    def is_admin(self):
        return self.role == 'admin'

    def is_manager(self):
        return self.role == 'manager'

    def is_client(self):
        return self.role == 'client'

    def is_partner(self):
        return self.role == 'partner'

    def is_active(self):
        return self.status == 'active'

    def is_blocked(self):
        return self.status == 'blocked'

    def is_deleted(self):
        return self.status == 'deleted'

    def is_anonymous(self):
        raise NotImplementedError


class User(UserHelperMixin, UserMixin, db.Model):
    __tablename__ = 'users'
    __table_args__ = {'mysql_charset': 'utf8', 'mysql_engine': 'InnoDB'}
    per_page = 20

    id = Column(Integer(), primary_key=True)
    role = Column(Enum(*ROLES, name='role'), nullable=False)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(80), nullable=False)
    secret = Column(String(255), default='', nullable=True)
    auth_token = Column(String(255), nullable=True)
    company = Column(String(255), default='', nullable=False)
    contact_name = Column(String(255), default='', nullable=False)
    phone = Column(String(255), default='', nullable=False)
    address = Column(Text(), default='', nullable=False)
    money = Column(Integer(), default=0, nullable=False)
    comment = Column(Text(), default='', nullable=True)
    status = Column(Enum(*STATUSES, name='status'), default='active', nullable=False)
    updated = Column(TIMESTAMP, default=datetime.now, nullable=False)
    created = Column(TIMESTAMP, default=datetime.now, nullable=False)

    sections = db.relationship('Section', back_populates="client", order_by="Section.name")
    scenarios = db.relationship('Scenario', back_populates="client", order_by="Scenario.name")
    channels = db.relationship('Channel', back_populates="partner", order_by="Channel.name")

    section_count = db.column_property(
        db.select([db.func.count(Section.id)]).where(Section.client_id == id).correlate_except(Section),
    )
    scenario_count = db.column_property(
        db.select([db.func.count(Scenario.id)]).where(Scenario.client_id == id).correlate_except(Scenario),
    )
    scenario_clicks = db.column_property(
        db.select([db.func.sum(Scenario.clicks)], Scenario.client_id == id).correlate_except(Scenario),
    )
    scenario_convs = db.column_property(
        db.select([db.func.sum(Scenario.convs)], Scenario.client_id == id).correlate_except(Scenario),
    )

    channel_clicks = db.column_property(
        db.select([db.func.sum(Channel.clicks)], Channel.partner_id == id).correlate_except(Channel),
    )
    channel_convs = db.column_property(
        db.select([db.func.sum(Channel.convs)], Channel.partner_id == id).correlate_except(Channel),
    )

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        password = kwargs.get('password')
        if not password:
            raise exception.UserCreate('password')
        self.set_password(password)

    def get_id(self):
        return self.id

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.email)

    def set_password(self, password):
        if not password:
            return
        self.set_secret(True)
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def check_secret(self, secret):
        return self.secret == secret

    def set_secret(self, force=False):
        if force or not self.secret:
            self.secret = generate_random()
        return self.secret

    def get_auth_token(self):
        return self.auth_token

    def get_money(self):
        return "%0.2f" % (self.money / 100.0)

    def is_anonymous(self):
        return False

    @classmethod
    def get(cls, id):
        # return cls.query.get(int(id))
        return cls.query.filter_by(id=id, status='active').first()

    @classmethod
    def get_or_404(cls, id):
        if any((isinstance(id, basestring) and id.isdigit(), isinstance(id, (int, float))),):
            return cls.query.get_or_404(int(id))
        return abort(404)

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(mail=email).first()

    def update(self, commit=True, **kwargs):
        for attr, value in kwargs.iteritems():
            if attr == 'password':
                self.set_password(value)
            else:
                setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        self.status = 'deleted'
        return commit and db.session.commit()

    def activate(self, commit=True):
        self.status = 'active'
        return commit and db.session.commit()

    def block(self, commit=True):
        self.status = 'blocked'
        return commit and db.session.commit()


class Anonymous(UserHelperMixin, AnonymousUserMixin):
    name = _(u"Гость")

    def get_id(self):
        return 0

    def get_role(self):
        return ''

    def is_anonymous(self):
        return True


Index('user_role', User.role)
