from django.contrib import admin

from .models import BasicInfo, Education, JobProfile, Language, Preferences, WorkHistory

admin.site.register(JobProfile)
admin.site.register(BasicInfo)
admin.site.register(WorkHistory)
admin.site.register(Education)
admin.site.register(Language)
admin.site.register(Preferences)
