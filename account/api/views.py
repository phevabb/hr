from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .ses import UserLoginSerializer, ChangePasswordSerializer, PasswordResetSerializer, PasswordResetConfirmSerializer
from rest_framework.permissions import AllowAny
User = get_user_model()
 

class PasswordResetConfirmView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Password has been reset successfully."}, status=status.HTTP_200_OK)
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
            "user_id": user.user_id,
        }

        # Region mapping
        REGION_CHOICES = [
            'AHAFO', 'ASHANTI', 'BONO & BONO EAST', 'CENTRAL', 'EASTERN', 
            'GREATER ACCRA', 'HEAD OFFICE', 'NORTHERN', 'UPPER EAST', 
            'WESTERN', 'Greater Accra', 'WESTERN NORTH'
        ]

        if user.role == "Manager":
            region_name = None
            region_id = None
            if hasattr(user, "manager_profile") and user.manager_profile.region:
                region_name = user.manager_profile.region
                # Use index in REGION_CHOICES as a pseudo-ID
                region_id = REGION_CHOICES.index(region_name) + 1

            user_data["region"] = region_name
            user_data["region_id"] = region_id

        return Response(
            {
                "token": token.key,
                "user": user_data,
            },
            status=status.HTTP_200_OK,
        )

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
    def post(self, request, *args, **kwargs):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(request)
            return Response({"detail": "Password reset link sent."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
