# 序列化文件

from rest_framework import serializers
from .models import Course
from django.contrib.auth.models import User


class CourseSerializer(serializers.ModelSerializer):  # 序列化course 表
    teacher = serializers.ReadOnlyField(source='teacher.username')  # 外键字段，只读

    class Meta:
        model = Course
        # exclude = ('id',) # 排除的字段
        # fields = ('name','price','teacher','introduction')
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):  # 序列化user表
    class Meta:
        model = User
        fields = '__all__'

