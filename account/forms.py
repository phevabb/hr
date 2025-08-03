from django import forms

departments_choice = (
    ('Admin', "Admin"),  ('Manager',"HR Manager"), ("Staff", "Staff"),

)


class LoginForm(forms.Form):
    staff_department = forms.ChoiceField(required=False, choices=departments_choice)
    user_ID = forms.CharField(required=True)
    password = forms.CharField(required=True)
