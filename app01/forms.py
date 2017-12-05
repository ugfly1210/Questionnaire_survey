from django.forms import Form, fields, widgets
from app01 import models
class QuestionNaire_Form(Form):
    '''添加页面的Form验证'''
    title = fields.CharField(required=True,max_length=64,
                                error_messages={
                                    'required' : '问题不可以为空!',
                                    'max_length' : '超过最大长度'
                                },
                                widget=widgets.Textarea(attrs={'placeholder':'请输入您的问题','type':'text','style':'width:80%;height:100px;'}))

    question_type = fields.ChoiceField(
        required=True,initial=1,error_messages={'required':'请选择问题类型'},widget=widgets.Select)
    #实时更新问卷列表
    def __init__(self,*args,**kwargs):
        super(QuestionNaire_Form, self).__init__(*args,**kwargs)
        self.fields['question_type'].choices = models.Question.question_type



