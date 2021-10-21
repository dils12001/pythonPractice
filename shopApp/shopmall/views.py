from django.shortcuts import render, redirect
from .models import Wheel, Nav, Discount, NewFind, ProductTypes, Products, Test, Users, Carts, Orders
from shopApp.settings import STATIC_URL
import time, random, os # 隨機生成token，及產生上傳檔案的路徑
import json
from django.core import serializers




# Create your views here.
def base(request):
    context = {
        'tittle':'base',
    }
    return render(request, 'shopmall/base.html', context=context)





def home(request):
    wheelsList = Wheel.objects.all()
    navList = Nav.objects.all()
    discountList = Discount.objects.all()
    newFindList = NewFind.objects.all()

    context = {
        'staticURL': STATIC_URL,
        'tittle': '首頁',
        'wheelsList': wheelsList,
        'navList': navList,
        'discountList': discountList,
        'newFindList': newFindList,
    }
    return render(request, 'shopmall/home.html', context=context)





def market(request, categoryId, childId, sortId):
    currentCategory = []
    currentCategory.append(categoryId)

    productTypesList = ProductTypes.objects.all()

    childTypeList = productTypesList.filter(typeId=categoryId)[0]
    currentCategory.append(childTypeList.typeName)

    childTypeList = childTypeList.childType.split('#')
    for i in range(len(childTypeList)):
        childTypeList[i] = childTypeList[i].split(':')

    # print(childTypeList)

    if childId == '0':
        productsList = Products.objects.filter(categoryId=categoryId)
    else:
        productsList = Products.objects.filter(categoryId=categoryId, childId=childId)
        currentCategory.append(childId)
        currentCategory.append(productsList[0].childName)

    if(sortId == '1'):
        productsList = productsList.order_by('-hot')
    if (sortId == '2'):
        productsList = productsList.order_by('-sales')
    if (sortId == '3'):
        productsList = productsList.order_by('discountPrice')
    if (sortId == '4'):
        productsList = productsList.order_by('-discountPrice')

    print(currentCategory)

    currentToken = request.session.get('token')
    if currentToken:
        try:
            user = Users.objects.get(userToken=currentToken)
            cartsList = Carts.objects1.filter(userAccount=user.userAccount)

            # cartsList 和 productsList 交叉比對，若 productId 相同，則該 product裡添加一個新屬性 cartNum = 購物車購買數
            for c in cartsList:
                for p in productsList:
                    if p.productId == c.productId:
                        p.cartNum = c.productNum
                        continue


        except Users.DoesNotExist as e:
            # currentToken已過期，不做事
            pass

    context = {
        'tittle': '超市',
        'productTypesList': productTypesList,
        'productsList': productsList,
        'currentCategory': currentCategory,
        'childTypeList': childTypeList,
    }

    return render(request, 'shopmall/market.html', context=context)





def cart(request):
    cartsList = []
    currentToken = request.session.get('token')
    totalPrice = 0
    totalProductNum = 0
    if currentToken:
        try:
            user = Users.objects.get(userToken=currentToken)
            cartsList = Carts.objects1.filter(userAccount=user.userAccount)

            isAllSelect = True
            if(len(cartsList) == 0):
                isAllSelect = False
            for cart in cartsList:
                totalPrice += cart.totalPrice
                totalProductNum += cart.productNum
                if(cart.isChoose == False):
                    isAllSelect = False
            print('111')
        except Users.DoesNotExist as e:
            # token不匹配(過期)，跳去 /login/
            return redirect('/login/')
    else:
        # 沒任何token，跳去 /login/
        return redirect('/login/')

    context = {
        'tittle': '購物車',
        'cartsList': cartsList,
        'user': user,
        'totalPrice': totalPrice,
        'totalProductNum': totalProductNum,
        'isAllSelect': isAllSelect,
    }

    return render(request, 'shopmall/cart.html', context=context)





def changeCart(request, flag):
    # 驗證用戶是否已登入
    currentToken = request.session.get('token')

    if currentToken:
        try:
            user = Users.objects.get(userToken=currentToken)
        except Users.DoesNotExist as e:
            # currentToken已過期，跳轉login介面
            return JsonResponse({'message': 'currentToken已過期', 'status': 'error'})

        productId = request.POST.get('productId')
        product = Products.objects.get(productId=productId)

        # 資料庫的token值 與 currentToken 一致，表示登入中，進行處理
        if flag == '0':
            # 減1
            try:
                oneCart = Carts.objects1.get(userAccount=user.userAccount, productId=productId)
                oneCart.productNum -= 1
                # 庫存加 1
                product.inventory += 1
                product.save()
                if oneCart.productNum <= 0:
                    oneCart.delete()
                    print('數量減至0，刪除該記錄')
                    return JsonResponse({'message': '數量減至0，刪除該記錄', 'status': 'success', 'cartNum': 0})
                oneCart.totalPrice = product.discountPrice * oneCart.productNum
                oneCart.save()
                print('數量減1')
                return JsonResponse({'message': '數量減1', 'status': 'success', 'cartNum': oneCart.productNum, 'cartPrice': oneCart.totalPrice})
            except Carts.DoesNotExist as e:
                # 資料庫不存在該紀錄，不做任何事
                print('cart記錄不存在，不做事')
                return JsonResponse({'message': 'cart記錄不存在，不做事', 'status': 'doNothing'})
        elif flag == '1':
            # 加1
            if product.inventory == 0:
                print('已經沒庫存了')
                return JsonResponse({'message': '已經沒庫存了', 'status': 'doNothing'})
            try:
                oneCart = Carts.objects1.get(userAccount=user.userAccount, productId=productId, orderId='0')
                oneCart.productNum += 1
                oneCart.totalPrice = product.discountPrice * oneCart.productNum
                oneCart.save()
                # 庫存減 1
                product.inventory -= 1
                product.save()
                print('數量加1')
                return JsonResponse({'message':'數量加1', 'status':'success', 'cartNum':oneCart.productNum, 'cartPrice': oneCart.totalPrice})
            except Carts.DoesNotExist as e:
                # 資料庫不存在該紀錄，直接新增一條
                print('新增一條cart記錄')
                newCart = Carts.createCart(user.userAccount, productId, 1, product.discountPrice, True, product.productImg, product.productName, '0', False)
                newCart.save()
                # 庫存減 1
                product.inventory -= 1
                product.save()
                return JsonResponse({'message':'新增一條cart記錄', 'status':'success', 'cartNum':1})

        elif flag == '2':
            # 購物車中，是否勾選此商品
            oneCart = Carts.objects1.get(userAccount=user.userAccount, productId=productId, orderId='0')
            oneCart.isChoose = not (oneCart.isChoose)
            oneCart.save()
            print(oneCart.isChoose)
            return JsonResponse({'message': '更改勾選記錄', 'status': 'success', 'isChoose': oneCart.isChoose})

        elif flag == '3':
            # 購物車中，全部勾選
            oneCart = Carts.objects1.get(userAccount=user.userAccount, productId=productId, orderId='0')
            oneCart.isChoose = True
            oneCart.save()
            print(oneCart.isChoose)
            return JsonResponse({'message': '全部勾選', 'status': 'allSelect'})

        elif flag == '4':
            # 購物車中，全部取消勾選
            oneCart = Carts.objects1.get(userAccount=user.userAccount, productId=productId, orderId='0')
            oneCart.isChoose = False
            oneCart.save()
            print(oneCart.isChoose)
            return JsonResponse({'message': '全部取消勾選', 'status': 'allDisSelect'})

    else:
        # 沒登入，基本上，完全不會跑這裡，呼叫時應該都是有token的，但可能過期
        # 除非他先進cart頁面，在手動刪除session
        return JsonResponse({'message':'未登入', 'status':'error'})

    return None










def mine(request):
    username = request.session.get('username', '未登入(點此登入)')

    context = {
        'tittle': '我的',
        'username': username,
    }
    return render(request, 'shopmall/mine.html', context=context)






from .forms.form import LoginForm
def login(request):
    # If this is a POST request then process the Form data
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        hisForm = LoginForm(request.POST)

        # Check if the form is valid 驗證傳過來的資料有沒有問題
        if hisForm.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            # 取出使用者輸入的數據
            name = hisForm.cleaned_data['username']
            passwd = hisForm.cleaned_data['passwd']

            # 查詢資料庫是否有該帳戶
            try:
                user = Users.objects.get(userAccount=name)
                if user.userPasswd != passwd:
                    # 有該帳戶，但密碼錯誤
                    print('密碼錯誤')
                    return render(request, 'shopmall/login.html', {'hisForm': hisForm, 'tittle': '登入', 'error':'密碼錯誤'})
            except Users.DoesNotExist as e:
                # 沒有該帳戶
                print('帳戶未註冊')
                return render(request, 'shopmall/login.html', {'hisForm': hisForm, 'tittle': '登入', 'error':'帳戶未註冊'})

            # 有該用戶且密碼正確，隨機生成新的且不重複的token，存進資料庫
            userToken = None
            while (True):
                try:
                    userToken = str(time.time() + random.randrange(1, 100000)).replace('.', '')
                    Users.objects.get(userToken=userToken)
                except Users.DoesNotExist as e:
                    print("該userToken可用")
                    break
            user.userToken = userToken
            user.save()

            request.session['username'] = user.userNickName
            request.session['token'] = user.userToken

            # redirect to a new URL:
            return redirect('/mine/')
        else:
            # 若輸入資料驗證有誤
            print('資料格式驗證錯誤')

    # If this is a GET (or any other method) create the default form.
    else:
        hisForm = LoginForm()

    return render(request, 'shopmall/login.html', {'hisForm': hisForm, 'tittle': '登入'})






from django.conf import settings
def register(request):
    if request.method == 'POST':
        # 進行註冊
        userAccount = request.POST.get('userAccount')   # get('input的name屬性')
        userPasswd = request.POST.get('userPass')
        userNickName = request.POST.get('nickName')
        userPhone = request.POST.get('userPhone')
        userAddress = request.POST.get('userAddress')
        userRank = 1

        # 隨機產生不重複的token
        userToken = None
        while (True):
            try:
                userToken = str(time.time() + random.randrange(1, 100000)).replace('.', '')
                Users.objects.get(userToken=userToken)
            except Users.DoesNotExist as e:
                print("該userToken可用")
                break

        userImg = os.path.join(settings.MEDIA_ROOT, 'headshot\\' + userAccount + '.png')

        # 若model的userImg欄位是ImageField() 可直接存
        pictureFile = request.FILES['userImg']
        with open(userImg, 'wb') as fp:
            for data in pictureFile.chunks():
                fp.write(data)

        newUser = Users.createUser(userAccount, userPasswd, userNickName, userPhone, userAddress, userImg, userRank, userToken)
        newUser.save()

        request.session['username'] = userNickName
        request.session['token'] = userToken

        return redirect('/mine/')

    else:
        # 返回註冊頁面
        return render(request, 'shopmall/register.html')





from django.http import JsonResponse
# 驗證註冊帳號是否存在
def checkuserid(request):
    userid = request.POST.get('userid')
    try:
        user = Users.objects.get(userAccount=userid)
        return JsonResponse({'message':'該用戶名已存在', 'status':'error'})
    except Users.DoesNotExist as e:
        return JsonResponse({'message':'無該用戶名', 'status':'success'})





from django.contrib.auth import logout
def quit(request):
    logout(request)
    return redirect('/mine/')


def saveOrder(request):
    # 驗證用戶是否已登入
    currentToken = request.session.get('token')

    if currentToken:
        try:
            user = Users.objects.get(userToken=currentToken)
        except Users.DoesNotExist as e:
            # currentToken已過期，跳轉login介面
            return JsonResponse({'message': 'currentToken已過期', 'status': 'error'})


        userCartSelectList = Carts.objects1.filter(userAccount=user.userAccount, isChoose=True)

        if len(userCartSelectList) == 0:
            print("該用戶的購物車沒有任何勾選的商品")
            return JsonResponse({'message': '該用戶的購物車沒有任何勾選的商品', 'status': 'doNothing'})

        # 隨機產生不重複的orderId
        orderId = None
        while(True):
            try:
                orderId = str(time.time() + random.randrange(1, 100000)).replace('.', '')
                Orders.objects.get(orderId=orderId)
            except Orders.DoesNotExist as e:
                print("該orderId可用")
                break

        print(orderId)
        # 創建一個新訂單
        newOrder = Orders.createOrder(orderId, user.userAccount, 1, False)
        newOrder.save()

        # 將Carts內，勾選的商品，邏輯刪除，並標示屬於哪份訂單 orderId
        for userCartSelect in userCartSelectList:
            userCartSelect.isDelete = True
            userCartSelect.orderId = newOrder.orderId
            userCartSelect.save()

    else:
        # 沒登入，基本上，完全不會跑這裡，呼叫時應該都是有token的，但可能過期
        # 除非他先進cart頁面，在手動刪除session
        # 或直接訪問此view(網址)
        return JsonResponse({'message': '未登入', 'status': 'error'})

    return JsonResponse({'message':'已新增訂單', 'status':'success'})





def showMyOrders(request):
    # 驗證用戶是否已登入
    currentToken = request.session.get('token')

    if currentToken:
        try:
            user = Users.objects.get(userToken=currentToken)
        except Users.DoesNotExist as e:
            # currentToken已過期，跳轉login介面
            return JsonResponse({'message': 'currentToken已過期', 'status': 'error'})

        # 用戶已登入，拿出該用戶所有的訂單
        # 因為最後要用 JsonResponse，queryset()並不能回傳
        # 需要先序列化，回傳型態為 "Json字串"
        ordersList = serializers.serialize("json", Orders.objects.filter(userId=user.userAccount), fields=('orderId', 'progress'))

        # 將"Json字串"轉回正常字典，以便做處理
        ordersList = json.loads(ordersList)

        orderData = []
        for order in ordersList:
            tempDict = {
                'orderId': order['fields']['orderId'],
                'progress': order['fields']['progress']
            }
            orderData.append(tempDict)

        print(orderData)

        if(len(orderData) == 0):
            return JsonResponse({'message': '該用戶沒任何訂單', 'status': 'doNothing'})

        returnData = {
            'message': '顯示所有訂單',
            'status': 'success',
            'orderData': orderData,
        }

        return JsonResponse(returnData)

    else:
        return JsonResponse({'message': '未登入', 'status': 'error'})







def showOrderDetail(request, orderId):
    # 驗證用戶是否已登入
    currentToken = request.session.get('token')

    if currentToken:
        try:
            user = Users.objects.get(userToken=currentToken)
        except Users.DoesNotExist as e:
            # currentToken已過期，跳轉login介面
            return JsonResponse({'message': 'currentToken已過期', 'status': 'error'})

        # 用戶已登入，拿出該訂單的詳細商品資訊(Carts資料庫裡，isDelete=True,orderId=orderId)
        orderDetailList = Carts.objects2.filter(orderId=orderId)
        if (len(orderDetailList) == 0):
            # 資料庫已查詢不到詳細資訊
            return JsonResponse({'message': '資料庫已查詢不到詳細資訊', 'status': 'doNothing'})

        # 因為最後要用 JsonResponse，queryset()並不能回傳
        # 需要先序列化，回傳型態為 "Json字串"
        orderDetailList = serializers.serialize("json", orderDetailList, fields=('productId', 'productNum', 'totalPrice', 'productImg', 'productName', 'orderId'))

        # 將"Json字串"轉回正常字典，以便做處理
        orderDetailList = json.loads(orderDetailList)
        print(orderDetailList)

        return JsonResponse({'message': '顯示訂單細節', 'status': 'success', 'orderDetailList': orderDetailList})

    else:
        return JsonResponse({'message': '未登入', 'status': 'error'})


def deleteOrder(request):
    orderId = request.POST.get('orderId')
    print(orderId)
    if orderId == None:
        return JsonResponse({'message': '沒拿到orderId', 'status': 'doNothing'})

    # 驗證用戶是否已登入
    currentToken = request.session.get('token')

    if currentToken:
        try:
            user = Users.objects.get(userToken=currentToken)
        except Users.DoesNotExist as e:
            # currentToken已過期，跳轉login介面
            return JsonResponse({'message': 'currentToken已過期', 'status': 'error'})

        # 用戶已登入，拿出該訂單的詳細商品資訊(Carts資料庫裡，isDelete=True,orderId=orderId)
        try:
            order = Orders.objects.get(orderId=orderId)
        except Orders.DoesNotExist as e:
            return JsonResponse({'message': '資料庫已查詢不到該訂單', 'status': 'doNothing'})

        order.delete()

        return JsonResponse({'message': '成功刪除該訂單', 'status': 'success', 'orderId': orderId})
    else:
        return JsonResponse({'message': '未登入', 'status': 'error'})