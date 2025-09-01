from django.contrib.auth import get_user_model
from rest_framework import serializers
from account.models import Region, Districts, Department, Classes, ManagementUnit, CurrentGrade, ChangeOfGrade

User = get_user_model()

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, style={"input_type": "password"})
    confirm_password = serializers.CharField(write_only=True, required=False, style={"input_type": "password"})

    class Meta:
        model = User
        # keep fields minimal (can expand as needed)
      
        exclude = ['last_login', 'is_superuser', 'groups', 'user_permissions', 'is_staff', 'is_active']

        extra_kwargs = {
            "user_id": {"required": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
            "role": {"required": True},
        }

    def validate(self, attrs):
        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")

        if password and password != confirm_password:
            raise serializers.ValidationError({"confirm_password": "Passwords don't match"})

        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        validated_data.pop("confirm_password", None)

        user = User(**validated_data)

        if not password:
            # Default password
            user.set_password("Securepassword123!")
        else:
            user.set_password(password)

        user.save()
        return user

# Backend API for dynamic options
class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'region']

class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = Districts
        fields = ['id', 'district']

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'department_name']

class ClassesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classes
        fields = ['id', 'classes_name']

class ManagementUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagementUnit
        fields = ['id', 'management_unit_name']

class CurrentGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrentGrade
        fields = ['id', 'current_grade']

class ChangeOfGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChangeOfGrade
        fields = ['id', 'grade']


# all fields under the User Model

# serializers.py
from rest_framework import serializers


class UserFieldsSerializer(serializers.Serializer):
    field_name = serializers.CharField()
    field_type = serializers.CharField()
    choices = serializers.ListField(child=serializers.ListField(), required=False)


