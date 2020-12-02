from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('map.urls')),
    path('api/members/', include('member.api.urls')),
]
