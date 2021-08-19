from django.urls import path
from rest_framework.routers import DefaultRouter
from divide import views

router = DefaultRouter()
# router.register('books', views.BooksViewSet)

urlpatterns = [
    path('', views.division)
]
