
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("users/admin/", admin.site.urls),
    path('users/api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('users/docs/', SpectacularSwaggerView.as_view(url_name='schema')),
    path('users/api/v1/users/', include('users.urls'))
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
