from django.urls import path

from list import views

urlpatterns = [
    path('add_list', views.add_list),
    path('quest', views.quest),
    path('set_deadline', views.set_deadline),
    path('set_publish', views.set_publish)
]
