from django.conf import settings
from django.urls import path
from . import views
from django.conf.urls.static import static

app_name = 'user'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('signup/', views.register_user, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('settings/', views.settings, name='settings'),
    path('confidentialite/', views.confidentialite, name='confidentialite'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('change-password/', views.change_password, name='change_password'),
    path('setting_profile/', views.setting_profile, name='setting_profile' ),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)