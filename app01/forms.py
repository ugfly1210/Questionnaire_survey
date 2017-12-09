from django.forms import Form       #代表类的基类
from django.forms import fields     #代表字段
from django.forms import widgets    #插件
from django.forms import ModelForm  #代表数据库和form可以一起用
from app01 import models

class QuestionNaire_Form(Form):
    '''添加页面的Form验证'''
    title = fields.CharField(required=True,max_length=64,
                                error_messages={
                                    'required' : '问卷标题不可以为空!',
                                    'max_length' : '超过最大长度'
                                },
                                widget=widgets.Textarea(attrs={'placeholder':'请输入问卷标题','type':'text','style':'width:80%;height:100px;','class':'form-control qn_title'}))

    classlist = fields.ChoiceField(required=True,initial=1,
                                       error_messages={'required':'请选择班级'},widget=widgets.Select)

    # fields.RegexField()
    #实时更新问卷列表
    def __init__(self,*args,**kwargs):
        super(QuestionNaire_Form, self).__init__(*args,**kwargs)
        self.fields['classlist'].choices = models.ClassList.objects.values_list("id","title")



class QuestionModelForm(ModelForm):
    class Meta:
        model = models.Question
        fields = ['caption','tp']     #这两行代表  拿到当前表所有的字段
                                      #这个fields 是按照models里面写的字段格式在前端页面生成相应的东西.
        widgets={'caption':widgets.Textarea(attrs={'style':'width:600px;height:80px','class':'form-control','placeholder':'请输入问题名称'})}
class OptionModelForm(ModelForm):
    class Meta:
        model = models.Option
        fields = ['option_name','score']


