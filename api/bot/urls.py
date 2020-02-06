from django.urls import path
from .views import UpdateBot

urlpatterns = [
    path('telegram', UpdateBot.as_view(), name='update'),
 
]