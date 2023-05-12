from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('', include("Goodreads.urls"), name="goodreads"),
    path('users/', include("users.urls"), name="users"),
    path('api/', include("api.urls"), name="api")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)