from django.contrib import admin
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path
from django.views.generic import TemplateView

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework import permissions

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
]

schema_view = get_schema_view(
    openapi.Info(
        title="Yatube API",
        default_version='v1',
        description="Документация для приложения Yambd",
        contact=openapi.Contact(email="yamdb17@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
    url(r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)