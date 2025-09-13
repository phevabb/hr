from django.contrib.auth import get_user_model
from rest_framework import serializers

from account.models import (
    AcademicQualification, Region, Districts, Department,
    Classes, NextGrade, ManagementUnit, CurrentGrade, ChangeOfGrade
)

User = get_user_model()

class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a new user with password validation and academic qualifications."""
    password = serializers.CharField(write_only=True, required=False, style={"input_type": "password"})
    confirm_password = serializers.CharField(write_only=True, required=False, style={"input_type": "password"})
    academic_qualifications = serializers.PrimaryKeyRelatedField(
        queryset=AcademicQualification.objects.all(), many=True, required=False
    )

    class Meta:
        model = User
        fields = [
            "id", "email", "user_id", "first_name", "last_name", "role", "password", "confirm_password",
            "current_grade", "next_grade", "change_of_grade", "date_of_assumption_of_duty",
            "date_of_retirement", "profile_picture", "management_unit_cost_centre",
            "directorate", "category", "district", "region", "academic_qualifications",
            "full_name", "title", "gender", "date_of_birth", "age", "marital_status",
            "current_salary_level", "current_salary_point", "date_of_first_appointment",
            "date_of_last_promotion", "number_of_years_in_service", "professional_qualification",
            "monthly_gross_pay", "annual_salary", "phone_number", "ghana_card_number",
            "social_security_number", "national_health_insurance_number", "bank_name",
            "bank_account_branch", "bank_account_number", "next_salary_level",
            "payroll_status", "accommodation_status", "supervisor_name", "at_post_on_leave",
            "fulltime_contract_staff", "national_effective_date", "substantive_date",
            "staff_category", "single_spine_monthly_salary", "self_assessment_description",
            "overall_assessment_score", "number_of_targets", "number_of_targets_met",
            "number_of_targets_not_met", "number_of_focus_areas", "years_on_current_grade",
            "professional"
        ]
        extra_kwargs = {
            "user_id": {"required": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
            "role": {"required": True},
            "password": {"write_only": True}
        }

    def validate(self, attrs):
        """Validate that passwords match if provided."""
        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")

        if password and password != confirm_password:
            raise serializers.ValidationError({"confirm_password": "Passwords don't match"})

        return attrs

    def create(self, validated_data):
        """Create a user with password hashing and set academic qualifications."""
        password = validated_data.pop("password", None)
        validated_data.pop("confirm_password", None)
        academic_qualifications = validated_data.pop("academic_qualifications", [])

        user = User.objects.create_user(**validated_data)
        if password:
            user.set_password(password)
        else:
            user.set_password("Securepassword123!")

        user.save()
        if academic_qualifications:
            user.academic_qualifications.set(academic_qualifications)
        return user

class RegionSerializer(serializers.ModelSerializer):
    """Serializer for Region model."""
    class Meta:
        model = Region
        fields = ['id', 'region']

class DistrictSerializer(serializers.ModelSerializer):
    """Serializer for Districts model."""
    class Meta:
        model = Districts
        fields = ['id', 'district']

class DepartmentSerializer(serializers.ModelSerializer):
    """Serializer for Department model."""
    class Meta:
        model = Department
        fields = ['id', 'department_name']

class ClassesSerializer(serializers.ModelSerializer):
    """Serializer for Classes model."""
    class Meta:
        model = Classes
        fields = ['id', 'classes_name']

class ManagementUnitSerializer(serializers.ModelSerializer):
    """Serializer for ManagementUnit model."""
    class Meta:
        model = ManagementUnit
        fields = ['id', 'management_unit_name']

class CurrentGradeSerializer(serializers.ModelSerializer):
    """Serializer for CurrentGrade model."""
    class Meta:
        model = CurrentGrade
        fields = ['id', 'current_grade']

class ChangeOfGradeSerializer(serializers.ModelSerializer):
    """Serializer for ChangeOfGrade model."""
    class Meta:
        model = ChangeOfGrade
        fields = ['id', 'grade']

class AcademicQualificationSerializer(serializers.ModelSerializer):
    """Serializer for AcademicQualification model."""
    class Meta:
        model = AcademicQualification
        fields = ['id', 'name']

class UserFieldsSerializer(serializers.Serializer):
    """Serializer for User model field metadata."""
    field_name = serializers.CharField()
    field_type = serializers.CharField()
    choices = serializers.ListField(child=serializers.ListField(), required=False)

class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user details with foreign key fields."""
    academic_qualifications = serializers.PrimaryKeyRelatedField(
        many=True, queryset=AcademicQualification.objects.all(), required=False
    )
    current_grade = serializers.PrimaryKeyRelatedField(
        queryset=CurrentGrade.objects.all(), required=False
    )
    next_grade = serializers.PrimaryKeyRelatedField(
        queryset=NextGrade.objects.all(), required=False
    )
    change_of_grade = serializers.PrimaryKeyRelatedField(
        queryset=ChangeOfGrade.objects.all(), required=False
    )
    management_unit_cost_centre = serializers.PrimaryKeyRelatedField(
        queryset=ManagementUnit.objects.all(), required=False
    )
    directorate = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(), required=False
    )
    category = serializers.PrimaryKeyRelatedField(
        queryset=Classes.objects.all(), required=False
    )
    district = serializers.PrimaryKeyRelatedField(
        queryset=Districts.objects.all(), required=False
    )
    region = serializers.PrimaryKeyRelatedField(
        queryset=Region.objects.all(), required=False
    )

    class Meta:
        model = User
        fields = [
            "id", "user_id", "email", "current_grade", "next_grade", "change_of_grade",
            "date_of_assumption_of_duty", "date_of_retirement", "profile_picture",
            "management_unit_cost_centre", "directorate", "category", "district", "region",
            "academic_qualifications", "full_name", "title", "gender", "date_of_birth",
            "age", "marital_status", "current_salary_level", "current_salary_point",
            "date_of_first_appointment", "date_of_last_promotion", "number_of_years_in_service",
            "professional_qualification", "monthly_gross_pay", "annual_salary",
            "phone_number", "ghana_card_number", "social_security_number",
            "national_health_insurance_number", "bank_name", "bank_account_branch",
            "bank_account_number", "next_salary_level", "payroll_status",
            "accommodation_status", "supervisor_name", "at_post_on_leave",
            "fulltime_contract_staff", "national_effective_date", "substantive_date",
            "staff_category", "single_spine_monthly_salary", "self_assessment_description",
            "overall_assessment_score", "number_of_targets", "number_of_targets_met",
            "number_of_targets_not_met", "number_of_focus_areas", "years_on_current_grade",
            "role", "professional"
        ]

    def to_representation(self, instance):
        """Convert foreign key IDs to human-readable names."""
        rep = super().to_representation(instance)
        rep["current_grade"] = (
            instance.current_grade.current_grade if instance.current_grade else None
        )
        rep["next_grade"] = (
            instance.next_grade.next_grade if instance.next_grade else None
        )
        rep["change_of_grade"] = (
            instance.change_of_grade.grade if instance.change_of_grade else None
        )
        rep["management_unit_cost_centre"] = (
            instance.management_unit_cost_centre.management_unit_name
            if instance.management_unit_cost_centre else None
        )
        rep["directorate"] = (
            instance.directorate.department_name if instance.directorate else None
        )
        rep["category"] = (
            instance.category.classes_name if instance.category else None
        )
        rep["district"] = instance.district.district if instance.district else None
        rep["region"] = instance.region.region if instance.region else None
        rep["academic_qualifications"] = [
            {"id": aq.id, "name": aq.name}
            for aq in instance.academic_qualifications.all()
        ]
        return rep

class UserSerializer(serializers.ModelSerializer):
    """Serializer for retrieving user details with human-readable foreign key fields."""
    management_unit_cost_centre = serializers.CharField(
        source="management_unit_cost_centre.management_unit_name", read_only=True
    )
    directorate = serializers.CharField(source="directorate.department_name", read_only=True)
    category = serializers.CharField(source="category.classes_name", read_only=True)
    district = serializers.CharField(source="district.district", read_only=True)
    region = serializers.CharField(source="region.region", read_only=True)
    change_of_grade = serializers.CharField(source="change_of_grade.grade", read_only=True)
    next_grade = serializers.CharField(source="next_grade.next_grade", read_only=True)
    current_grade = serializers.CharField(source="current_grade.current_grade", read_only=True)
    academic_qualifications = serializers.PrimaryKeyRelatedField(
        many=True, queryset=AcademicQualification.objects.all(), required=False
    )

    class Meta:
        model = User
        fields = [
            "id", "email", "user_id", "first_name", "last_name", "role", "professional",
            "current_grade", "next_grade", "change_of_grade", "date_of_assumption_of_duty",
            "date_of_retirement", "profile_picture", "management_unit_cost_centre",
            "directorate", "category", "district", "region", "academic_qualifications",
            "full_name", "title", "gender", "date_of_birth", "age", "marital_status",
            "current_salary_level", "current_salary_point", "date_of_first_appointment",
            "date_of_last_promotion", "number_of_years_in_service", "professional_qualification",
            "monthly_gross_pay", "annual_salary", "phone_number", "ghana_card_number",
            "social_security_number", "national_health_insurance_number", "bank_name",
            "bank_account_branch", "bank_account_number", "next_salary_level",
            "payroll_status", "accommodation_status", "supervisor_name", "at_post_on_leave",
            "fulltime_contract_staff", "national_effective_date", "substantive_date",
            "staff_category", "single_spine_monthly_salary", "self_assessment_description",
            "overall_assessment_score", "number_of_targets", "number_of_targets_met",
            "number_of_targets_not_met", "number_of_focus_areas", "years_on_current_grade"
        ]

    def to_representation(self, instance):
        """Convert academic qualifications to include IDs and names."""
        rep = super().to_representation(instance)
        rep["academic_qualifications"] = [
            {"id": aq.id, "name": aq.name} for aq in instance.academic_qualifications.all()
        ]
        return rep

    def update(self, instance, validated_data):
        """Update user instance and handle academic qualifications."""
        academic_qualifications = validated_data.pop("academic_qualifications", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if academic_qualifications is not None:
            instance.academic_qualifications.set(academic_qualifications)

        return instance

    def create(self, validated_data):
        """Create a user and set academic qualifications."""
        academic_qualifications = validated_data.pop("academic_qualifications", [])
        user = User.objects.create(**validated_data)
        if academic_qualifications:
            user.academic_qualifications.set(academic_qualifications)
        return user

class UserSerializerToExcel(serializers.ModelSerializer):
    """Serializer for exporting user data to Excel with flattened academic qualifications."""
    management_unit_cost_centre = serializers.CharField(
        source="management_unit_cost_centre.management_unit_name", read_only=True
    )
    directorate = serializers.CharField(source="directorate.department_name", read_only=True)
    category = serializers.CharField(source="category.classes_name", read_only=True)
    district = serializers.CharField(source="district.district", read_only=True)
    region = serializers.CharField(source="region.region", read_only=True)
    change_of_grade = serializers.CharField(source="change_of_grade.grade", read_only=True)
    next_grade = serializers.CharField(source="next_grade.next_grade", read_only=True)
    current_grade = serializers.CharField(source="current_grade.current_grade", read_only=True)
    academic_qualifications = serializers.PrimaryKeyRelatedField(
        many=True, queryset=AcademicQualification.objects.all(), required=False
    )

    class Meta:
        model = User
        fields = [
            "id", "email", "user_id", "first_name", "last_name", "role", "professional",
            "current_grade", "next_grade", "change_of_grade", "date_of_assumption_of_duty",
            "date_of_retirement", "profile_picture", "management_unit_cost_centre",
            "directorate", "category", "district", "region", "academic_qualifications",
            "full_name", "title", "gender", "date_of_birth", "age", "marital_status",
            "current_salary_level", "current_salary_point", "date_of_first_appointment",
            "date_of_last_promotion", "number_of_years_in_service", "professional_qualification",
            "monthly_gross_pay", "annual_salary", "phone_number", "ghana_card_number",
            "social_security_number", "national_health_insurance_number", "bank_name",
            "bank_account_branch", "bank_account_number", "next_salary_level",
            "payroll_status", "accommodation_status", "supervisor_name", "at_post_on_leave",
            "fulltime_contract_staff", "national_effective_date", "substantive_date",
            "staff_category", "single_spine_monthly_salary", "self_assessment_description",
            "overall_assessment_score", "number_of_targets", "number_of_targets_met",
            "number_of_targets_not_met", "number_of_focus_areas", "years_on_current_grade"
        ]

    def to_representation(self, instance):
        """Flatten academic qualifications for Excel export."""
        rep = super().to_representation(instance)
        rep["academic_qualifications"] = ", ".join(
            [aq.name for aq in instance.academic_qualifications.all()]
        )
        return rep

    def update(self, instance, validated_data):
        """Update user instance and handle academic qualifications."""
        academic_qualifications = validated_data.pop("academic_qualifications", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if academic_qualifications is not None:
            instance.academic_qualifications.set(academic_qualifications)

        return instance

    def create(self, validated_data):
        """Create a user and set academic qualifications."""
        academic_qualifications = validated_data.pop("academic_qualifications", [])
        user = User.objects.create(**validated_data)
        if academic_qualifications:
            user.academic_qualifications.set(academic_qualifications)
        return user