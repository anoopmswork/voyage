from rest_framework import routers
from . import views

router = routers.SimpleRouter(trailing_slash=False)

router.register(r'api/account', views.AccountViewSet, base_name='account')
router.register(r'api/user', views.UserViewSet, base_name='user')

urlpatterns = router.urls
