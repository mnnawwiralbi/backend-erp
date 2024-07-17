from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response


class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data.get('acces')
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"Logout": refresh_token}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"Logout": "failed"}, status=status.HTTP_400_BAD_REQUEST)
