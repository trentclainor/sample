from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers as nested_routers

from sample.api.choices.views import ChoicesViewSet
from sample.api.common.views import (CountryViewSet, ExternalRoleViewSet, ExternalSkillViewSet, IndustryViewSet,
                                        LocationViewSet, RoleViewSet)
from sample.api.job_profile.views import (BasicInfoViewSet, EducationViewSet, JobProfileViewSet,
                                             LanguageViewSet, PreferencesViewSet, WorkHistoryViewSet)
from sample.api.search.views import (SearchJobProfileViewSet, SearchVacancyPersonalizedViewSet,
                                        SearchVacancyStandardViewSet)
from sample.api.user.views import (CandidateRegisterView, CompanyViewSet, RecruiterRegisterView, UserViewSet)
from sample.api.vacancy.views import (MessageViewSet, VacancyViewSet)
from sample.api.views import ObtainAuthToken

router = DefaultRouter()

router.register(r'users', UserViewSet, base_name='users')
user_router = nested_routers.NestedDefaultRouter(router, r'users', lookup='user')
user_router.register(r'companies', CompanyViewSet, base_name='users-companies')

router.register(r'job-profiles', JobProfileViewSet, base_name='job-profiles')
job_profile_router = nested_routers.NestedDefaultRouter(router, r'job-profiles', lookup='job_profile')
job_profile_router.register(r'basic-info', BasicInfoViewSet, base_name='job-profiles-basic-info')
job_profile_router.register(r'educations', EducationViewSet, base_name='job-profiles-educations')
job_profile_router.register(r'languages', LanguageViewSet, base_name='job-profiles-languages')
job_profile_router.register(r'preferences', PreferencesViewSet, base_name='job-profiles-preferences')
job_profile_router.register(r'work-histories', WorkHistoryViewSet, base_name='job-profiles-work-histories')

router.register(r'vacancies', VacancyViewSet, base_name='vacancies')
vacancy_router = nested_routers.NestedDefaultRouter(router, r'vacancies', lookup='vacancy')
vacancy_router.register(r'messages', MessageViewSet, base_name='vacancies-messages')

router.register(r'search/job-profiles', SearchJobProfileViewSet, base_name='search-job-profiles')
router.register(r'search/vacancies/personalized', SearchVacancyPersonalizedViewSet,
                base_name='search-vacancies-personalized')
router.register(r'search/vacancies/standard', SearchVacancyStandardViewSet, base_name='search-vacancies-standard')

common_router = DefaultRouter()
common_router.register(r'common/countries', CountryViewSet, base_name='common-contries')
common_router.register(r'common/external-roles', ExternalRoleViewSet, base_name='common-external-roles')
common_router.register(r'common/external-skills', ExternalSkillViewSet, base_name='common-external-skills')
common_router.register(r'common/industries', IndustryViewSet, base_name='common-industries')
common_router.register(r'common/locations', LocationViewSet, base_name='common-locations')
common_router.register(r'common/roles', RoleViewSet, base_name='common-roles')

router.register(r'choices', ChoicesViewSet, base_name='choices')

urlpatterns = [
    url(r'^auth-token/$', ObtainAuthToken.as_view(), name='auth-token'),
    url(r'^users/candidate-register/$', CandidateRegisterView.as_view(), name='users-candidate-register'),
    url(r'^users/recruiter-register/$', RecruiterRegisterView.as_view(), name='users-recruiter-register'),
]

urlpatterns += [
    url(r'^', include(router.urls)),
    url(r'^', include(common_router.urls)),
    url(r'^', include(job_profile_router.urls)),
    url(r'^', include(user_router.urls)),
    url(r'^', include(vacancy_router.urls)),
    url(r'^', include(router.urls)),
]
