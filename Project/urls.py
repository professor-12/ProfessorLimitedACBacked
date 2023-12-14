from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.Signup, name="Signup"),
    path("chat", views.Send_Message, name="chatApi"),
    path("users", views.Users, name="users"),
    path("message/", views.GETChatApi, name="getMessage"),
    path("contact/", views.ContactApi, name="contact"),
    path("login/", views.Login, name="Login"),
    path("contactcreation/", views.CreateContact, name="CreateContact"),
    path("editprofile", views.EditProfile, name="EditProfile"),
    path("", views.ListApi, name="ListApi"),
]
