from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('user/chats/', views.UserChatsView.as_view(), name='user-chats'),
    path('chats/<int:chat_id>/mark-messages-as-read/', views.MarkMessagesAsReadView.as_view(), name='mark-messages-as-read'),
    path('chats/create/', views.CreateOrActivateChatView.as_view(), name='create-or-activate-chat'),
    path('chat/<int:chat_id>/details/', views.ChatDetailsView.as_view(), name='chat-messages'),
    path('chat/<int:chat_id>/messages/send/', views.SendMessageView.as_view(), name='send-message'),
    path('chats/<int:chat_id>/delete/', views.DeleteChatView.as_view(), name='delete-chat'),
    path('message/delete-for-me/<int:message_id>/', views.DeleteMessageForMeView.as_view(), name='delete-message-for-me'),
    path('message/delete-for-everyone/<int:message_id>/', views.DeleteMessageForEveryoneView.as_view(), name='delete-message-for-everyone'),
    path('block/user/<int:user_id>/', views.BlockUserView.as_view(), name='block-user'),
    path('unblock/user/<int:user_id>/', views.UnBlockUserView.as_view(), name='unblock-user'),
]
