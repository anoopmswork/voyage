from rest_framework import routers
from . import views

router = routers.SimpleRouter(trailing_slash=False)

router.register(r'api/account', views.AccountViewSet, base_name='account')
router.register(r'api/user', views.UserViewSet, base_name='user')
router.register(r'api/user_profile', views.UserProfileViewSet, base_name='user_profile')
router.register(r'api/geo', views.GeoViewSet, base_name='geo')
router.register(r'api/vat', views.VatViewSet, base_name='vat')
router.register(r'api/emergency', views.EmergencyContactViewSet, base_name='vat')

urlpatterns = router.urls
