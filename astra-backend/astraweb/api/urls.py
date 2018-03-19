from api.views.user import (
    UserIDViewSet,
    UserBasicViewSet,
    UserUpdateViewSet,
    UserLoginViewSet,
    UserPasswordViewSet, 
    UserICOKYCViewSet, 
    UserAirDropsViewSet,
    UserBalanceViewSet,
    UserRelationalViewSet,
)
from api.views.device import (
    DeviceIDViewSet,
)
from api.views.social_media_post import (
    SocialMediaPostViewSet,
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('users/id', UserIDViewSet, base_name='user_id')
router.register('users/basic', UserBasicViewSet, base_name='user_basic')
router.register('users/update', UserUpdateViewSet, base_name='user_update')
router.register('users/login', UserLoginViewSet, base_name='user_login')
router.register('users/password', UserPasswordViewSet, base_name='user_password')
router.register('users/icokyc', UserICOKYCViewSet, base_name='user_ico_kyc')
router.register('users/airdrops', UserAirDropsViewSet, base_name='user_air_drops')
router.register('users/balance', UserBalanceViewSet, base_name='user_balance')
router.register('users/relational', UserRelationalViewSet, base_name='user_relational')

router.register('device/create', DeviceIDViewSet, base_name='device_create')

router.register('proof-of-love', SocialMediaPostViewSet, base_name='proof_of_love')

urlpatterns = router.urls