from django.urls import path
from api.views.user import (
    UserIDViewSet,
    UserBasicViewSet,
    UserLoginViewSet,
    UserPasswordViewSet, 
    UserICOKYCViewSet, 
    UserBalanceViewSet,
    UserRelationalViewSet,
)
from api.views.device import (
    DeviceIDViewSet,
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('users/id', UserIDViewSet, base_name='user_id')
router.register('users/basic', UserBasicViewSet, base_name='user_basic')
router.register('users/login', UserLoginViewSet, base_name='user_login')
router.register('users/password', UserPasswordViewSet, base_name='user_password')
router.register('users/icokyc', UserICOKYCViewSet, base_name='user_ico_kyc')
router.register('users/balance', UserBalanceViewSet, base_name='user_balance')
router.register('users/relational', UserRelationalViewSet, base_name='user_relational')

router.register('device/create', DeviceIDViewSet, base_name='device_create')

urlpatterns = router.urls