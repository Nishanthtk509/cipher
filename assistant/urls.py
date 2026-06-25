from django.urls import path
from . views import*
from . import views

urlpatterns = [
    path('',views.Register, name="register"),
    path('login',views.login, name="login"),
    path('chat',views.chatbot, name="chatbot"),
    path('knowledge/',views.KnowledgeView, name="knowledge"),
    path("knowledge/edit/<int:id>/",EditKnowledge,name="edit_knowledge"),
    path("knowledge/delete/<int:id>/",DeleteKnowledge, name="delete_knowledge"),

]
