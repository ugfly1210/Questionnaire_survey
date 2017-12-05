from django.contrib import admin

# Register your models here.
from app01.models import *

admin.site.register(UserInfo)
admin.site.register(ClassList)
admin.site.register(Student)
admin.site.register(QuestionNaire)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(Answer)

