from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Chat(models.Model):
    message = models.TextField(
        max_length=99999999999999999999999999999, blank=True)
    img = models.ImageField(blank=True, upload_to="chatimg/%y")
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sender")
    reciever = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reciever")
    date = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)
    time = models.TimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.sender.username


class Contacts(models.Model):
    contact = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="contact", blank=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user")

    def __str__(self):
        return self.user.username


class Profile(models.Model):
    bio = models.CharField(default="A bio", max_length=50)
    profilepics = models.ImageField(upload_to="img/%y", default="default.png")
    email = models.CharField(max_length=100, blank=True)
    location = models.CharField(default="Earth", max_length=20)
    user_profile = models.CharField(max_length=100, default="User_profile")
    displayname = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    online = models.BooleanField(default=False)
    def __str__(self):
        return self.user.username


class Group(models.Model):
    name = models.CharField(max_length=100)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="group_admin")
    participant = models.ManyToManyField(User)
    groupProfile = models.ImageField(
        upload_to="groupimg/%y", default="default.png")
    date_created = models.DateField(auto_now_add=True)
    admin = models.ManyToManyField(to=User, related_name='admin')

    def __str__(self):
        return self.name


class GroupChat(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    message = models.TextField(max_length=1000000000)
    senders = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    timesent = models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.group.name
