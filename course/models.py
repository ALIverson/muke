from django.db import models
from django.conf import settings


# Create your models here.


class Course(models.Model):
    name = models.CharField(max_length=255, unique=True, help_text="课程名称", verbose_name='名称')
    introduction = models.CharField(max_length= 4096,help_text="课程简介", verbose_name='简介')
    price = models.DecimalField(max_digits=6, decimal_places=2, help_text='课程价格')
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, help_text="课程名称", verbose_name='讲师')
    create_time = models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, help_text='更新时间', verbose_name='更新时间')

    class Meta:
        verbose_name = '课程信息'
        verbose_name_plural = verbose_name
        ordering = ('price',)  # 这里之前报错要么用元组，要么用数组，但是用元组依然报错，改成数组可以了

    def __str__(self):
        return self.name
