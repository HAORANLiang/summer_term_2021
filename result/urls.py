from django.urls import path, include


from result import views


urlpatterns = [
    path('save_result', views.save_result),
    path('statistic', views.statistic),
    path('', views.all_result_count),
    path('to_excel', views.to_excel),
    path('check_ans', views.check_ans)，
    path('time_line', views.time_line)
]

