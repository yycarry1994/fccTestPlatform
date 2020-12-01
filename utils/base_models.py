from django.db import models


class BaseModel(models.Model):
    """
    数据库表公共字段
    """
    # id = models.AutoField(primary_key=True, verbose_name='主键', help_text='主键')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="更新时间")

    class Meta:
        # 为抽象模型类, 用于其他模型来继承，数据库迁移时不会创建ModelBase表
        abstract = True
        verbose_name = "公共字段表"
        db_table = 'BaseModel'




