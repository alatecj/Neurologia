from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('logout', views.logout_view, name="logout"),
    path('login', views.login_view, name="login"),
    path('add_patient', views.add_patient, name="add_patient"),
    path('process', views.process, name='process'),
    path('q/<int:questionnaire_id>', views.display_questionnaire, name='display_questionnaire'),
    path('reporty', views.get_report, name='get_report'),
    path('show_report/<int:exam_id>', views.show_report, name='show_report'),
]
