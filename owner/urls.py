from django.urls import path


from owner import views


urlpatterns = [
    path('sort', views.get_list),
    path('to_recycle', views.to_recycle)
]
