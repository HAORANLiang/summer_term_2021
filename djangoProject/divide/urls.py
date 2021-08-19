from django.urls import path, include
from rest_framework.routers import DefaultRouter
from djangoProject.divide import views

router = DefaultRouter()
# router.register('books', views.BooksViewSet)

urlpatterns = [
    path('division/', views.division())
]
