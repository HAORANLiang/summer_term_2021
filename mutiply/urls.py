from django.urls import path, include


from mutiply import views

urlpatterns = [
    path('', views.mutiply),

]