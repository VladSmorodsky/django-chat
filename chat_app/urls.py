from django.urls.conf import path

from chat_app import views

urlpatterns = [
    path('', views.chat_view, name='index'),
    path('login/', views.login_view, name='login'),
    path('<int:chat_id>/', views.chat_room_view, name='chat_room'),
    path('<int:chat_id>/edit/', views.edit_chat_room, name='chat_room_edit'),
]