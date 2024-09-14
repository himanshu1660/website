from django.urls import path
from . import views

urlpatterns= [
    path('', views.index, name='index'),
    path('settings',views.settings, name='settings'),
    path('upload',views.upload, name='upload'),
    path('like_post',views.like_post, name='like_post'),
    path('follow',views.follow, name='follow'),
    path('login',views.login, name='login'),
    path('signup',views.signup, name='signup'),
    path('logout',views.logout, name='logout'),
    path('messages', views.chats, name='chats'),
    path('bookmark', views.bookmark, name='bookmark'),
    path('bookmark_it', views.bookmark_it, name='bookmark_it'),
    path('explore', views.explore, name='explore'),
    path('profile/<str:pk>/', views.profile, name='profile'),
    path('directs/<username>', views.directs, name='directs'),
    path('SendMessage', views.SendMessage, name='send-message'),
    path('searchuser', views.SearchUser, name='searchuser'),
    path('new/<username>', views.NewMessage, name='new-message'),
    path('poststory', views.PostStory, name='poststory'),
    path('stories', views.stories, name='stories'),
    path('deletepost', views.Delete_post, name='delete-post'),
]

