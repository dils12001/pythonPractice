from django.db import models
from django.db.models import Model


class Users(models.Model):
    u_name = models.CharField(max_length=25,unique=True)
    u_password = models.CharField(max_length=30,unique=True)
    u_gender = models.BooleanField(default=True)
    u_age = models.IntegerField(default=5)
    #default屬性不管用
    u_isDelete = models.BooleanField(null=False, default=False, blank=False)

    #建立外鍵，引用Department的PK(id)
    u_dept = models.ForeignKey('Departments',on_delete=models.CASCADE,default=2)

    #print(Users對象) 時，就可以直接返回u_name
    def __str__(self):
        return self.u_name

    def fuctionTest(self):
        return str(self.u_name) + '此函式不能有self以外的參數'

    class Meta:
        #寫在定義該資料表的裡面
        #建立此資料表時，此資料表的名稱，系統預設為 專案名_類名
        db_table = "users"
        #對象獲取數據時會依該 欄位 進行排序，['id']升冪 ['-id']降冪
        #ordering = ['id']


class deptManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(d_isDelete = False)

class Departments(models.Model):
    #自定義django管理器
    #原本預設用 類名.object.方法() 如下 可以用 類名.deptObj.方法()
    #deptObj = models.Manager()
    #自定義使 deptObj2 取出的數據都為 d_isDelete = False
    deptObj2 = deptManager()

    d_name = models.CharField(max_length=25)
    d_description = models.CharField(max_length=20)
    d_createDate = models.DateTimeField()
    #default屬性不管用
    d_isDelete = models.BooleanField(null=False, default=False, blank=False)

    # print(Department對象) 時，就可以直接返回d_name
    def __str__(self):
        return self.d_name
    class Meta:
        db_table = "depts"

class UsersProfile(models.Model):
    img = models.ImageField(upload_to='headshots')
    user = models.OneToOneField(Users, on_delete=models.CASCADE)
    class Meta:
        db_table = "usersprofile"
