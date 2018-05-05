"""astraweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from api.permissions import APIUserPermission
from .views import redirect_root

schema_view = get_schema_view(
   openapi.Info(
      title="Astra API",
      default_version='v1',
      description="A RESTful API to expose functionality for Astra products",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="skale1@berkeley.edu"),
      license=openapi.License(name="BSD License"),
   ),
   validators=['flex', 'ssv'],
   public=True,
   permission_classes=(APIUserPermission,),
)

urlpatterns = [
    path('', redirect_root),
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    re_path('swagger(.json|.yaml)', schema_view.without_ui(cache_timeout=None), name='schema-json/yaml'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=None), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=None), name='schema-redoc'),
    path('api/', include('api.urls')),
    path('auth/', include('rest_framework.urls')),
    path('admin/', admin.site.urls),
]   
