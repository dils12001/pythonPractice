from django.contrib import admin
#從myApp/models.py import Users這個Class
from .models import Users,Departments
# Register your models here.
#superuser = dennis,Zaq12wsx


#在 新增Dept 時，也一併新增User引用該Dept當外鍵
#下面DepartmentsAdmin會用到
#也可替換繼承對象如下，顯示樣板不一樣而已
# class createUsersByDept(admin.StackedInline):
class createUsersByDept(admin.TabularInline):
    #新增的資料庫類
    model = Users
    #一次順便新增幾個 該資料庫類的記錄(添加 2個user記錄)
    extra = 2

#自定義該資料庫在admin頁面的顯示方式
#裝飾器 取代 admin.site.register(Users, UsersAdmin)
@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    #顯示該欄位時，變換Boolean為其他詞彙，list_display = []引用
    def gender(self):
        if self.u_gender:
            return '男'
        else:
            return '女'
    gender.short_description = '性別'

    def isDelete(self):
        if self.u_isDelete == 0:
            return '未被刪除'
        else:
            return '被邏輯刪除'
    isDelete.short_description = '是否被邏輯刪除'

    #列表頁 的屬性設置

    #顯示哪些欄位
    list_display = ['id', 'u_name', 'u_password', gender, 'u_age', 'u_dept', isDelete]
    #以該欄位來進行篩選(篩選器出現在右方)，通常應該會選用外鍵欄位
    list_filter = ['u_dept','u_gender','u_age']
    #按該欄位來進行搜索(搜索框出現在上方)
    search_fields = ['u_name','u_dept']
    #每5條數據 當一頁
    list_per_page = 5

    #添加,修改頁 的屬性設置
    #fields和fieldsets二者僅能選其一

    #當添加或修改數據時，進入的那個頁面，可決定欄位的顯示順序
    #不用加'id'，因為id是系統自動生成的
    #fields = ['u_password','u_name']

    #可再將欄位分組顯示
    fieldsets = [
        #('groupName',{'fields':['fieldName','fieldName',...]})
        ('UserName and Password',{'fields':['u_name','u_password']}),
        ('Basic Information',{'fields':['u_dept', 'u_gender', 'u_age', 'u_isDelete']})
    ]

    #執行動作的框框顯示在哪兒
    actions_on_top = False
    actions_on_bottom = True


#自定義該資料庫在admin頁面的顯示方式
class DepartmentsAdmin(admin.ModelAdmin):
    #要在新增Dept時，順便新增引用它外鍵的User
    #inlines = [上面自定義的類名]
    inlines = [createUsersByDept]

    #列表頁 的屬性設置

    #顯示哪些欄位
    list_display = ['id', 'd_name', 'd_description', 'd_createDate', 'd_isDelete']
    #以該欄位來進行篩選(篩選器出現在右方)，通常應該會選用外鍵欄位
    list_filter = ['d_name']
    #按該欄位來進行搜索(搜索框出現在上方)
    search_fields = ['id', 'd_name']
    #每5條數據 當一頁
    list_per_page = 5

    #添加,修改頁 的屬性設置
    #fields和fieldsets二者僅能選其一

    #當添加或修改數據時，進入的那個頁面，可決定欄位的顯示順序
    #不用加'id'，因為id是系統自動生成的
    fields = ['d_name', 'd_description', 'd_createDate', 'd_isDelete']

    #可再將欄位分組顯示
    '''fieldsets = [
        #('groupName',{'fields':['fieldName','fieldName',...]})
        ('UserName and Password',{'fields':['u_name','u_password']}),
        ('Basic Information',{'fields':['u_dept', 'u_gender', 'u_age', 'u_isDelete']})
    ]'''

#使admin這網頁能管理Users這個資料庫
#admin.site.register(該資料庫類名)
admin.site.register(Departments, DepartmentsAdmin)



