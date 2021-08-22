from django.urls import path

from list import views

urlpatterns = [
    path('add_list', views.add_list),
    path('quest', views.quest),
    path('set_publish', views.set_publish),
    path('set_publish_info', views.set_publish_info)
]
