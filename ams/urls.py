
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.static import serve



urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth', include('accounts.urls')),
    path('', include('core.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('dashboard/church_us/', include('church.urls')),
    path('dashboard/distric_us/', include('district.urls')),
    path('dashboard/conf_us/', include('conference.urls')),
    path('dashboard/admin_user/', include('reports.urls')),

    # password reset
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name = 'pages/password_reset.html'), name='password_reset' ),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name= 'pages/password_reset_done.html'), name='password_reset_done' ),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="pages/password_reset_confirm.html"), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name="pages/password_reset_complete.html"), name='password_reset_complete '),

]

