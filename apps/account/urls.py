from apps.account import views
from rest_framework import routers

router = routers.SimpleRouter(trailing_slash=False)

urlpatterns = router.urls
