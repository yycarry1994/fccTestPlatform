from rest_framework import routers

from projects import views
from . import views

router = routers.SimpleRouter()
router.register(r'interfaces', views.InterfaceViewSet)


urlpatterns = [

]
urlpatterns += router.urls
