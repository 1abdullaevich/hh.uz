from django.contrib import admin
from .models import *


@admin.register(LocationModel)
class LocationModelAdmin(admin.ModelAdmin):
    list_display = ['city', 'country']
    search_fields = ['city', 'country']


@admin.register(MyUserModel)
class MyUserModelAdmin(admin.ModelAdmin):
    list_display = ['email', 'phone_number', 'location', 'is_staff']
    search_fields = ['email', 'phone_number']
    list_filter = ['is_staff', 'location']


@admin.register(CompanyModel)
class CompanyModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'description', 'website']
    search_fields = ['name', 'user__email']
    list_filter = ['user__location']


@admin.register(VacancyModel)
class VacancyModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'location', 'created_at', 'expiration_date']
    search_fields = ['title', 'company__name']
    list_filter = ['created_at', 'expiration_date']


@admin.register(ApplicationModel)
class ApplicationModelAdmin(admin.ModelAdmin):
    list_display = ['employee', 'vacancy', 'message', 'applied_at']
    search_fields = ['employee__email', 'vacancy__title']
    list_filter = ['applied_at']


@admin.register(SkillModel)
class SkillModelAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(EducationModel)
class EducationModelAdmin(admin.ModelAdmin):
    list_display = ['degree', 'institution', 'graduation_year']
    search_fields = ['degree', 'institution']
    list_filter = ['graduation_year']


@admin.register(ExperienceModel)
class ExperienceModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'start_date', 'end_date']
    search_fields = ['title', 'company']
    list_filter = ['start_date', 'end_date']


@admin.register(SkillSetModel)
class SkillSetModelAdmin(admin.ModelAdmin):
    list_display = ['employee', 'skill']
    search_fields = ['employee__email', 'skill__name']


@admin.register(EmployeeEducationModel)
class EmployeeEducationModelAdmin(admin.ModelAdmin):
    list_display = ['employee', 'education']
    search_fields = ['employee__email', 'education__degree']


@admin.register(EmployeeExperienceModel)
class EmployeeExperienceModelAdmin(admin.ModelAdmin):
    list_display = ['employee', 'experience']
    search_fields = ['employee__email', 'experience__title']
