from rest_framework import serializers

from .models import Category, Ad, Reply, News


class NewsSerializer(serializers.ModelSerializer):
    user_id = serializers.EmailField(source='user_id.email')

    class Meta:
        model = News
        fields = ['id', 'user_id', 'header', 'creation_time']


class NewsDetailSerializer(serializers.ModelSerializer):
    user_id = serializers.ReadOnlyField(source='user_id.email')

    class Meta:
        model = News
        fields = '__all__'


class AdListSerializer(serializers.ModelSerializer):
    user_id = serializers.EmailField(source='user_id.email')
    category_id = serializers.StringRelatedField()

    class Meta:
        model = Ad
        exclude = ['ad']


class AdDetailSerializer(serializers.ModelSerializer):
    user_id = serializers.EmailField(read_only=True, source='user_id.email')
    category_id = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Ad
        fields = '__all__'


class RepliesSerializer(serializers.ModelSerializer):
    user_id = serializers.EmailField(read_only=True, source='user_id.email')
    ad_id = serializers.SlugRelatedField(
        slug_field='header',
        queryset=Ad.objects.all()
    )

    class Meta:
        model = Reply
        fields = '__all__'


class AdFilterSerializer(serializers.ModelSerializer):
    user_id = serializers.EmailField(read_only=True, source='user_id.email')
    category_id = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Category.objects.all()
    )
    reply = RepliesSerializer(many=True, read_only=True)

    class Meta:
        model = Ad
        fields = ['user_id', 'category_id', 'header', 'creation_time',
                  'reply']
