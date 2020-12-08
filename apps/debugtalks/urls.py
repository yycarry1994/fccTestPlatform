from rest_framework import routers

from projects import views
from debugtalks import views

router = routers.SimpleRouter()
router.register(r'debugtalks', views.DebugTalksViewSet)


urlpatterns = [

]
urlpatterns += router.urls
