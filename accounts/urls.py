from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = "accounts"

urlpatterns = [
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.user_registration, name="register"),
    path('profile/', views.edit_profile, name="edit_profile"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
