"""
URL configuration for muke_20230724 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from rest_framework.authtoken import views
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls

schema_view = get_schema_view(title ="Drf Api 文档",description='描述')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),  # drf 的登录退出
    path('course/', include('course.urls')),  # drf 接口

    # 获取新注册用户token
    path('api-token-auth/',views.obtain_auth_token),
    # 方法1：注册api文档路由
    path('schema/',schema_view),
    # 方法2：注册api文档路由
    path('doc/',include_docs_urls(title="drf api doc",description='restfromwork 快速入门')),



]
