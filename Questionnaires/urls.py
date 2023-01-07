from django.urls import path
from . import views

urlpatterns = [
    path('process', views.process, name='process'),
    path('q/<int:questionnaire_id>', views.display_questionnaire, name='display_questionnaire'),
    path('reporty', views.reporty, name='reporty'),
]
