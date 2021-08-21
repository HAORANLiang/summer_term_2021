from django.urls import path
from rest_framework.routers import DefaultRouter


from list import views


router = DefaultRouter()

urlpatterns = [
    path('add_list/', views.add_list)
]
