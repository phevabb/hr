from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserRemovalLog, User, Department, Classes, CurrentGrade, ManagementUnit, Region, Districts, ChangeOfGrade, AcademicQualification


#@admin.register(ChangeOfGrade)
#class ChangeOfGradeAdmin(admin.ModelAdmin):
#    list_display = ('grade',)
#    search_fields = ('grade',)


#@admin.register(Districts)
#class DistrictsAdmin(admin.ModelAdmin):
#    list_display = ('district',)
#    search_fields = ('district',)


#@admin.register(Region)
##class RegionAdmin(admin.ModelAdmin):
 #   list_display = ('region',)
 #   search_fields = ('region',)


@admin.register(AcademicQualification)
class AcademicQualificationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(UserRemovalLog)
class UserRemovalLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'reason', 'removed_at')
    search_fields = ('user__username', 'reason')
    list_filter = ('removed_at', 'reason')
    ordering = ('-removed_at',)  # latest removals first


@admin.register(ManagementUnit)
class ManagementUnitAdmin(admin.ModelAdmin):
    list_display = ('management_unit_name',)
    search_fields = ('management_unit_name',)

@admin.register(CurrentGrade)
class CurrentGradeAdmin(admin.ModelAdmin):
    list_display = ['current_grade']
    list_filter = ['current_grade']

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    model = Department
    list_display = ('department_name',)
    list_filter = ('department_name',)


@admin.register(Classes)
class ClassesAdmin(admin.ModelAdmin):
    model = Classes
    list_display = ('classes_name',)
    list_filter = ('classes_name',)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = (
        'id','user_id', 'first_name', 'last_name', 'middle_name', 'role', 'gender',
        'phone_number', 'email', 'region', 'district', 'payroll_status',
        'date_of_birth', 'is_active', 'is_staff', 'is_superuser'
    )
    list_filter = (
        'role', 'gender', 'marital_status', 'region', 'district',
        'payroll_status', 'staff_category', 'is_active'
    )
    search_fields = (
        'user_id', 'first_name', 'last_name', 'phone_number',
        'ghana_card_number', 'social_security_number',
        'national_health_insurance_number', 'bank_account_number'
    )
    ordering = ('first_name', 'last_name',)

    fieldsets = (
        ('Personal Information', {
            'fields': (
                'user_id', 'profile_picture', 'email', 'title', 'first_name', 'last_name', 'middle_name',
                'maiden_name', 'gender', 'date_of_birth', 'marital_status',
                'phone_number', 'ghana_card_number', 'social_security_number',
                'national_health_insurance_number'
            )
        }),
        ('Job Details', {
            'fields': (
                'role', 'category', 'directorate', 'staff_category', 'region', 'district',
                'current_grade', 'next_grade', 'date_of_first_appointment',
                'date_of_assumption_of_duty', 'date_of_last_promotion', 
              'professional',
                'fulltime_contract_staff', 'academic_qualifications', 'professional_qualification'
            )
        }),
        ('Salary & Payroll', {
            'fields': (
                'current_salary_level', 'current_salary_point', 'next_salary_level',
                'single_spine_monthly_salary', 'monthly_gross_pay', 'annual_salary',
                'payroll_status', 'management_unit_cost_centre'
            )
        }),
        ('Performance & Assessment', {
            'fields': (
                'number_of_focus_areas', 'number_of_targets', 'number_of_targets_met',
                'number_of_targets_not_met', 'overall_assessment_score',
                'self_assessment_description'
            )
        }),
        ('Banking Information', {
            'fields': (
                'bank_name', 'bank_account_number', 'bank_account_branch'
            )
        }),
        ('Other Details', {
            'fields': (
                'at_post_on_leave', 'on_leave_type', 'accommodation_status',
                'supervisor_name'
            )
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'
            )
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'user_id', 'password1', 'password2', 'title', 'first_name',
                'last_name', 'role', 'phone_number', 'gender', 'region',
                'district', 'is_staff', 'is_superuser'
            ),
        }),
    )
