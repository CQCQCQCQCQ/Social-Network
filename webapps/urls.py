"""webapps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from socialnetwork import views

urlpatterns = [
    path('', views.add_post, name='home'),
    # path('login', views.login_action, name='login'),
    path('logout', views.logout_action, name='logout'),
    path('register', views.register_action, name='register'),
    path('global', views.add_post, name='global'),
    path('accounts/login/', views.login_action, name='login'),
    path('myProfile/<int:id>', views.update_profile, name='mine'),
    path('follower_stream/', views.return_following, name='follow'),
    path('photo/<int:id>', views.get_photo, name='photo'),
    path('add-post', views.add_post, name='add'),
    path('follow-update/<int:id>', views.follow_update, name='follow'),
    path('socialnetwork/add-comment/<int:post_id>', views.add_comment),
    path('follower_stream/socialnetwork/add-comment/<int:post_id>', views.add_comment),
    path('socialnetwork/refresh-global', views.refresh_global, name='refresh_global'),
    path('socialnetwork/refresh-follower', views.refresh_following, name='refresh_follower'),

]
