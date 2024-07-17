from rest_framework import serializers
from django.contrib.auth.models import User


class accountserelizers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']


class AccountSerializerRegisterSuperUser(serializers.ModelSerializer):
    class Meta:
        model = User
        # Tambahkan field lain yang diperlukan
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        user = User.objects.create_superuser(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
