from django import forms

departments_choice = (
    ('Admin', "Admin"),  ('Manager',"Manager"), ("Staff", "Staff"),
)


class Login_form(forms.Form):
    staff_department = forms.ChoiceField(required=False, choices=departments_choice)
    user_ID = forms.CharField(required=True)
    password = forms.CharField(required=True)


from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False,
        help_text="Leave empty to keep the default password 'Securepassword123!'"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = User
        fields = '__all__'
        exclude = ['last_login', 'is_superuser', 'groups', 'user_permissions', 'is_staff', 'is_active']

        widgets = {
            'user_id': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.Select(attrs={'class': 'form-select'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
            'maiden_name': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'marital_status': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'directorate': forms.Select(attrs={'class': 'form-select'}),
            'current_grade': forms.Select(attrs={'class': 'form-select'}),
            'next_grade': forms.Select(attrs={'class': 'form-select'}),
            'current_salary_level': forms.TextInput(attrs={'class': 'form-control'}),
            'current_salary_point': forms.TextInput(attrs={'class': 'form-control'}),
            'next_salary_level': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_first_appointment': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_of_assumption_of_duty': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_of_last_promotion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'change_of_grade': forms.Select(attrs={'class': 'form-select'}),
            'substantive_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'national_effective_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'years_on_current_grade': forms.NumberInput(attrs={'class': 'form-control'}),
            'number_of_years_in_service': forms.NumberInput(attrs={'class': 'form-control'}),
            'fulltime_contract_staff': forms.Select(attrs={'class': 'form-select'}),
            'academic_qualification': forms.TextInput(attrs={'class': 'form-control'}),
            'professional_qualification': forms.TextInput(attrs={'class': 'form-control'}),
            'staff_category': forms.Select(attrs={'class': 'form-select'}),
            'region': forms.Select(attrs={'class': 'form-select'}),
            'district': forms.Select(attrs={'class': 'form-select'}),
            'single_spine_monthly_salary': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'monthly_gross_pay': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'annual_salary': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'date_of_retirement': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'number_of_focus_areas': forms.NumberInput(attrs={'class': 'form-control'}),
            'number_of_targets': forms.NumberInput(attrs={'class': 'form-control'}),
            'number_of_targets_met': forms.NumberInput(attrs={'class': 'form-control'}),
            'number_of_targets_not_met': forms.NumberInput(attrs={'class': 'form-control'}),
            'overall_assessment_score': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'self_assessment_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'ghana_card_number': forms.TextInput(attrs={'class': 'form-control'}),
            'social_security_number': forms.TextInput(attrs={'class': 'form-control'}),
            'national_health_insurance_number': forms.TextInput(attrs={'class': 'form-control'}),
            'bank_name': forms.TextInput(attrs={'class': 'form-control'}),
            'bank_account_number': forms.TextInput(attrs={'class': 'form-control'}),
            'bank_account_branch': forms.TextInput(attrs={'class': 'form-control'}),
            'management_unit_cost_centre': forms.Select(attrs={'class': 'form-select'}),
            'payroll_status': forms.Select(attrs={'class': 'form-select'}),
            'at_post_on_leave': forms.Select(attrs={'class': 'form-select'}),
            'on_leave_type': forms.TextInput(attrs={'class': 'form-control'}),
            'accommodation_status': forms.Select(attrs={'class': 'form-select'}),
            'supervisor_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show password fields when creating a new user
        if self.instance and self.instance.pk:
            self.fields['password'].help_text = "Enter new password to change, or leave empty to keep current password"

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and password != confirm_password:
            self.add_error('confirm_password', "Passwords don't match")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)

        # Set default password for new users if no password provided
        if not user.pk and not self.cleaned_data.get('password'):
            user.set_password('Securepassword123!')
        # Update password if provided
        elif self.cleaned_data.get('password'):
            user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()
        return user


class UserCreateForm(UserForm):
    class Meta(UserForm.Meta):
        fields = ['user_id', 'first_name', 'last_name', 'role', 'password', 'confirm_password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make password fields required for new user creation
        self.fields['password'].required = True
        self.fields['confirm_password'].required = True
        self.fields['password'].help_text = "Default password will be 'Securepassword123!' if left empty"