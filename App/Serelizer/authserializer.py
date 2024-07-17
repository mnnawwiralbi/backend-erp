from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status


class AuthSerializer (serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']


class AuthFormSerializerUsername(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def create(self, validated_data):
        return validated_data

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError({
                'refresh': 'error',
                'access': 'error',
                'user_id': 'error',
                'message': 'failed',
                'status': status.HTTP_400_BAD_REQUEST
            })

        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        return {
            'refresh': str(refresh),
            'access': str(access_token),
            'user_id': user.id,
            'message': 'Success',
            'status': status.HTTP_200_OK
        }


class AuthFormSerializerEmail(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def create(self, validated_data):
        return validated_data

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        try:
            # Verifikasi user berdasarkan email
            user = User.objects.get(email=email)

            if user.check_password(password):
                # Generate token menggunakan RefreshToken
                refresh = RefreshToken.for_user(user)
                access_token = refresh.access_token

                return {
                    'refresh': str(refresh),
                    'access': str(access_token),
                    'user_id': user.id,
                    'message': 'Success',
                    'status': status.HTTP_200_OK
                }

            else:
                raise serializers.ValidationError({
                    'refresh': 'error',
                    'access': 'error',
                    'user_id': 'error',
                    'message': 'failed',
                    'status': status.HTTP_400_BAD_REQUEST
                })
        except User.DoesNotExist:
            raise serializers.ValidationError({
                'refresh': 'error',
                'access': 'error',
                'user_id': 'error',
                'message': 'failed',
                'status': status.HTTP_400_BAD_REQUEST
            })
