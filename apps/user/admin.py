from .models.user import User
from .models.answered import  Answer
from django.contrib import admin
admin.site.register(User)
admin.site.register(Answer)

