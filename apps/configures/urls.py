from rest_framework import routers

from projects import views
from . import views

router = routers.SimpleRouter()
router.register(r'configures', views.ConfiguresViewSet)


urlpatterns = [

]
urlpatterns += router.urls
