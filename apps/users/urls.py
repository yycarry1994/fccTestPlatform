from django.urls import path, re_path
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token
from users import views
from rest_framework import routers
import re


router = routers.SimpleRouter()
router.register(r'user', views.Users)
# router.register(r'users', views.Count)

urlpatterns = [
    path('login/', obtain_jwt_token),
    re_path(r'^user/(?P<email>([\w]+\.*)([\w]+)\@[\w]+\.\w{3}(\.\w{2}|))/count$', views.Count.as_view({'get': 'list_0'})),
    re_path(r'^user/(?P<username>\w{6,20})/count$', views.Count.as_view({'get': 'list_1'}))
]
urlpatterns += router.urls

