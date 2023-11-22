from rest_framework.views import APIView
from .serializers import UserSignUpSerializer
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
import datetime
import random
from config.celery import sent_otp
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
class UserSignupView(APIView):
    @swagger_auto_schema(request_body=UserSignUpSerializer)
    def post(self, request):
        serializer = UserSignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": "otp is send please check", "user_id": user.id},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyUser(APIView):
    def patch(self, request, pk):
        data = request.data
        otp = data.get("otp")
        user = MyUser.objects.get(pk=pk)
        if (
            int(user.otp) == otp
            and timezone.now() < user.otp_expiry
            and user.otp_max_try >= 1
            and user.is_active == False
        ):
            user.otp_max_try = 3
            user.otp_expiry = None
            user.otp_max_out = None
            user.is_active = True
            user.save()
            token = get_tokens_for_user(user=user)

            return Response(
                {
                    "message": "user is activated",
                    "access": token["access"],
                    "refresh": token["refresh"],
                }
            )

        else:
            return Response(
                {"error": "otp is not valid or user active or you are in blocking time"}
            )

class ReGenerateCode(APIView):
    def post(self, request):
        user_id = request.data.get("user_id")

        try:
            user = MyUser.objects.get(id=user_id)
        except ObjectDoesNotExist:
            return Response({"error": "User with the provided ID does not exist"}, status=status.HTTP_404_NOT_FOUND)

        if user.otp_max_out and user.otp_max_out > timezone.now():
            return Response({"message": "You are in block"})

        if user.otp_max_try < 1:
            user.otp_max_out = timezone.now() + datetime.timedelta(minutes=60)
            user.save()
            return Response({"message": "You are blocked"})

        user.otp_max_try -= 1
        otp = random.randint(1000, 9999)
        user.otp = otp
        user.otp_expiry = timezone.now() + datetime.timedelta(minutes=5)
        user.save()

        subject = "Verify your email address"
        sent_otp.delay(otp, user.email, subject)

        return Response({"message": "Regenerated code is send"})