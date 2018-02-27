from django.db.models import Avg
from rest_framework.viewsets import ReadOnlyModelViewSet

from sample.api.permissions import IsRecruiter
from sample.api.search.filters import FilterSearchJobProfile
from sample.api.search.serializers import SearchJobProfileSerializer
from sample.job_profiles.models import JobProfile
from sample.vacancies.models import Vacancy


class SearchJobProfileViewSet(ReadOnlyModelViewSet):
    """
    ViewSet for search job profiles
    """

    serializer_class = SearchJobProfileSerializer
    search_fields = (
        'preferences__location__city__name', 'preferences__location__state__name',
        'preferences__location__country__name')
    filter_class = FilterSearchJobProfile
    permission_classes = (IsRecruiter,)
    queryset_param = 'vacancy_id'
    vacancies = None

    def list(self, request, *args, **kwargs):
        vacancy_id = request.query_params.get(self.queryset_param, None)
        if vacancy_id:
            self.vacancies = Vacancy.objects.filter(id=vacancy_id, company__user=request.user,
                                                    company__user__is_recruiter=True)
        return super(SearchJobProfileViewSet, self).list(request, *args, **kwargs)

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_recruiter:
            queryset = JobProfile.objects.filter(is_published=True, is_default=True, user__is_candidate=True)
            if not self.vacancies:
                self.vacancies = Vacancy.objects.filter(company__user=self.request.user,
                                                        company__user__is_recruiter=True)
            queryset = queryset.filter(jobprofilevacancy__vacancy__in=self.vacancies)
            queryset = queryset.annotate(score=Avg('jobprofilevacancy__score'))
            if self.request.user.is_authenticated and self.request.user.is_candidate:
                queryset = queryset.exclude(user=self.request.user)
            return queryset
        return JobProfile.objects.none()
