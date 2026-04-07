from django.contrib import admin
from .models import Question, Option, Quiz, UserAnswer, MCQstats, User, DjangoAdmin

# Register your models here.
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(Quiz)
admin.site.register(UserAnswer)
admin.site.register(MCQstats)
admin.site.register(User)
admin.site.register(DjangoAdmin)
