from django.urls import path, include
from course import views

from rest_framework.routers import DefaultRouter



router = DefaultRouter()
router.register(prefix='viewsets', viewset=views.CourseViewSet)  # prefix是路由的前缀，viewset是具体的实例方法

urlpatterns = [
    # Function Based View （FBV)
    path('fbv/list/', views.course_list_drf_fbv, name='fbvlist'),
    path('fbv/detail/<int:primary_key>/', views.course_detail_drf_fbv, name='fbvdetail'),

    # 2. 类视图编程 Classed Based View （CBV）
    path('cbv/list/', views.CourseListCBV.as_view(), name='cbvlist'),
    path('cbv/detail/<int:pk>/', views.CourseDetailCBV.as_view(), name='cbvdetail'),

    # 3.通用类视图编程 Generic Classed Based View （GCBV）
    path('gcbv/list/', views.CourseListGCBV.as_view(), name='gcbvlist'),
    path('gcbv/detail/<int:pk>/', views.CourseDetailGCBV.as_view(), name='gcbvdetail'),

    # 4. DRF视图集 viewsets
    # 传统方法：
    # path('viewsets/',views.CourseViewSet.as_view(
    #     {'get':'list','post':'create'}
    # ),name = 'viewsets'),
    # path('viewsets/<int:pk>/',views.CourseViewSet.as_view(
    #     {'get':'retrieve','put':'update','patch':'partial_update','delete':'destroy'}
    # ),name = 'viewsets'),
    # 另一个注册方法
    path('', include(router.urls))


]
