from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *
urlpatterns = [
    path('get-user-from-jwt/', get_user_from_jwt, name='get-user-from-jwt'),
    path('user_registration/', user_gp_controller),
    path('user_registration/<int:pk>/', user_gpd_controller),
    path('session_controller/', session_gp_controller),
    path('session_controller/<int:pk>/', session_gpd_controller),
    path('upload_image', predict_ml_model, name='predict_ml_model')
]

# urlpatterns = format_suffix_patterns(urlpatterns)
