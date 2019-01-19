from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = "home"

urlpatterns = [
    # ex: /polls/
    path('get_alert', views.GetAlertView.as_view(), name='get_alert'),
]