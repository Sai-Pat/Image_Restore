from django.urls import path
from . import views
from features.eye_tracking.stream import eye_tracking_stream

urlpatterns = [
    path('', views.home, name='home'),
    path('stream/eye_track/', eye_tracking_stream, name='eye_tracking_stream'),
    path('<str:feature_id>/', views.feature_view, name='feature'),
]
