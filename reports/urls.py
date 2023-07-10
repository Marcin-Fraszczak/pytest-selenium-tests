from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
	path('', views.HomeView.as_view(), name='home'),
	path('report/', views.ReportView.as_view(), name='report'),
]