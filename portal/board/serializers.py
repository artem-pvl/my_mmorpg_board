from django.db.models import fields
from rest_framework import serializers

from .models import Category, Ad, Reply, News


class NewsSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user_id = serializers.DjangoModelField()
    header = serializers.CharField(required=True, allow_blank=False,
                                   max_length=255)
    news = serializers.CharField(required=True, allow_blank=False,
                                 style={'base_template': 'textarea.html'})
    creation_time = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return News.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.user = validated_data.get('user', instance.user)
        instance.header = validated_data.get('header', instance.header)
        instance.news = validated_data.get('news', instance.news)
        instance.save()

        return instance


class AdListSerializer(serializers.ModelSerializer):
    # ad_id = serializers.IntegerField()
    user_id = serializers.EmailField(source='user_id.email')
    category_id = serializers.CharField(source='category_id.name')
    header = serializers.CharField()
    # ad = serializers.CharField()
    creation_time = serializers.DateTimeField()

    class Meta:
        model = Ad
        fields = ['id', 'user_id', 'category_id', 'header', 'creation_time']
