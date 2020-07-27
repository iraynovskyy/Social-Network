from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Post, Preference

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import PostSerializer
from datetime import datetime


# Create your views here.
@api_view(["GET"])
def welcome(request):
    content = {'Message': 'Welcome! It is a Home page!'}
    return JsonResponse(content)


@api_view(["GET"])
def post_info(request):
    allposts = Post.objects.all()

    serializer = PostSerializer(allposts, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def user_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                print('Username taken')
            elif User.objects.filter(email=email).exists():
                print('email taken')
            else:
                user = User.objects.create_user(username=username, password=password1, email=email)
                user.save()
                print('user created')

        else:
            print('password not matching...')
        return Response('User is successfully created!')


@api_view(["POST", "GET"])
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return Response(f"Hello, {user}, you are logged in!")
        else:
            messages.info(request, 'invalid credentials')
            return Response(f"Please, register or enter valid credentials...")

    else:
        return Response(f"This method is not a POST method.")


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def post_creation(request):
    if request.method == "POST":
        serializer = PostSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            post = serializer.save()
            data['response'] = "successfully added a new post."
            data['title'] = post.title
        else:
            data = serializer.errors
        return Response(data)


@api_view(["POST", "GET"])
@permission_classes([IsAuthenticated])
def postpreference(request, postid, userpreference):
    print('request =', request.method)
    print('postid =', postid)
    print('userpreference =', userpreference)
    if request.method == "POST":
        eachpost = get_object_or_404(Post, id=postid)

        obj = ''
        valueobj = ''

        try:
            obj = Preference.objects.get(user=request.user, post=eachpost)
            print('obj = ', obj, 'type of obj is:', type(obj))

            valueobj = obj.value  # value of userpreference

            valueobj = int(valueobj)

            userpreference = int(userpreference)

            if valueobj != userpreference:
                obj.delete()

                upref = Preference()
                upref.user = request.user

                upref.post = eachpost

                upref.value = userpreference

                if userpreference == 1 and valueobj != 1:
                    eachpost.likes += 1
                    eachpost.dislikes -= 1
                elif userpreference == 2 and valueobj != 2:
                    eachpost.dislikes += 1
                    eachpost.likes -= 1

                upref.save()

                eachpost.save()

                context = {'eachpost': eachpost,
                           'postid': postid}

                return Response({'Message': 'User has changed his preference!',
                                 'eachpost': str(eachpost),
                                 'postid': postid})

            elif valueobj == userpreference:
                obj.delete()

                if userpreference == 1:
                    eachpost.likes -= 1
                elif userpreference == 2:
                    eachpost.dislikes -= 1

                eachpost.save()

                context = {'Message': 'User has clicked on a same button again!',
                                 'eachpost': str(eachpost),
                                 'postid': postid}

                return Response(context)




        except Preference.DoesNotExist:
            upref = Preference()

            upref.user = request.user

            upref.post = eachpost

            upref.value = userpreference

            userpreference = int(userpreference)

            if userpreference == 1:
                eachpost.likes += 1
            elif userpreference == 2:
                eachpost.dislikes += 1

            upref.save()

            eachpost.save()

            context = {'eachpost': eachpost,
                       'postid': postid}
            print('lalala', type(eachpost))
            print('lalala2', postid)

            # return Response({'Message': 'Well Done Like/Dislike!'})
            return Response({'eachpost': str(eachpost), 'postid': postid})


    else:
        eachpost = get_object_or_404(Post, id=postid)
        context = {'eachpost': eachpost,
                   'postid': postid}

        return Response({'Message': 'Well Done Like/Dislike But it is not a POST method!'})


@api_view(["POST"])
def analytics(request):
    date1 = request.GET["date_from"]
    date2 = request.GET["date_to"]

    date1 = datetime.strptime(date1, '%Y-%m-%d')
    date2 = datetime.strptime(date2, '%Y-%m-%d')

    objs = Preference.objects.all()
    count = 0
    for obj in objs:
        valueobj = obj.value  # value of userpreference
        valueobj = int(valueobj)
        obj_date = obj.date.replace(tzinfo=None)

        if valueobj == 1 and obj_date >= date1 and obj_date <= date2:
            count += 1

    print('count=', count)

    return Response(f"From {date1} to {date2} were made {count} likes.")


@api_view(["GET"])
def user_activity(request, user_id):
    if request.method == 'GET':
        user_name = User.objects.get(id=user_id)
        date_joined = user_name.date_joined
        last_login = user_name.last_login

        return JsonResponse({
                             'User name': str(user_name),
                             'date_joined': str(date_joined),
                             'last login': str(last_login)
                             })
