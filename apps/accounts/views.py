from random import randint
from django.core.cache import caches
from django.conf import settings
from rest_framework import status
from rest_framework.generics import get_object_or_404, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from .serializer import UserProfileSerializer
from .tasks import send_verify_code
from redis import StrictRedis
from django.core.exceptions import ValidationError
from .models import UserProfile
from rest_framework.views import APIView
from django.utils.connection import ConnectionProxy

cache = ConnectionProxy(caches, "accounts")
redis_client = StrictRedis.from_url(settings.CACHES['accounts']['LOCATION'])


class LoginAndVerifyAPIView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'account/login.html'

    @staticmethod
    def code_generator():
        return str(randint(100000, 999999))

    @staticmethod
    def get_time_to_expire(email):
        return redis_client.ttl(f':1:{email}')


    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        assert email, "Email field must be set !"

        code = request.data.get("code")
        assert code, "Code field must be set !"

        if cache.get(email) != code:
            raise ValidationError("verification code has been expired or incorrect!")
        cache.delete(email)

        user, created = UserProfile.objects.get_or_create(email=email)

        refresh = RefreshToken.for_user(user)
        access_token = AccessToken.for_user(user)

        response = Response({'access': str(access_token), 'refresh': str(refresh)},
                            status=status.HTTP_202_ACCEPTED)
        response['Authorization'] = f'Bearer {access_token}'
        return response


    def patch(self, request, *args, **kwargs):
        email = request.data.get("email")
        assert email, "Email field must be set !"

        if (ttl := self.get_time_to_expire(email)) > 0:
            return Response({'expire': ttl}, status=status.HTTP_403_FORBIDDEN)
        code = self.code_generator()
        send_verify_code.delay(email, code)
        print(code)
        cache.set(email, code, 180)

        return Response(status=status.HTTP_200_OK)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get("refresh_token")
        access_token = request.data.get("access_token")
        if refresh_token:
            try:
                RefreshToken(refresh_token).blacklist()
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


        response = Response({"message": "Successfully logged out"}, status=status.HTTP_200_OK)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')

        return response

class UserUpdateAPIView(UpdateAPIView):
    queryset = UserProfile.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'account/profile.html'

    def get(self, request, *args, **kwargs):
        instance = get_object_or_404(UserProfile, id=request.user.id)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
