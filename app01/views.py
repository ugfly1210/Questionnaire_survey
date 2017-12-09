import json
from django.shortcuts import render,HttpResponse,redirect
from app01 import models,forms
from app01.forms import QuestionModelForm,OptionModelForm
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
# def add(request):
#     '''添加'''
#     if request.method == 'GET':
#         form = forms.QuestionNaire_Form()
#         # class_list = models.ClassList.objects.all()
#         return render(request,'add.html',{'form':form})
#     else:
#         user_obj = models.UserInfo.objects.filter(name=request.session.get('username')).first()
#         title = request.POST.get('np_title')
#         class_id = request.POST.get('class_list')
#         models.QuestionNaire.objects.create(title=title,classlist_id=class_id,creator_id=user_obj.id)
#         return redirect('/index/')

def add(request):
    '''添加'''
    if request.method == 'GET':
        form = forms.QuestionNaire_Form()
        return render(request, 'add.html', {'form' : form})
    else :
        form = forms.QuestionNaire_Form(request.POST)
        if form.is_valid():
            title = request.POST.get('title')
            classlist_id = request.POST.get('classlist')
            print('classlist_id-------',classlist_id)
            name = request.session.get('username')
            user_obj = models.UserInfo.objects.filter(name=name).first()
            models.QuestionNaire.objects.create(title=title,classlist_id=classlist_id,creator=user_obj)
            return redirect('/index/')
        else:
            return render(request,'add.html',{'form':form})
def question(request,qid):
    '''问题相关'''
    print(request.POST,qid)
    if request.method=='GET':
        question_list = models.Question.objects.filter(questionnaire_id=qid).all()
        qn_obj = models.QuestionNaire.objects.filter(id=qid).first()
        # print('-------question_list',question_list)
        # 方法一 : 通过循环遍历
        # if not question_list:  #如果没有的话,说明是新添加的问题.   问题没有归属问卷
        #     form_list = []
        #     form = QuestionModelForm()
        #     form_list.append(form)
        # else:
        #     '''如果有.说明这个问题有问卷id,就应该显示它的值.'''
        #     form_list = []
        #     for question in question_list:   #要为每一个对象生成一个实例化对象
        #         form = QuestionModelForm(instance=question)  #把对象的字段的值放到框框里面
        #         form_list.append(form)
        # return render(request,'question.html',{'form_list':form_list})
        def inner():
            if not question_list:  #如果没有的话,说明是新添加的问题.   问题没有归属问卷
                form = QuestionModelForm()
                # yield form
                # print('66666666666')
                yield {'form':form,'obj':None,'option_class':'hide','options':None}         #这里用yield,前端发来请求说要取值的时候,这里才遍历.
            else:
                '''如果有.说明这个问题有问卷id,就应该显示它的值.'''
                for question in question_list:   #要为每一个对象生成一个实例化对象
                    form = QuestionModelForm(instance=question)  #把对象的字段的值放到框框里面
                    '''
                    给obj是因为传一个对象过去,之后可能会拿对象的字段.
                    给一个option_class是因为想让在选项为单选的时候,才会出现那个编辑选项框.
                    '''
                    temp = {'form':form,'obj':question,'option_class':'hide','options':None}
                    # print('question.tp--------',question.tp)
                    if question.tp == 2 :
                        # print(question.tp)
                        temp['option_class'] = ''
                        '''当类型为单选,应该把已经存在的选项列出来.要拿到当前问题下的所有选项.'''
                        # option_mf_list = []
                        # option_list = models.Option.objects.filter(question=question)
                        # for option in option_list:
                        #     '''为每一个option创建一个modelform对象'''
                        #     option_modelform = OptionModelForm(instance=option)
                        #     option_mf_list.append(option_modelform)
                        # temp['options'] = option_mf_list
                        def inner_option(_question):
                            option_list = models.Option.objects.filter(question_id=_question.id)
                            for option in option_list:
                                '''为每一个option创建一个modelform对象'''
                                yield {'form':OptionModelForm(instance=option),'obj':option}
                        # for option in inner_option():
                        #     print(option)
                        temp['options'] = inner_option(question)  #这个为什么缩进这么多
                    yield temp
                    # print('temp---',temp)
                    # print('inner=====',inner())
        # for item in inner():
            # print("------", item.get("options"))
            # if item.get("obj").tp == 2:
                # for option in item.get("options"):
                    # print(option)
        return render(request,'question.html',{'form_list':inner(),'qid':qid})

    else:
        if not request.session.get('username'):
            return redirect('/login/')
        return HttpResponse('ok')
    '''
    拿到问题ID,对比一下.'''