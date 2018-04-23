from api.views.user import (
    UserIDViewSet,
    UserRegisterViewSet,
    UserUpdateViewSet,
    UserLoginViewSet,
    UserPasswordViewSet, 
    UserICOKYCViewSet, 
    UserBalanceViewSet,
    UserRelationalViewSet,
)
from api.views.device import (
    DeviceIDViewSet,
)
from api.views.social_media_post import (
    SocialMediaPostViewSet,
)
from api.views.file import (
    FileUploadViewSet,
)
from api.views.homepage import homepage
from rest_framework.routers import DefaultRouter
from django.urls import path

router = DefaultRouter()

router.register('users/id', UserIDViewSet, base_name='user_id')
router.register('users/basic', UserRegisterViewSet, base_name='user_register')
router.register('users/update', UserUpdateViewSet, base_name='user_update')
router.register('users/login', UserLoginViewSet, base_name='user_login')
router.register('users/password', UserPasswordViewSet, base_name='user_password')
router.register('users/icokyc', UserICOKYCViewSet, base_name='user_ico_kyc')
router.register('users/balance', UserBalanceViewSet, base_name='user_balance')
router.register('users/relational', UserRelationalViewSet, base_name='user_relational')

router.register('device/create', DeviceIDViewSet, base_name='device_create')

router.register('proof-of-love', SocialMediaPostViewSet, base_name='proof_of_love')

router.register('files', FileUploadViewSet, base_name='files')

urlpatterns = router.urls + [path('home/', homepage, name='index')]