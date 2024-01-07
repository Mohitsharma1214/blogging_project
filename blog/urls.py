from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('user_home/', views.user_home, name='user_home'),
    path('admin_home/', views.admin_home, name='admin_home'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('create_post/', views.create_post, name='create_post'),
    path('edit_post/<int:post_id>/', views.edit_post, name='edit_post'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('logout/', views.logout_view, name='logout'),
    path('upload/image', views.upload_image, name='upload_image'),
]