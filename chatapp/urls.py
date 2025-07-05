from django.urls import path

from . import views
urlpatterns = [
    path('chat/', views.OpenAIChatView.as_view(),name='chat')
]
