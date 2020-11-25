from django.urls import path, re_path
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token
from users import views
from rest_framework import routers
import re


router = routers.SimpleRouter()
router.register(r'users', views.Users)
# router.register(r'users', views.Count)

urlpatterns = [
    path('login/', obtain_jwt_token),
    path('user/<str:email>/count', views.Count.as_view({'get': 'list_0'})),
    path('user/<str:username>/count', views.Count.as_view({'get': 'list_1'}))
]

urlpatterns += router.urls