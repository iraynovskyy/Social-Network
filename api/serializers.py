from rest_framework import serializers
from .models import Post
from django.contrib.auth.models import User



class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'likes', 'dislikes']
