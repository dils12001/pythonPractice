import os
from random import randint
from django.contrib.auth import logout
from django.core.paginator import Paginator
from django.db.models import F, Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
import django.http

from .forms import ProfileForm
from .models import Users, Departments, UsersProfile


# Create your views here.
def getUsers(request):
    pageNum = int(request.GET.get('pageNum', 1))
    print(pageNum)
    users = Users.objects.all().order_by('id') #pycharm community不支援django,所以warning
    # 每頁顯示4條記錄
    paginator = Paginator(users,4)
    currentPage = paginator.page(pageNum)
    print(currentPage[0])
    # 可以與別的欄位進行比較 用 F(需import F)，可對其做算術運算
    #users = Users.objects.filter(u_age__gte=F('別的欄位屬性名稱')+20)
    #users = Users.objects.filter(Q(u_dept_id=6) | Q(u_dept_id=5))
    # or 邏輯 ，使用 Q ，需import Q
    #users = Users.objects.filter(Q(u_dept_id=6) | Q(u_gender=1))
    # 若只有一個 Q對象，Users.objects.filter(Q(u_dept_id=6))，等同匹配u_dept_id=6
    # 若前面加上 ~ ，Users.objects.filter(~Q(u_dept_id=6))，取反
    #users = Users.objects.filter(~Q(u_dept_id=6))
    # 下面這行有Bug??
    #users = Users.objects.filter(departments__d_name='Game')
    #print(users)
    '''count = 1
    for user in users:
        print(user.id)
        print(count)
        user.id = count
        print('ok')
        user.save()
        count = count+1
       # print(user.id)'''
    #user = Users.objects.first()
    #print(user.u_name)
    #a = Users.objects.get(pk=88)
    #print(a.u_name)
    #print(a.u_name)

    context = {
        'users': currentPage,
        'h1': 'Get All User',
    }
    return render(request, 'getUsers.html', context)
    #context=字典,在html檔裡用{% for user in 字典key %}調用 上面的'users'
    #html裡使用模板語法,{{ 字典key值 }} 作調用

def addUsers(request):
    for i in range(10):
        randomNum = randint(18,100)
        #print(randomNum)
        user = Users()
        haveUser = Users.objects.filter(u_name='user%d'%randomNum)
        #print(not haveUser.exists())
        if not haveUser.exists():
            user.u_name = 'user%d' %randomNum
            user.u_password = randomNum
            user.save()
            print('add user%d'%randomNum)
    return HttpResponse("success to add some users")


def delUsers(request):
    userCount = Users.objects.count()
    print(userCount)
    for i in range(userCount):
        user = Users.objects.first()
        user.delete()
    return HttpResponse('success to delete all users')


def updateUser(request):
    '''
    改第一筆的u_name
    '''
    #userCount = Users.objects.count()
    #ranNum = randint(1,userCount)
    user = Users.objects.first()
    print(user.u_name)
    user.u_name = 'stuby'+user.u_name[4:]
    user.save()
    return HttpResponse(user.u_name)


def num(request,num):
    return HttpResponse('You asked page number %s.' % num)

def getDept(request):
    depts = Departments.deptObj2.all()
    # 關聯查詢，u_name裡有符合條件的，找出他們的所屬部門
    #depts = Departments.deptObj2.filter(Q(users__u_name__contains='幹') | Q(users__u_name__contains='奴隸'))
    context = {
        'depts':depts
    }
    return render(request, 'getDepts.html', context=context)


def getDeptUser(request,num):
    #print(num)
    #deptUsers = Users.objects.filter(u_dept_id=int(num))
    #deptName = Departments.objects.filter(id=int(num))[0].d_name
    #獲取一個部門對象
    try:
        dept = Departments.deptObj2.get(pk=int(num))
    except Exception as e:
        detail = e.args[0]
        if detail == 'Departments matching query does not exist.':
            return HttpResponse('沒有 "%s" 這個部門編號喔~ .' % num)
    deptName = dept.d_name
    #反向獲取 外鍵 關連到這個 dept對象 的所有 User對象 們
    #格式: 被外鍵關聯的對象.使用外鍵的"小寫"類名_set.all()
    deptUsers = dept.users_set.all()
    #print(deptUsers)

    context = {
        'deptName':deptName,
        'deptUsers':deptUsers
    }
    return render(request, 'getDeptsUsers.html', context=context)


def get(request):
    '''
    # 當使用者輸入 http://127.0.0.1:8000/get/?a=5&b=9&c=45 時，取得GET請求的參數
    a = request.GET.get('a')
    b = request.GET['b']    #另一種寫法
    c = request.GET.get('c')
    '''
    # 當使用者輸入 http://127.0.0.1:8000/get/?a=5&a=9&c=45 時，取得GET請求的參數
    # 因為傳過來的 a 有兩個，用getlist接收
    a = request.GET.getlist('a')
    c = request.GET.get('c')
    return HttpResponse(a[0]+a[1]+c)


def registerPage(request):
    return render(request, 'registerUser.html')


def registUser(request):
    #接收 POST請求 時，需先將 settings.py 中的 csrf 刪掉(註解)
    '''
    MIDDLEWARE = [
        # 'django.middleware.csrf.CsrfViewMiddleware',
        ]
    '''
    user = Users()
    user.u_name = request.POST['name']
    user.u_password = request.POST['passwd']
    user.u_gender = request.POST['sex']
    user.u_age = request.POST['age']
    dept = Departments.deptObj2.filter(d_name=request.POST['dept'])[0]
    user.u_dept = dept
    user.save()
    '''
    a = request.POST['name']    #html input標籤裡的 name屬性
    b = request.POST['passwd']
    c = request.POST['sex']
    d = request.POST['age']
    e = request.POST['dept']
    f = request.POST.getlist('hobby')   #拿列表依定要用 getlist()
    '''

    return HttpResponse('success create a user "%s".' % user.u_name)


def home(request):
    print(request.session.get('username', default='遊客'))
    imgList = []
    for i in range(2,25):
        imgPath = '/myStatic/myApp/img/' + str(i) + '.jpg'
        imgList.append(imgPath)
    context = {
        'username' : request.session.get('username', default='遊客'),
        'imgList' : imgList,
    }

    return render(request, 'home.html', context=context)

def login(request):
    return render(request, 'login.html')

def log_out(request):
    # 清除session
    logout(request)
    #request.session.clear()
    #request.session.flush()
    print('登出囉~')
    # 重定向
    return redirect('/')


def verify(request):
    # 需先啟用 redis，才能將 session 存入redis的資料庫
    try:
        user = Users.objects.get(u_name=request.POST['uname'])
        if user.u_password == request.POST['upasswd']:
            request.session['username'] = request.POST['uname']

            # 設定session持續時長，默認是2星期後
            # set_expiry(整數) : 單位是 秒
            # set_expiry(0) : 當瀏覽器關閉時過期
            # set_expiry(None) : 永不過期
            # set_expiry(時間對象) : 該時間過期
            #request.session.set_expiry(300)
            print('登入成功')
        else:
            print('密碼錯誤')
    except:
        print('無此帳號')
    return redirect('/')


def saveProfilePage(request):
    saved = False
    print(111)

    if request.method == "POST":
        print(222)
        # Get the posted form
        MyProfileForm = ProfileForm(request.POST, request.FILES)
        print(333)
        print(MyProfileForm)
        if MyProfileForm. is_valid():
            print(444)
            user = Users.objects.filter(u_name=MyProfileForm.cleaned_data["name"])[0]
            print(user)
            if user:
                usersProfile = UsersProfile()
                usersProfile.img = MyProfileForm.cleaned_data["picture"]
                usersProfile.user = user
                usersProfile.save()
                saved = True
            else:
                MyProfileForm = ProfileForm()

    return render(request, 'savedProfile.html', locals())

def profilePage(request):
    return render(request, 'profile.html')

