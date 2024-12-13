
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView



urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),     
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    path('admin/', admin.site.urls), # admin endpoint 
    
    # user endpoints 
    path('auth/', include('djoser.urls.jwt')), # Djoser endpoints 
    path('', include('users.urls')),  
    

] 

if settings.DEBUG: 
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include("debug_toolbar.urls")),
    ] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

