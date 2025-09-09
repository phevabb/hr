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
class UserFieldsSerializer(serializers.Serializer):
    field_name = serializers.CharField()
    field_type = serializers.CharField()
    choices = serializers.ListField(child=serializers.ListField(), required=False)

from rest_framework import serializers




class UserSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(required=False, allow_null=True)
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

    def validate_profile_picture(self, value):
        print(f'Profile picture received: {value}, Type: {type(value)}')  # Log received value and type
        if value and not hasattr(value, 'file'):
            print(f'Invalid profile_picture data: {value}')  # Log invalid data
            return None  # Treat invalid data as null to avoid validation error
        if value:
            print(f'File name: {value.name}, File size: {value.size}, Content type: {value.content_type}')  # Log file details
        return value

    def update(self, instance, validated_data):
        print(f'Validated data: {validated_data}')  # Log validated data
        instance = super().update(instance, validated_data)
        print(f'Updated profile_picture: {instance.profile_picture}')  # Log final field value
        return instance

    class Meta:
        model = User
        exclude = [
            'password', 'user_permissions', 'groups', 'last_login',
            'is_superuser', 'is_staff', 'is_active', 'date_joined'
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.change_of_grade:
            representation['change_of_grade'] = instance.change_of_grade.grade
        if instance.current_grade:
            representation['current_grade'] = instance.current_grade.current_grade
        if instance.next_grade:
            representation['next_grade'] = instance.next_grade.current_grade
        if instance.directorate:
            representation['directorate'] = instance.directorate.department_name
        if instance.category:
            representation['category'] = instance.category.classes_name
        if instance.district:
            representation['district'] = instance.district.district
        if instance.region:
            representation['region'] = instance.region.region
        if instance.management_unit_cost_centre:
            representation['management_unit_cost_centre'] = instance.management_unit_cost_centre.management_unit_name
        representation["age"] = instance.age
        representation["full_name"] = instance.full_name
        representation["date_of_retirement"] = instance.date_of_retirement
        return representation


    