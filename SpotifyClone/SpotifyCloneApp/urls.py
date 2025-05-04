from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('user_in/', views.user_in, name='user_in'),
    path('library/', views.library_user, name='library'),
    path('songs/', views.top_tracks_view, name='songs'),
    path('music/<str:pk>/', views.music, name='music')
]