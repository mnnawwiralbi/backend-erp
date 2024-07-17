from rest_framework import serializers
from App.models import ReviewUser


class ReviewSerializer (serializers.ModelSerializer):
    class Meta:
        model = ReviewUser
        fields = '__all__'
