from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from videos import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('videos/', include('videos.urls', namespace="videos")),
    path('search/', views.search_results, name='search_results'),
    path('liked_Videos/', views.liked_videos, name='liked_videos'),
    path('subscriptions/', views.subscription_videos, name='subscription-videos'),
    path("notifications/", views.notifications, name="notifications"),
    path("notifications/mark-read/", views.mark_notifications_read, name="mark_notifications_read"),
    path('<str:username>/', views.profile, name='profile'),
    path('accounts/', include('accounts.urls', namespace="accounts")),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
