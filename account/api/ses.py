from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

User = get_user_model()


class PasswordResetConfirmSerializer(serializers.Serializer):
    uidb64 = serializers.CharField()
    token = serializers.CharField()
    new_password1 = serializers.CharField(write_only=True, min_length=8)
    new_password2 = serializers.CharField(write_only=True, min_length=8)

    def validate(self, attrs):
        uidb64 = attrs.get("uidb64")
        token = attrs.get("token")
        password1 = attrs.get("new_password1")
        password2 = attrs.get("new_password2")

        # Check if passwords match
        if password1 != password2:
            raise serializers.ValidationError({"password": "Passwords do not match."})

        # Decode user
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError({"uidb64": "Invalid user ID."})

        # Validate token
        if not default_token_generator.check_token(user, token):
            raise serializers.ValidationError({"token": "Invalid or expired token."})

        # Attach user for later use
        attrs["user"] = user
        return attrs

    def save(self, **kwargs):
        password = self.validated_data["new_password1"]
        user = self.validated_data["user"]
        user.set_password(password)
        user.save()
        return user

class UserLoginSerializer(serializers.Serializer):
    staff_department = serializers.CharField(
    required=True,
    allow_blank=False,
    error_messages={
        "blank": "Choose a department",
        "required": "Department is required"
    }
)

    password = serializers.CharField(
    required=True,
    min_length=8,
    max_length=128,
    style={'input_type': 'password'},
    trim_whitespace=True,
    error_messages={
        "blank": "Password cannot be empty",
        "required": "Password is required",
        "min_length": "Password must be at least 8 characters long",
        
    }
)

    user_ID = serializers.CharField(required=True)

    def validate(self, attrs):
        staff_department = attrs.get('staff_department')
        password = attrs.get('password')
        user_ID = attrs.get('user_ID')
       
        

        if not user_ID or not password:
            raise serializers.ValidationError('Password and user id are required')
        if not staff_department:
            raise serializers.ValidationError('Choose a department')

        user = authenticate(user_id=user_ID, password=password)
        if not user:
            raise serializers.ValidationError('Invalid credentials')
        
        if staff_department not in ['Admin', 'Manager', 'Staff']:
            raise serializers.ValidationError("Select a valid department")
        
        
        if user.role != staff_department:
            raise serializers.ValidationError("Select Appropraite department")


        if not user.is_active:
            raise serializers.ValidationError('Your account is disabled')
        attrs['user'] = user
        return attrs



class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)


    def validate_old_password(self, value):
        user =  self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is not correct")
        return value
    
    def validate(self, attrs):
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')

        if new_password != confirm_password:
            raise serializers.ValidationError("New password and confirm password do not match")
        
        validate_password(new_password)
        return attrs
    
    def save(self, **kwargs):
        user = self.context['request'].user
        new_password = self.validated_data['new_password']
        user.set_password(new_password)
        user.save()
        return user





class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("No account is associated with this email address.")
        self.user = user
        return value

    def save(self, request):
        user = self.user
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        # Construct reset link (frontend should handle actual reset form)
        #  https://phevab1.pythonanywhere.com/
        reset_url = f"http://localhost:8080/password-reset-confirm/{uid}/{token}/"

        # Send email to the same user email stored in DB
        user.email_user(
            subject="Password Reset Request",
            message=f"Hi {user.first_name},\n\n"
                    f"We received a request to reset your password. "
                    f"Click the link below to reset it:\n\n{reset_url}\n\n"
                    f"If you didn’t request this, you can ignore this email.",
        )

        return {"detail": "Password reset link has been sent to your email."}


         