from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from App.utils.tokenjwt import create_access_token, create_refresh_token
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenObtainSerializer
from App.Serelizer.accountserelizer import AccountSerializer
from App.Serelizer.authserializer import AuthFormSerializerEmail, AuthFormSerializerUsername


class AuthUsername (APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        userauth = authenticate(username=username, password=password)
        if userauth:

            access = create_access_token(userauth.id)
            refresh = create_refresh_token(userauth.id)

            try:
                token = Token.objects.get(user=userauth)
                token.key = access
                token.save()
            except Token.DoesNotExist:
                Token.objects.create(user=userauth, key=access)

            return Response({'access': access, 'refresh': refresh, 'user_id': userauth.id, 'message': 'Success'}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'error': 'Invalid credentials', 'message': 'Failed'}, status=status.HTTP_406_NOT_ACCEPTABLE)


class authis (APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        try:
            if User.objects.get(email=request.data.get('email')) and User.objects.get(password=request.data.get('password')):
                userauth = User.objects.get(email=request.data.get('email'))
                access = create_access_token(userauth.id)
                refresh = create_refresh_token(userauth.id)
                try:
                    token = Token.objects.get(user=userauth)
                    token.key = access
                    token.save()
                except Token.DoesNotExist:
                    Token.objects.create(user=userauth, key=access)
                return Response({'access': access, 'refresh': refresh, 'user_id': userauth.id, 'message': 'Success'}, status=status.HTTP_202_ACCEPTED)
        except:
            return Response({'error': 'Invalid credentials', 'message': 'Failed'}, status=status.HTTP_406_NOT_ACCEPTABLE)


class Logins (APIView):

    permission_classes = [AllowAny]
    # metode login

    def post(self, request):
        if request.method == 'POST':
            # menampung nilai
            nama = str(request.POST.get('username'))
            pw = str(request.POST.get('password'))
            try:
                user = User.objects.get(email=nama)
                password_check = user.check_password(pw)
                username = user.get_username()

                if (password_check):
                    access = create_access_token(username)
                    refresh = create_refresh_token(username)
                    try:
                        token = Token.objects.get(user=user)
                        token.key = access
                        token.save()
                    except:
                        Token.objects.create(user=user, key=access)
                    return Response({'access': access, 'refresh': refresh, 'user_id': username, 'message': 'Success'}, status=status.HTTP_202_ACCEPTED)
            except:
                return Response({'message': 'Failed'}, status=status.HTTP_400_BAD_REQUEST)


class LoginAuthToken(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        if request.method == 'POST':
            nama = request.data.get('email')
            pw = request.data.get('password')

            if not nama or not pw:
                return Response({'message': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                user = User.objects.get(email=nama)
            except User.DoesNotExist:
                return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

            if not user.check_password(pw):
                return Response({'message': 'Incorrect password'}, status=status.HTTP_401_UNAUTHORIZED)

            username = user.get_username()

            access = create_access_token(username)
            refresh = create_refresh_token(username)

            userauth = authenticate(username=username, password=pw)

            try:
                token = Token.objects.get(user=userauth)
                token.key = access
                token.save()
            except Token.DoesNotExist:
                Token.objects.create(user=user, key=access)

            return Response({'access': access, 'refresh': refresh, 'user_id': userauth.id, 'message': 'Success'}, status=status.HTTP_202_ACCEPTED)


class LoginSimpleJwtTokenObtain (APIView):

    permission_classes = [AllowAny]
    # metode login

    def post(self, request):
        if request.method == 'POST':
            # menampung nilai
            nama = str(request.data.get('email'))
            pw = str(request.data.get('password'))

            try:

                user = User.objects.get(email=nama)
                password_check = user.check_password(pw)
                username = user.get_username()

                # serializer
                serializer = AccountSerializer(data=user)

                if (password_check):

                    # access = create_access_token(username)
                    # refresh = create_refresh_token(username)
                    # return Response({'access': access, 'refresh': refresh, 'user_id': username, 'message': 'Success'}, status=status.HTTP_202_ACCEPTED)

                    tokenobtain = TokenObtainSerializer(serializer)

                    tokenpair = TokenObtainPairSerializer(tokenobtain)

                    return Response({'obtain': tokenobtain.data, 'pair': tokenpair.default_validators, 'user_id': username, 'message': 'Success'}, status=status.HTTP_202_ACCEPTED)

                return Response({'message': 'Incorrect password'}, status=status.HTTP_401_UNAUTHORIZED)
            except:
                return Response({'message': 'Failed'}, status=status.HTTP_400_BAD_REQUEST)


class LoginSimpleJwtRefreshToken(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        if request.method == 'POST':
            # menampung nilai
            email = request.data.get('email')
            password = request.data.get('password')

            try:
                # Verifikasi user berdasarkan email
                user = User.objects.get(email=email)

                if user.check_password(password):
                    # Generate token menggunakan RefreshToken
                    refresh = RefreshToken.for_user(user)
                    access_token = refresh.access_token

                    return Response({
                        'refresh': str(refresh),
                        'access': str(access_token),
                        'user_id': user.id,
                        'message': 'Success'
                    }, status=status.HTTP_202_ACCEPTED)
                else:
                    return Response({'message': 'Incorrect password'}, status=status.HTTP_401_UNAUTHORIZED)

            except User.DoesNotExist:
                return Response({'message': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)


class AuthSerializerFormEmail(APIView):
    serializer_class = AuthFormSerializerEmail
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data)
        return Response(serializer.errors, status=400)


class AuthSerializerFormUsername(APIView):
    serializer_class = AuthFormSerializerUsername
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data)
        return Response(serializer.errors, status=400)
