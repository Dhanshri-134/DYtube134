from django.urls import path

from . import views

app_name = "videos"


urlpatterns = [
    path('video/<int:id>/', views.video, name='video'),
    path('add_video/', views.add_video, name='add_video'),
    path('comment/', views.comment, name='comment'),
    path('remove/', views.remove, name='remove'),
    path('edit_video/<int:id>/', views.edit_video, name='edit_video'),
    path('delete_video/<int:id>/', views.delete_video, name='delete_video'),
    path('delete_video_confirmation/<int:id>/', views.delete_video_confirmation, name='delete_video_confirmation'),
    path('search/', views.search_results, name='search_results'),
]
