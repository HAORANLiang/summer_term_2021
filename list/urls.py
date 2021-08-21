from django.urls import path



from list import views



urlpatterns = [
    path('add_list/', views.add_list)
]
