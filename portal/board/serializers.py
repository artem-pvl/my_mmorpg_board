from rest_framework import serializers

from .models import Category, Ad, Reply, News


class NewsSerializer(serializers.ModelSerializer):
    user_id = serializers.EmailField(source='user_id.email')

    class Meta:
        model = News
        fields = ['id', 'user_id', 'header', 'creation_time']


class NewsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'


class AdListSerializer(serializers.ModelSerializer):
    user_id = serializers.EmailField(source='user_id.email')
    category_id = serializers.CharField(source='category_id.name')

    class Meta:
        model = Ad
        fields = ['id', 'user_id', 'category_id', 'header', 'creation_time']
