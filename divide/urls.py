from django.urls import path

from divide import views


# router.register('books', views.BooksViewSet)

urlpatterns = [
    path('', views.division)
]
