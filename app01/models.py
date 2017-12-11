from django.db import models

# Create your models here.
class UserInfo(models.Model):
    '''
    员工表
    '''
    name = models.CharField(max_length=12)
    password = models.CharField(max_length=32)

    def __str__(self):
        return self.name
class ClassList(models.Model):
    '''
	班级表
	'''
    title = models.CharField(max_length=32,verbose_name='班级名称')
    def __str__(self):
        return self.title
class Student(models.Model):
    '''
	学生表
	'''
    name = models.CharField(max_length=12,verbose_name='学生姓名')
    password = models.CharField(max_length=24,verbose_name='学生密码')
    classlist = models.ForeignKey(to=ClassList,verbose_name='学生所在班级')
    def __str__(self):
        return self.name
class QuestionNaire(models.Model):
    '''
	问卷表
	'''
    title = models.CharField(max_length=64,verbose_name='问卷标题')
    classlist = models.ForeignKey(to=ClassList,verbose_name='答问卷的班级')
    creator = models.ForeignKey(to=UserInfo,verbose_name='创建问卷的辣个银')
    def __str__(self):
        return self.title

class Question(models.Model):
    '''
	问题表
	'''
    caption = models.CharField(max_length=64,verbose_name='问题')
    question_type = (
		(1,'打分'),
		(2,'单选'),
		(3,'评价'),
	)
    tp = models.IntegerField(choices=question_type)
    questionnaire = models.ForeignKey(to=QuestionNaire,verbose_name='该问卷下的问题',default=1)
    def __str__(self):
       return self.caption


class Option(models.Model):
    '''
	单选题的选项
	'''
    option_name = models.CharField(max_length=32,verbose_name='选项名称')
    score = models.IntegerField(verbose_name='选项对应的分值')
    question = models.ForeignKey(to=Question,verbose_name='所在的问题')
    def __str__(self):
        return self.option_name

class Answer(models.Model):
    '''
	Answer my questions
	'''
    val = models.IntegerField(verbose_name='打分项的得分',null=True,blank=True)
    content = models.CharField(max_length=255,null=True,blank=True,verbose_name='评价')
    student = models.ForeignKey(to=Student,verbose_name='哪位同学答的题')
    question = models.ForeignKey(to=Question,verbose_name='答的是哪道题')
    option = models.ForeignKey(to=Option,verbose_name='单选选项',null=True)
    def __str__(self):
        return self.val