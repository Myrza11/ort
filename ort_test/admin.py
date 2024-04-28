from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Subject)
admin.site.register(Topics)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Test)
admin.site.register(TestQuestion)
admin.site.register(Results)
admin.site.register(ResultAnswer)