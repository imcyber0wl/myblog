from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.main, name="main"),
    path('article/<int:num>/', views.article),
    path('edit-article/<int:num>/', views.edit_article,name="edart"),
    path('like/',views.like, name="like"),
    path('new-article/',views.write, name="write"),

    path('myprofile/', views.myprofile, name="profile"),
    path('myprofile/edit/', views.edit_profile, name="edit"),
        
    path('login/', views.login_view, name="login"),  
    path('logout/', views.logout_view, name="logout"),
    path('register/', views.register, name="register"),  
    path('admin/', admin.site.urls),
]
