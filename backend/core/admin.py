from django.contrib import admin
from .models import EmployeeData, Skill, JobSkillRequirement, Recommendation

class EmployeeDataAdmin(admin.ModelAdmin):
    list_display = ("job_title", "country", "industry", "skills", "experience_years")

admin.site.register(EmployeeData, EmployeeDataAdmin)
admin.site.register(Skill)
admin.site.register(JobSkillRequirement)
admin.site.register(Recommendation)
