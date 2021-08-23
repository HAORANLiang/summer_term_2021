from django.urls import path


from owner import views


urlpatterns = [
    path('sort', views.get_list),
    path('to_recycle', views.to_recycle),
    path('get_recycle_list', views.get_recycle_list)
]
