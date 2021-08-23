from django.urls import path

from list import views

urlpatterns = [
    path('add_list', views.add_list),
    path('quest', views.quest),
    path('verify_quest', views.verity_quest),
    path('set_publish', views.set_publish),
    path('set_publish_info', views.set_publish_info),
    path('get_publish_info', views.get_publish)
]
