from rest_framework import serializers  # type: ignore
from django.contrib.auth import get_user_model  # type: ignore

from posts.models import Comment, Post, Group, Follow

User = get_user_model()


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)

    class Meta:
        model = Post
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'post', 'created')


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    following = serializers.SlugRelatedField(
        slug_field='username', queryset=User.objects.all()
    )

    class Meta:
        model = Follow
        fields = ('user', 'following')

    def validate(self, data):
        request_user = self.context['request'].user
        following_user = data.get('following')

        if request_user == following_user:
            raise serializers.ValidationError({
                'following': ['Нельзя подписаться на самого себя!']
            })

        if Follow.objects.filter(
                user=request_user,
                following=following_user).exists():
            raise serializers.ValidationError({
                'following': ['Вы уже подписаны на этого пользователя!']
            })

        return data

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
