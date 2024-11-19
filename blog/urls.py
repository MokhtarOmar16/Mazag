
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.urls import path



urlpatterns = [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),

    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('admin/', admin.site.urls),
    
    path(r'', include('djoser.urls')),
    path(r'auth/', include('djoser.urls.jwt')),
    path('',include('core.urls'))

]
urlpatterns += static(settings.MEDIA_URL,
                        document_root=settings.MEDIA_ROOT)

if settings.DEBUG: 
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ] 
