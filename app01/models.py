from django.db import models

class Admin(models.Model):
    name = models.CharField(verbose_name="用户名",max_length=32)
    password = models.CharField(verbose_name="密码",max_length=64)

    def __str__(self):
        return self.name

class Department(models.Model):
    title = models.CharField(max_length=32)

    def __str__(self):
        return self.title

class UserInfo(models.Model):
    name = models.CharField(max_length=32,verbose_name="姓名")
    password = models.CharField(max_length=64,verbose_name="密码")
    age = models.IntegerField(verbose_name="年龄",default=2)
    acount = models.DecimalField(verbose_name="账户额度",max_digits=10,decimal_places=2,default=0)
    create_time = models.DateTimeField(verbose_name="入职时间")
    depart = models.ForeignKey(verbose_name="部门ID",to="Department",to_field="id",on_delete=models.CASCADE)
    gender_choices = (
        (1,"男"),
        (2,"女"),
    )
    gender = models.SmallIntegerField(verbose_name="性别",choices=gender_choices)


class PrettyNum(models.Model):
    mobile = models.CharField(verbose_name="手机号",max_length=11)
    price = models.IntegerField(verbose_name="价格",default=0)
    level_choices=(
        (1, "1级"),
        (2, "2级"),
        (3, "3级"),
        (4, "4级"),
    )
    level = models.SmallIntegerField(verbose_name="级别",choices=level_choices,default=1)
    status_choices = (
        (1,"未占用"),
        (2,"已占用"),
    )
    status = models.SmallIntegerField(verbose_name="状态",choices=status_choices,default=1)


class task(models.Model):
    level_choice = (
        (1,"紧急"),
        (2,"重要"),
        (3,"临时"),
    )
    level = models.SmallIntegerField(verbose_name="级别",choices=level_choice,default=1)
    title = models.CharField(verbose_name="标题",max_length=64)
    datail = models.TextField(verbose_name="详细信息")
    user = models.ForeignKey(verbose_name="负责人",to="Admin",on_delete=models.CASCADE)


class Order(models.Model):
    """ 订单 """
    oid = models.CharField(verbose_name="订单号",max_length=64,null=False)
    title = models.CharField(verbose_name="商品名称",max_length=32)
    price = models.IntegerField(verbose_name="价格")
    status_choices = (
        (1,"待支付"),
        (2,"已支付"),
    )
    status = models.SmallIntegerField(verbose_name="状态",choices=status_choices,default=1)
    user = models.ForeignKey(verbose_name="管理员",to="Admin",on_delete=models.CASCADE)


class Boss(models.Model):
    """ 老板信息 """
    name = models.CharField(verbose_name="姓名",max_length=32)
    age = models.IntegerField(verbose_name="年龄")
    imgs = models.CharField(verbose_name="头像",max_length=128)


class City(models.Model):
    """ 城市 """
    name = models.CharField(verbose_name="名称",max_length=32)
    count = models.IntegerField(verbose_name="人口")
    # 本质上数据库也是CharField类型，可自动保存文件数据。upload_to 指的是将文件存放在media下的city文件夹中
    imgs = models.FileField(verbose_name="Logo",max_length=128,upload_to="city/")

