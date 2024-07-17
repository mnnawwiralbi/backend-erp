from rest_framework import serializers
from App.models import Article


class ArticelSerelizer (serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'
