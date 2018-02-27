from django.db import models
from django.utils import timezone


class JobProfileVacancy(models.Model):
    job_profile = models.ForeignKey('job_profiles.JobProfile', on_delete=models.CASCADE)
    vacancy = models.ForeignKey('vacancies.Vacancy', on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=15, decimal_places=6)
    modified = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'search_jobprofile_vacancy'
        unique_together = (('job_profile', 'vacancy'),)
        ordering = ('-score',)

    def __str__(self):
        return '{} {} {}'.format(self.job_profile.name, self.vacancy.role, self.score)


class JobProfileMatching(models.Model):
    job_profile = models.ForeignKey('job_profiles.JobProfile', on_delete=models.CASCADE)
    external_id = models.IntegerField()

    class Meta:
        db_table = 'search_jobprofile_matching'
        unique_together = (('job_profile', 'external_id'),)


class VacancyMatching(models.Model):
    vacancy = models.ForeignKey('vacancies.Vacancy', on_delete=models.CASCADE)
    external_id = models.IntegerField()

    class Meta:
        db_table = 'search_vacancy_matching'
        unique_together = (('vacancy', 'external_id'),)


class ExternalJobProfile(models.Model):
    cv_id = models.AutoField(primary_key=True)
    cv_content = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'cvs'


class ExternalVacancy(models.Model):
    job_id = models.AutoField(primary_key=True)
    job_posting = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'jobs'


class ExternalJobProfileVacancy(models.Model):
    cv = models.OneToOneField(ExternalJobProfile, on_delete=models.CASCADE, primary_key=True)
    job = models.OneToOneField(ExternalVacancy, on_delete=models.CASCADE)
    match_score = models.DecimalField(max_digits=15, decimal_places=6)

    class Meta:
        db_table = 'cand_job_matches'
