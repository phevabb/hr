from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = (
        'user_id', 'first_name', 'last_name', 'middle_name', 'role', 'gender',
        'phone_number', 'email', 'region', 'district', 'payroll_status',
        'date_of_birth', 'age', 'date_of_retirement', 'is_active', 'is_staff', 'is_superuser'
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
                'user_id', 'title', 'first_name', 'last_name', 'middle_name',
                'maiden_name', 'gender', 'date_of_birth', 'age', 'marital_status',
                'phone_number', 'ghana_card_number', 'social_security_number',
                'national_health_insurance_number'
            )
        }),
        ('Job Details', {
            'fields': (
                'role', 'category', 'directorate', 'staff_category', 'region', 'district',
                'current_grade', 'next_grade', 'date_of_first_appointment',
                'date_of_assumption_of_duty', 'date_of_last_promotion', 'date_of_retirement',
                'years_on_current_grade', 'number_of_years_in_service',
                'fulltime_contract_staff', 'academic_qualification', 'professional_qualification'
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
