from django.urls import path
from . import views

urlpatterns = [
    path('postEvent', views.post_event),
]