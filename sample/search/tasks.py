import logging

from celery.task import task
from django.db import connections

from sample.job_profiles.models import JobProfile
from sample.search.models import (ExternalJobProfile, ExternalJobProfileVacancy, ExternalVacancy, JobProfileMatching,
                                     JobProfileVacancy, VacancyMatching)
from sample.vacancies.models import Vacancy

logger = logging.getLogger('celery')


def refresh_materialized_view():
    cursor = connections['matching'].cursor()
    cursor.execute("""
        REFRESH MATERIALIZED VIEW cv_skill_correlations;
        REFRESH MATERIALIZED VIEW cand_skill_importance;
        REFRESH MATERIALIZED VIEW posting_skill_correlations;
        REFRESH MATERIALIZED VIEW posting_skill_importance;
        REFRESH MATERIALIZED VIEW cand_job_matches;
    """)


@task()
def job_profile_score(job_profile_id):
    """Receive job profile matching score"""

    job_profile = JobProfile.objects.get(id=job_profile_id)
    ext_job_profile, created = ExternalJobProfile.objects.get_or_create(cv_content=job_profile.get_content())
    JobProfileMatching.objects.get_or_create(
        job_profile_id=job_profile.pk,
        external_id=ext_job_profile.pk,
    )
    refresh_materialized_view()
    matchings = ExternalJobProfileVacancy.objects.filter(cv=ext_job_profile)
    for matching in matchings:
        vacancy_matchings = VacancyMatching.objects.filter(external_id=matching.job_id)
        for vacancy_matching in vacancy_matchings:
            job_profile_matchings = JobProfileMatching.objects.filter(external_id=matching.cv_id)
            for job_profile_matching in job_profile_matchings:
                JobProfileVacancy.objects.update_or_create(
                    job_profile=job_profile_matching.job_profile,
                    vacancy=vacancy_matching.vacancy,
                    score=matching.match_score,
                )
    return True

@task()
def vacancy_score(vacancy_id):
    """Receive vacancy matching score"""

    vacancy = Vacancy.objects.get(id=vacancy_id)
    ext_vacancy, created = ExternalVacancy.objects.get_or_create(job_posting=vacancy.get_content())
    VacancyMatching.objects.get_or_create(
        vacancy=vacancy,
        external_id=ext_vacancy.pk,
    )
    refresh_materialized_view()
    matchings = ExternalJobProfileVacancy.objects.filter(job=ext_vacancy)
    for matching in matchings:
        vacancy_matchings = VacancyMatching.objects.filter(external_id=matching.job_id)
        for vacancy_matching in vacancy_matchings:
            job_profile_matchings = JobProfileMatching.objects.filter(external_id=matching.cv_id)
            for job_profile_matching in job_profile_matchings:
                JobProfileVacancy.objects.update_or_create(
                    job_profile=job_profile_matching.job_profile,
                    vacancy=vacancy_matching.vacancy,
                    score=matching.match_score,
                )
    return True
