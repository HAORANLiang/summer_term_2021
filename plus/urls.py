from django.urls import path

from plus import views



# router.register('books', views.BooksViewSet)

urlpatterns = [
    path('', views.plus)
]