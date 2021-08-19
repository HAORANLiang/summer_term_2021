from django.urls import path, include


from jian import views

urlpatterns = [
    path('', views.jian),

]