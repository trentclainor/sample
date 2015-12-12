# -*- coding: utf-8 -*-
from flask.ext.babel import gettext as _

ROLES = [
    ('admin', _(u'Админ')),
    ('manager', _(u'Менеджер')),
    ('client', _(u'Клиент')),
    ('partner', _(u'Партнер')),
]

ADMIN_ROLES = [
    ('admin', _(u' Администратор')),
    ('manager', _(u'Менеджер')),
]

SIGNUP_ROLES = [
    ('client', _(u'Клиент')),
    ('partner', _(u'Партнер')),
]

STATUSES = [
    ('active', _(u'Активен')),
    ('blocked', _(u'Заблокирован')),
    ('deleted', _(u'Удален')),
]

STATUSES_BLOCKED = [
    ('active', _(u'Активен')),
    ('blocked', _(u'Заблокирован')),
]

STATUSES_DELETED = [
    ('active', _(u'Активен')),
    ('deleted', _(u'Удален')),
]

SECTION_TYPES = [
    ('address', _(u'Адрес')),
    ('header', _(u'Заголовок')),
    ('id', _(u'ID')),
]

CHANNEL_TYPES = [
    ('CPC', _(u'Cost Per Click (CPC)')),
    ('CPA', _(u'Cost Per Action (CPA)')),
    ('manually', _(u'Вручную')),
]

COST_TYPES = [
    ('CPC', _(u'Cost Per Click (CPC)')),
    ('CPA', _(u'Cost Per Action (CPA)')),
]

MODERATION = [
    ('pre', _(u'Премодерация')),
    ('post', _(u'Постмодерация')),
]

REPORTS = [
    ('days', _(u'По датам')),
    ('sections', _(u'Разделы')),
    ('scenarios', _(u'Сценарии')),
]

CLICK_STATUSES = [
    ('new', _(u'Новый')),
    ('rejected', _(u'Отказано')),
    ('accepted', _(u'Принято')),
    ('reported', _(u'Уведомили')),
]

CONVERSATION_STATUSES = [
    ('new', _(u'Новая')),
    ('rejected', _(u'Отказано')),
    ('accepted', _(u'Принято')),
    ('reported', _(u'Уведомили')),
]

CONVERSATION_FILTER_STATUSES = [
    ('new', _(u'Новая')),
    ('rejected', _(u'Отказано')),
    ('accepted', _(u'Принято')),
]

CLICK_FILTER_STATUSES = [
    ('new', _(u'Новый')),
    ('rejected', _(u'Отказано')),
    ('accepted', _(u'Принято')),
]

CHOOSE_ROLE = [('', _(u'Выберите роль'))]
CHOOSE_CLIENT = [(0, _(u'Выберите клиента'))]
CHOOSE_SECTION_TYPE = [(0, _(u'Выберите тип'))]
CHOOSE_CHANNEL_TYPE = [(0, _(u'Выберите тип'))]
CHOOSE_COST_TYPE = [(0, _(u'Выберите способ оплаты'))]
CHOOSE_MODERATION = [(0, _(u'Выберите метод модерации'))]

NO_STATUS = [('no', _(u'Нет'))]
ANY_STATUS = [('', _(u'Любой статус'))]
ANY_CLIENT = [(0, _(u'Любой клиент'))]
ANY_SCENARIO = [(0, _(u'Любой сценарий'))]
ANY_PARTNER = [(0, _(u'Любой партнер'))]
ANY_CHANNEL = [(0, _(u'Любой канал'))]
