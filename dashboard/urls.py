from django.conf import settings
from django.urls import path
from . import views
from django.conf.urls.static import static

app_name='dashboard'

urlpatterns = [
    path('dash/', views.dash, name='dash'),    
    path('articles/', views.tous_articles, name='articles'),
    path('ajouter_article/', views.ajouter_article, name='ajouter_article')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)