from rest_framework import routers

from projects import views
from reports import views

router = routers.SimpleRouter()
router.register(r'reports', views.ReportsViewSet)


urlpatterns = [

]
urlpatterns += router.urls
