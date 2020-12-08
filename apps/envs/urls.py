from rest_framework import routers

from projects import views
from . import views

router = routers.SimpleRouter()
router.register(r'envs', views.EnvsViewSet)


urlpatterns = [

]
urlpatterns += router.urls
