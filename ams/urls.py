
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth', include('accounts.urls')),
    path('', include('core.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('dashboard/church_us/', include('church.urls')),
    path('dashboard/distric_us/', include('district.urls')),
    path('dashboard/conf_us/', include('conference.urls')),
]
