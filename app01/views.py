import json
from django.shortcuts import render,HttpResponse,redirect
from app01 import models,forms
# Create your views here.

def login(request):
    '''登录'''
    if request.method == 'GET':
        return render(request,'login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = models.UserInfo.objects.filter(name=username,password=password).first()
        login_response = {'flag':False,'error_massage':None}
        if not user_obj:
            login_response['error_massage'] = 'username or password is error!'
        else:
            login_response['flag'] = True
            request.session['username'] = username
        print(login_response)
        return HttpResponse(json.dumps(login_response))

def index(request):
    '''首页'''
    qn = models.QuestionNaire.objects.all()
    return render(request,'index.html',{'qn':qn})

def add(request):
    '''添加'''
    if request.method == 'GET':
        form = forms.QuestionNaire_Form()
        return render(request,'add.html',{'form' : form})
    else :
        pass

def qn(request,class_id,qn_id):    #def qn_addr(request,**kwargs)
    '''问卷选项'''
    pass
