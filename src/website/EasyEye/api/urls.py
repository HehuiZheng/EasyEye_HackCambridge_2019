from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = "api"

urlpatterns = [
    # ex: /polls/
    path('get_alert', views.GetAlertView.as_view(), name='get_alert'),
    path('upload_data', views.DataUploadView.as_view(), name='upload_data'),
    path('index', views.IndexView.as_view(), name='index'),
]