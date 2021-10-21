from django.db import models

# Create your models here.

# 主頁_輪播圖1
class Wheel(models.Model):
    img = models.CharField(max_length=150)
    name = models.CharField(max_length=20)
    trackid = models.CharField(max_length=20)
    isDelete = models.BooleanField(default=False)

# 主頁_小圖示
class Nav(models.Model):
    img = models.CharField(max_length=150)
    name = models.CharField(max_length=20)
    trackid = models.CharField(max_length=20)
    isDelete = models.BooleanField(default=False)

# 主頁_輪播圖2
class Discount(models.Model):
    img = models.CharField(max_length=150)
    name = models.CharField(max_length=20)
    trackid = models.CharField(max_length=20)
    isDelete = models.BooleanField(default=False)

# 主頁_每日發現
class NewFind(models.Model):
    img = models.CharField(max_length=150)
    name = models.CharField(max_length=150)
    trackid = models.CharField(max_length=20)
    isDelete = models.BooleanField(default=False)

# 超市_大分類與其子類ID
class ProductTypes(models.Model):
    typeId = models.CharField(max_length=10)
    typeName = models.CharField(max_length=12)
    img = models.CharField(max_length=150)
    childType = models.CharField(max_length=500)
    typeSort = models.IntegerField()
    isDelete = models.BooleanField(default=False)

# 超市_商品
class Products(models.Model):
    productId = models.CharField(max_length=10) # productId: 11708405
    productName = models.CharField(max_length=100)   # productName: 【CHING'S獨家】超顯瘦彈性極佳中高腰黑褲 長褲 S-2XL 黑釦真拉鍊前後口袋 黑褲 女裝 褲子
    productImg = models.CharField(max_length=150)   # productImg: https://cf.shopee.tw/file/2a684c81589bb509d79dec9c3e5bbee1_tn
    discountPrice = models.IntegerField() # discountPrice: 29900000(須 除以100000)
    originalPrice = models.IntegerField() # originalPrice: 0(若此商品無打折，此值為0)
    categoryId = models.CharField(max_length=10)    # (大分類)categoryId: 11040766
    childId = models.CharField(max_length=10)   # (子類)childId: 11042304
    childName = models.CharField(max_length=10) # (子類名稱)childName: T恤
    shopLocation = models.CharField(max_length=10)  # (出貨地點)shopLocation: 臺北市南港區
    sales = models.IntegerField() # (目前銷量)sales: 67741
    hot = models.FloatField()   # (熱門?星星)hot: 4.95
    inventory = models.IntegerField()   # inventory庫存
    isdelete = models.BooleanField(default=False)   # 邏輯刪除


class Users(models.Model):
    userAccount = models.CharField(max_length=20, unique=True)
    userPasswd = models.CharField(max_length=20)
    userNickName = models.CharField(max_length=20)
    userPhone = models.CharField(max_length=20)
    userAddress = models.CharField(max_length=100)
    userImg = models.CharField(max_length=150)
    userRank = models.IntegerField()
    # 每次登入後，亂數更新，確認是否 是同一個session
    userToken = models.CharField(max_length=50)

    @classmethod
    def createUser(cls, account, passwd, nickname, phone, address, img, rank, token):
        newUser = cls(userAccount=account, userPasswd=passwd, userNickName=nickname, userPhone=phone, userAddress=address, userImg=img, userRank=rank, userToken=token)
        return newUser



class CartsManager1(models.Manager):
    def get_queryset(self):
        return super(CartsManager1, self).get_queryset().filter(isDelete=False)

class CartsManager2(models.Manager):
    def get_queryset(self):
        return super(CartsManager2, self).get_queryset().filter(isDelete=True)

class Carts(models.Model):
    userAccount = models.CharField(max_length=20)
    productId = models.CharField(max_length=10)
    productNum = models.IntegerField()
    totalPrice = models.IntegerField()
    isChoose = models.BooleanField(default=True)
    productImg = models.CharField(max_length=150)
    productName = models.CharField(max_length=100)
    orderId = models.CharField(max_length=20, default='0')
    isDelete = models.BooleanField(default=False)

    objects1 = CartsManager1()
    objects2 = CartsManager2()

    @classmethod
    def createCart(cls, userAccount, productId, productNum, totalPrice, isChoose, productImg, productName, orderId, isDelete):
        newCart = cls(userAccount=userAccount, productId=productId, productNum=productNum, totalPrice=totalPrice, isChoose=isChoose, productImg=productImg, productName=productName, orderId=orderId, isDelete=isDelete)
        return newCart




class Orders(models.Model):
    orderId = models.CharField(max_length=20)
    userId = models.CharField(max_length=20)
    progress = models.IntegerField()
    isDelete = models.BooleanField(default=False)

    @classmethod
    def createOrder(cls, orderId, userId, progress, isDelete):
        newOrder = cls(orderId=orderId, userId=userId, progress=progress, isDelete=isDelete)
        return newOrder




class Test(models.Model):
    test1 = models.FloatField()
