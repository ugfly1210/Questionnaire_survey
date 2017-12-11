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
def question(request,qnid):
    '''问题相关'''
    if request.method=='GET':
        question_list = models.Question.objects.filter(questionnaire_id=qnid).all()
        qn_obj = models.QuestionNaire.objects.filter(id=qnid).first()
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
        return render(request,'question.html',{'form_list':inner(),'qnid':qnid})

    else:
        login_status(request)
        ret = {'status': True, 'msg': None}
        try :
            data = request.POST.get('data') # 不转换一下的话,拿到的还是json字符串
            '''
           [
           {"qid":"1","question_title":"佩奇稳不稳","question_tp":"1","option_list":null},
           
           {
           "qid":"2","question_title":"egon萌不萌","question_tp":"2",
           "option_list":
           [
           {"option_name":"a","score":"2","id":"1"},
           {"option_name":"b","score":"6","id":"2"},
           {"option_name":"d","score":"1","id":"4"}
           ]
           },
           {"qid":"4","question_title":"李乾隆死不死","question_tp":"2","option_list":[{"option_name":"c","score":"9","id":"3"},{"option_name":"eee","score":"2","id":"5"}]},{"qid":"5","question_title":"qwer","question_tp":"3","option_list":null}]
    
            '''
            data = json.loads(data) # 变为python可以识别的格式
            '''拿到数据后先判断问题ID,如果为空就是新增.如果少了就删,多了就存,还在的就更新'''
            question_list = models.Question.objects.filter(questionnaire_id=qnid)
            # 拿到用户提交的所有问题id
            post_qid_list = [i.get('qid') for i in data if i.get('qid')]
            # 获取现在数据库已存在的问题id
            que_id_list = [i.id for i in question_list if i.id]
            # 获取要删除的id
            del_id_list = set(que_id_list).difference(post_qid_list)
            # 判断哪些是需要更新,哪些需要删除,哪些需要新增.
            for item in data:
                qid = item.get('qid') # 拿到问题ID
                question_title = item.get('question_title') # 拿到问题名称
                question_tp = item.get('question_tp') # 拿到问题类型
                option_list = item.get('option_list') # 拿到选项列表
                if qid not in que_id_list:
                    # 新增
                    que_obj = models.Question.objects.create(question_title=question_title,question_tp=question_tp)
                    if question_tp == 2: # 如果tp=2,说明是单选,需要把选项保存一下
                        for op_obj in option_list:
                            models.Option.objects.create(question=que_obj,option_name=op_obj.get('option_name'),socre=op_obj.get('score'))
                else: # 如果在就是更新
                    models.Question.objects.filter(id=qid).update(caption=question_title,question_tp=question_tp)
                    if not option_list:
                        # 如果提交的问题id在表问题id里面,就是更新.
                        # 再如果原来的问题tp为2,而现在是非2, 那么就要把之前单选选项删除.
                        models.Option.objects.filter(question_id=qid).delete()
                    else:
                        '''如果有,就更新或者新添'''
                        models.Option.objects.filter(question_id=qid).delete()
                        for option in option_list:
                            models.Option.objects.create(option_name=option.get('option_name'),score=option.get('score'),question_id=qid)
            models.Question.objects.filter(id__in=del_id_list).delete()
        except Exception as e :
            ret['msg'] = e
            ret['status'] = False

        return HttpResponse(ret)












        return HttpResponse('ok')

def login_status(request):
    '''判断用户当前登录状态'''
    if not request.session.get('username'):
        return redirect('/login/')

def student_login(request):
    if request.method == 'GET':
        return render(request,'stu_login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        stu_obj = models.Student.objects.filter(name=username,password=password).first()
        login_response = {'flag':False,'error_massage':None}
        if not stu_obj:
            login_response['error_massage'] = 'STUDENT! YOUR username or password is error!'
        else:
            login_response['flag'] = True
            request.session['stu_info'] = {'stu_user':stu_obj.name,'stu_id':stu_obj.id}

        return HttpResponse(json.dumps(login_response))

def eva_stu(request,class_id,qn_id):

    stu_obj = models.Student.objects.filter(id=request.session.get("stu_info").get("stu_id"),classlist_id=class_id).first()

    # 1. 先看是否是本班学生
    if not stu_obj:
        return HttpResponse('您不配啊!!!')
    # 2. 看它是否已经答过问卷
    ans_obj = models.Answer.objects.filter(student_id=stu_obj.id,question__questionnaire_id=qn_id).count()
    if ans_obj:
        return HttpResponse('别闹! 您已经答过了啊')
    # 3. 拿到所有的问题并显示
    from django.forms import Form,fields,widgets
    que_list = models.Question.objects.filter(questionnaire_id=qn_id).all()
    field_dict = {}
    for que in que_list:
        if que.tp == 1: # 打分用chioce
            field_dict['val_%s' % que.id] = fields.ChoiceField(
                label = que.caption,
                required=True,
                error_messages={'required' : '不能为空哦'},
                widget=widgets.RadioSelect,
                choices=[ (i,i) for i in range(1,11) if i ]
            )
        elif que.tp == 2 : # 单选
            field_dict['option_%s' % que.id] = fields.ChoiceField(
                required=True,
                label = que.caption,
                error_messages={'required':'必选'},
                choices = models.Option.objects.filter(question_id=que.id).values_list('id','option_name'), #为什么改成values_list就可以显示选项
                widget = widgets.RadioSelect
            )
        else :
            field_dict['text_%s' % que.id] = fields.CharField(
                required=True,
                label = que.caption,
                widget = widgets.Textarea,
                validators=[func,]
            )
    # print("field_dict",field_dict)
    # 创建类,并实例化
    # print('field_dict======',field_dict)
    MyAnswerForm = type('MyAnswerForm', (Form,),field_dict)
    if request.method == 'GET':
        form  = MyAnswerForm()
        return render(request,'eva_stu.html',{'form':form})
    else:
        form = MyAnswerForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            # {'option_1': '2', 'option_2': '4', 'val_3': '4', 'text_4': '123123123213213213213'}
            l = []
            for key,v in form.cleaned_data.items():
                k,qid = key.rsplit('_',1)
                answer_dict = {'student_id':stu_obj.id,'question_id':qid,k:v}
                print(answer_dict)
                # l1 = l.append(answer_dict)
                l.append(models.Answer(**answer_dict))
                print(77777)
                # models.Answer.objects.bulk_create()
            return HttpResponse('ok')
        return render(request,'eva_stu.html',{'form':form})

from django.core.exceptions import ValidationError
def func(val):
    if len(val) < 15 :
        raise ValidationError(' duan duan duan ')



# def meeting(req):
#     return render(req,'meeting.html')