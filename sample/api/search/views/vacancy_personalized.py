from django.db.models import F
from rest_framework.viewsets import ReadOnlyModelViewSet

from sample.api.permissions import IsCandidate
from sample.api.search import serializers
from sample.api.search.filters import FilterSearchVacancyPersonalized
from sample.job_profiles.models import JobProfile
from sample.vacancies.models import Vacancy


class SearchVacancyPersonalizedViewSet(ReadOnlyModelViewSet):
    """
    ViewSet for search personalized vacancies
    """

    serializer_class = serializers.SearchVacancyPersonalizedSerializer
    search_fields = ['name', 'location__city__name', 'location__state__name', 'location__country__name']
    filter_class = FilterSearchVacancyPersonalized
    permission_classes = (IsCandidate,)
    ordering = ('-modified',)
    queryset_param = 'job_profile_id'
    job_profile = None

    def list(self, request, *args, **kwargs):
        job_profile_id = request.query_params.get(self.queryset_param, None)
        if job_profile_id:
            self.job_profile = JobProfile.objects.filter(user=self.request.user, id=job_profile_id).select_related(
                'preferences').first()
        else:
            self.job_profile = JobProfile.objects.filter(user=self.request.user, is_published=True,
                                                         is_default=True).select_related('preferences').first()
        return super(SearchVacancyPersonalizedViewSet, self).list(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Vacancy.objects.select_related('location', 'location__city', 'location__country', 'industry',
                                                  'company', 'company__user', 'role').all()
        if self.job_profile:
            queryset = queryset.filter(jobprofilevacancy__job_profile=self.job_profile)
            queryset = queryset.annotate(score=F('jobprofilevacancy__score'))
            if hasattr(self.job_profile, 'preferences'):
                preferences = self.job_profile.preferences
                if preferences.industries.count():
                    queryset = queryset.filter(industry__in=preferences.industries.all())
                if preferences.roles.count():
                    queryset = queryset.filter(role__in=preferences.roles.all())
                if preferences.looking_for:
                    queryset = queryset.filter(types__overlap=preferences.looking_for)
                if preferences.location:
                    queryset = queryset.filter(location=preferences.location)
                return queryset
            return queryset
        return Vacancy.objects.none()
