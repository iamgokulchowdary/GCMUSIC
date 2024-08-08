from django.urls import path
from .views import *

app_name = "databaseapp"

urlpatterns = [
    path('', StartDBView, name='startdbview')
]