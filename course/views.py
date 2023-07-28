"""
用django写接口
"""
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

course_dict = {
    'name': '课程名称',
    'introduction': '课程介绍',
    'price': 3.11
}


# 使用Django 原生的FBV编写API接口
@csrf_exempt  # 对于post请求需要用该装饰器来解决csrf问题
def course_list(request):
    if request.method == "GET":
        # return HttpResponse(json.dumps(course_dict),content_type='application/json')
        # 上面的return 的HttpResponse 和下面 JsonResponse 返回的内容是一样的，显然下面更方便
        return JsonResponse(course_dict)
    if request.method == "POST":
        # 解析传参的数据，解码成utf-8格式
        course = json.loads(request.body.decode('utf-8'))
        # return HttpResponse(json.dumps(course),content_type='application/json')
        return JsonResponse(course, safe=False)  # 当传参是字符串的时候，需要设置safe=False


# 使用 Django原生的CBV来编写API接口,思路是对于不同的请求方法使用不同的函数处理
from django.views import View


class CourseList(View):
    def get(self, request):
        return JsonResponse(course_dict)

    @csrf_exempt
    def post(self, request):
        course = json.loads(request.body.decode('utf-8'))
        return JsonResponse(course, safe=False)  # 当传参是字符串的时候，需要设置safe=False


"""
使用rest_framework
"""
# 函数式编程：Function Based View （FBV)
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Course
from .serializer import CourseSerializer


@api_view(["GET", "POST"])
def course_list_drf_fbv(request):
    """
    获取所有课程或者新增一个课程
    :param request:
    :return:
    """
    if request.method == 'GET':
        res = CourseSerializer(instance=Course.objects.all(), many=True)  # many=true表示序列化几个对象，多个需要写，一个就不需要了
        return Response(data=res.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':

        req = CourseSerializer(data=request.data,
                               partial=True)  # 1、partial=True 表示可以部分更新，但是仅针对在数据库构造时的非必填字段；2、这里要用request.data
        # req是前端传过来的数据，我们需要对这个数据进行校验
        if req.is_valid():
            req.save(teacher=request.user)
            return Response(data=req.data, status=status.HTTP_201_CREATED)
        return Response(req.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def course_detail_drf_fbv(request, primary_key):
    """
    获取、更新、删除一个课程
    :param request:
    :param primary_key:
    :return:
    """
    # 先获取到primary_key对应的课程，然后需要对课程是否存在进行判断
    try:
        course_info = Course.objects.get(pk=primary_key)
    except Course.DoesNotExist:
        return Response(data={"msg": "无此课程信息"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        if request.method == 'GET':
            res = CourseSerializer(instance=course_info)
            return Response(data=res.data, status=status.HTTP_200_OK)
        if request.method == 'PUT':
            res = CourseSerializer(instance=course_info, data=request.data)
            if res.is_valid():
                res.save()
            return Response(data=res.data, status=status.HTTP_200_OK)

        if request.method == 'DELETE':
            course_info.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


# 2. 类视图编程 Classed Based View （CBV）
from rest_framework.views import APIView


class CourseListCBV(APIView):
    def get(self, request):
        """
         查看课程信息
        :param request:
        :return:
        """
        query_set = Course.objects.all()
        res = CourseSerializer(instance=query_set, many=True)
        a = res.data# instance是查询出来的数据
        return Response(data=res.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        新增课程信息
        :param request:
        :return:
        """
        req = CourseSerializer(data=request.data)
        if req.is_valid():
            req.save(teacher=self.request.user)
            return Response(data=req.data, status=status.HTTP_201_CREATED)  # data 是前端传过来的数据，需要进行is_valid校验
        return Response(data=req.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseDetailCBV(APIView):

    # 用一个通用的方法处理获取的实例对象
    def get_object(self, pk):
        try:
            course_info = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return None
        else:
            return course_info

    def get(self, request, pk):
        course_info = self.get_object(pk)
        if not course_info:
            return Response(data={"msg": "无此课程信息"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            res = CourseSerializer(instance=course_info)
            return Response(data=res.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        course_info = self.get_object(pk)
        if not course_info:
            return Response(data={"msg": "无此课程信息"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            req = CourseSerializer(instance=course_info, data=request.data)
            if req.is_valid():
                req.save()
                return Response(data=req.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        course_info = self.get_object(pk)
        if not course_info:
            return Response(data={"msg": "无此课程信息"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            course_info.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


# 3. 通用类视图编程 Generic Classed Based View （GCBV）
from rest_framework import generics


class CourseListGCBV(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    # 由于我们要自定义传入信息，所以重写一下create里面的函数
    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)


class CourseDetailGCBV(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


# 4. DRF视图集 viewsets
from rest_framework import viewsets


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)


"""
用信号方式生成用户token
"""
from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(signal=post_save,sender = settings.AUTH_USER_MODEL)  # django的信号机制
def generate_token(sender,instance=None,created=False,**kwargs):
    """
    创建用户时生成token
    当新增一个用户需要保存的时候，post_save方法会通知receiver，然后receiver会执行下面的generate_token 方法
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    if created:
        Token.objects.create(user=instance)
