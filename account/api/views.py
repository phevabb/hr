from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from rest_framework import generics
from rest_framework.views import APIView
from .ses import PasswordResetSerializer
from django.contrib.auth import get_user_model
from .ses import UserLoginSerializer, ChangePasswordSerializer, PasswordResetSerializer, PasswordResetConfirmSerializer
from rest_framework.permissions import AllowAny
from rest_framework import generics, status
from django.core.exceptions import ObjectDoesNotExist
User = get_user_model()
 

class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, uidb64, token, *args, **kwargs):
        data = {
            "uid": uidb64,
            "token": token,
            "new_password": request.data.get("new_password"),
        }
        serializer = PasswordResetConfirmSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail": "Password has been reset successfully."},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class UserLoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        token, created = Token.objects.get_or_create(user=user)

        # Base user data
        user_data = {
            "id": user.id,
            "role": user.role,
            "full_name": user.full_name,
            "user_id": getattr(user, 'user_id', None),  # Handle if user_id is optional
        }

        # Region mapping
        REGION_CHOICES = [
            'AHAFO', 'ASHANTI', 'BONO & BONO EAST', 'CENTRAL', 'EASTERN',
            'GREATER ACCRA', 'HEAD OFFICE', 'NORTHERN', 'UPPER EAST',
            'WESTERN', 'Greater Accra', 'WESTERN NORTH'
        ]

        if user.role == "Manager":
            if not hasattr(user, "manager_profile") or not user.manager_profile:
                return Response(
                    {"error": "Manager profile not found. Please contact Head Office to assign you a region."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if not user.manager_profile.region:
                return Response(
                    {"error": "Manager profile not found. Please contact Head Office to assign you a region."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            region_name = user.manager_profile.region

            try:
                region_id = REGION_CHOICES.index(region_name.upper()) + 1  # Case-insensitive match
            except ValueError:
                return Response(
                    {"error": f"Invalid region: {region_name} not in REGION_CHOICES."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user_data["region"] = region_name
            user_data["region_id"] = region_id

        response_data = {
            "token": token.key,
            "user": user_data,
        }

        return Response(response_data, status=status.HTTP_200_OK)



class UserLogoutView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, *args, **kwargs):
        Token.objects.filter(user=request.user).delete()
        return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': "Password changed successfully"}, status=status.HTTP_200_OK)

        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
        )






class PasswordResetView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            try:
                result = serializer.save(request)
                return Response(result, status=status.HTTP_200_OK)
            except Exception as e:
                return Response(
                    {"detail": "An error occurred while processing your request."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)