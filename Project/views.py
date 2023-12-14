from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from .serializers import *
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db.models import Q
from .pusher import pusher_client
from django.shortcuts import get_object_or_404, get_list_or_404




@api_view(["GET"])
def ListApi(req):
    urls = ("signup/","chat","users","message","contact","login","contactcreation","editprofile",)
    return Response(urls)

@api_view(['POST'])
def Signup(req):
    serialized_data = User_serializer(data=req.data)
    if serialized_data.is_valid():
        serialized_data.save()
        user = User.objects.get(username=req.data["username"])
        user.set_password(req.data["password"])
        user.save()
        profile_data = {
            "displayname": user.username,
            "user": user.pk,
            "email": req.data["email"],
            "user_profile": req.data["username"],
        }

        profile_serializer = Profile_serializer(data=profile_data)
        if profile_serializer.is_valid():
            profile_serializer.save()
        token = Token.objects.create(user=user)
        response = {"token": token.key,
                    "user": serialized_data.data, "profile": profile_data}
        return Response(response, status=status.HTTP_201_CREATED)
    return Response(serialized_data.error_messages, status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(["POST"])
def Login(req):
    user_login = get_object_or_404(User, username=req.data["username"])
    if not user_login.check_password(req.data["password"]):
        return Response("NOT FOUND", status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user_login)
    profile = get_object_or_404(Profile, user=user_login)
    serialized_login = User_serializer(user_login, many=False)
    serialized_profile = Profile_serializer(profile, many=False)
    response = {"token": token.key, "profile": serialized_profile.data,
                "user": serialized_login.data}
    return Response(response, status=status.HTTP_200_OK)


@api_view(["GET"])
def Users(req):
    user = Profile.objects.all()
    serialized_user = Profile_serializer(user, many=True)
    return Response(serialized_user.data)


@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def Send_Message(req):
    req.data["sender"] = get_object_or_404(
        User, username=req.user.username).id
    message = Chat_serializer(data=req.data)

    if message.is_valid():
        message.save()
        chat = Chat.objects.filter(Q(sender=req.data["sender"], reciever=req.data["reciever"]) | Q(
            sender=req.data["reciever"], reciever=req.data["sender"])).order_by('date')
        const = Chat_serializer(chat, many=True)
        pusher_client.trigger(u'chat', u'message',
                              const.data)
        return Response(message.data)
    return Response(message.error_messages)


@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def GETChatApi(req):
    if req.method == "POST":
        sender = get_object_or_404(User, username=req.user.username)
        reciever = get_object_or_404(User, username=req.data["reciever"])
        profile = get_object_or_404(Profile, user=reciever)
        message = Chat.objects.filter(Q(sender=sender, reciever=reciever) | Q(
            sender=reciever, reciever=sender)).order_by('date')
        const = Chat_serializer(message, many=True)
        friendprofileserializer = Profile_serializer(profile)
        return Response({"messageinfo": const.data, "friendprofile": friendprofileserializer.data})


@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def ProfileApi(req):
    user = get_object_or_404(User, username=req.user.username)
    Data = get_object_or_404(Profile, user=user)
    Data.email = user.email
    serializedData = Profile_serializer(Data)
    return Response(serializedData.data)


@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def ContactApi(req):
    if  req.method == "GET": 
        profileuserlist = []
        user = get_object_or_404(User, username=req.user.username).id
        contact = Contacts.objects.filter(Q(user=user))
        for i in contact:
            coontactprofile = get_object_or_404(User, username=i.contact)
            print(coontactprofile)
            profile = get_object_or_404(Profile, user=coontactprofile)
            profileuserlist.append(profile)
        profileserializer = Profile_serializer(profileuserlist, many=True)
        return Response(profileserializer.data)


@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def CreateContact(req):
    user = get_object_or_404(
        User, username=req.user.username).pk
    contact = get_object_or_404(
        User, pk=req.data["contact"])
    usercontact = Contacts.objects.filter(user=user)
    serializecontact = Contact_serializer(usercontact, many=True)
    for i in serializecontact.data:
        print(contact.pk)
        if i["contact"] == contact.pk:
            return Response("User is already your contact")

    Data = {
        "user": user,
        "contact": contact.id
    }
    contactserializers = Contact_serializer(
        data={"user": contact.id, "contact": user})
    contactserializer = Contact_serializer(data=Data)
    if contactserializer.is_valid():

        contactserializer.save()
    if contactserializers.is_valid():
        if Data["user"] != Data["contact"]:
            contactserializers.save()
            return Response("Contact added succesfully")
    return Response(contactserializer.errors)


@api_view(["PUT"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def EditProfile(req):
    user = get_object_or_404(
        User, username=req.user.username)
    profiles = get_object_or_404(Profile, user=user.id)
    profiles.email = req.user.email
    req.data["user"] = user.id
    profile = Profile_serializer(instance=profiles, data=req.data)
    if profile.is_valid():
        profile.save()
        userprofile = Profile_serializer(profiles, many=False)
        pusher_client.trigger(u'chat', u'profile', userprofile.data)
        return Response("Successful")
    return Response(profile.errors)
