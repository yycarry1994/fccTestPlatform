from rest_framework import routers

from projects import views
from . import views

router = routers.SimpleRouter()
router.register(r'summary', views.SummaryViewSet, basename='summary')


urlpatterns = [

]
urlpatterns += router.urls
