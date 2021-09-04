from random import randint
from django.http import HttpResponse
from django.shortcuts import render
import django.http
from .models import Users, Departments


# Create your views here.
def hello(request):
    return HttpResponse('Hello')


def tempTest(request):
    return render(request, 'htmltest.html')


def temp2(request):
    return render(request, 'template2.html')


def getUsers(request):
    users = Users.objects.all() #pycharm community不支援django,所以warning
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
        'users': users,
        'h1': 'Get All User',
    }
    return render(request, 'getUsers.html', context=context)
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
    context = {
        'depts':depts
    }
    return render(request, 'getDepts.html', context=context)


def getDeptUser(request,num):
    print(num)
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
    print(deptUsers)


    context = {
        'deptName':deptName,
        'deptUsers':deptUsers
    }
    return render(request, 'getDeptsUsers.html', context=context)