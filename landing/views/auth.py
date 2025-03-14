from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from landing.serializers import CustomUserSerializer
from landing.models import CustomUser, Company 
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt  # Disable CSRF protection for this endpoint
@api_view(["POST"])
@permission_classes([])  # Remove authentication requirement
def user_login(request):
    """
    Login a user using email or mobile number and password.
    """
    identifier = request.data.get("identifier")  # Email or mobile
    password = request.data.get("password")

    if not identifier or not password:
        return Response(
            {"error": "Identifier (email or mobile number) and password are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Determine whether the identifier is an email or mobile number
    try:
        validate_email(identifier)
        is_email = True
    except ValidationError:
        is_email = False

    if is_email:
        user = CustomUser.objects.filter(email=identifier).first()
    else:
        user = CustomUser.objects.filter(mobile_number=identifier).first()

    if user and user.check_password(password):
        user.last_login = timezone.now()
        user.save(update_fields=["last_login"])  # Update last login time
        
        refresh = RefreshToken.for_user(user)
        company_name = user.company.company_name if user.company else None
        return Response(
            {
                "token": str(refresh.access_token),
                "userData": CustomUserSerializer(user).data,
                "HotelData": company_name,
            },
            status=status.HTTP_200_OK,
        )

    return Response(
        {"error": "Invalid email/mobile number or password."},
        status=status.HTTP_401_UNAUTHORIZED,
    )


@api_view(["POST"])  # or ["GET"] if you're validating via GET request
@permission_classes([IsAuthenticated])  # 🔥 This ensures only authenticated users can access
def validate_token(request):
    return Response({"message": "Token is valid"}, status=200)
    
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def change_password(request):
    current_password = request.data.get("currentPassword")
    new_password = request.data.get("newPassword")
    confirm_password = request.data.get("confirmPassword")

    if not current_password or not new_password or not confirm_password:
        return Response(
            {"error": "All fields (currentPassword, newPassword, confirmPassword) are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = request.user
    if not user.check_password(current_password):
        return Response(
            {"error": "Current password is incorrect."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if new_password != confirm_password:
        return Response(
            {"error": "New password and confirm password do not match."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user.set_password(new_password)
    user.save()

    return Response(
        {"message": "Password changed successfully."},
        status=status.HTTP_200_OK,
    )