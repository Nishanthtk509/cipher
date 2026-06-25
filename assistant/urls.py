from django.urls import path,re_path
from . views import*
from . import views

urlpatterns = [
    path('',views.Register, name="register"),
    path('login',views.user_login, name="login"),
    path('logout', views.logout, name="logout"),
    path('chat',views.chatbot, name="chatbot"),
    path('knowledge/',views.KnowledgeView, name="knowledge"),
    path("knowledge/edit/<int:id>/",EditKnowledge,name="edit_knowledge"),
    path("knowledge/delete/<int:id>/",DeleteKnowledge, name="delete_knowledge"),
    path("adminlogin/",admin_login,name="admin_login"),
    path("adminlogout/",admin_logout,name="admin_logout"),
    re_path(r"^.*$", views.chatbot),

]
