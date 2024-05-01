from django.contrib import admin

from .models import Quiz
from .models import Question
from .models import Option

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Option)

