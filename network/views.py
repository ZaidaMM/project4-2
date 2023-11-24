from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator

from .models import Post, User, Follow


def index(request):
    # *******
    posts = Post.objects.all().order_by('id').reverse()

    # Pagination, show 10 psots per page
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        'posts': posts,
        'page_obj': page_obj
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

# *****************

def compose(request):
    # Compose new post
    if request.method == "POST":
        body = request.POST['compose-body']
        user = User.objects.get(pk=request.user.id)
        post = Post(body = body, author = user)
        post.save()
        
        return HttpResponseRedirect(reverse('index'))
    
    else:
        return JsonResponse({"error": "POST request required"}, status=400)
    
    
def profile(request, user_id):
    user = User.objects.get(pk=user_id)

    # Filter posts by user
    posts = Post.objects.filter(author=user).order_by('id').reverse()

    follower = Follow.objects.filter(follower=user)
    following = Follow.objects.filter(following=user)


    # isFollowing = False
   
    try:
        # check = follower.filter(user=User.objects.get(pk=request.user.id))
        if len(follower.filter(user=User.objects.get(pk=request.user.id))) == 0:
            isFollowing = False
        else:
            isFollowing = False
    
    except:
        isFollowing = False

    # Pagination, show 10 posts per page
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)



    return render(request, "network/profile.html", {
        'posts': posts,
        'page_obj': page_obj,
        'username': user.username,
        'profile_owner': user,
        'isFollowing': isFollowing,
        'following': following,
        'follower': follower,
    })

def following(request):
    user = User.objects.get(pk=request.user.id)
    followingUsers = Follow.objects.filter(follower=user)

    # Filter posts by user
    posts = Post.objects.all().order_by('id').reverse()  

    follPosts = []

    for post in posts:
        for person in followingUsers:
            if person.following == post.author:
                follPosts.append(post)

    # Pagination, show 10 posts per page
    paginator = Paginator(follPosts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/following.html", {
        'page_obj': page_obj,
        'username': user,
    })

def follow(request):
    userUnfollow = request.POST['follow']
    currentUser = User.objects.get(pk=request.user.id)
    followerInput = User.objects.get(username=userUnfollow)
    foll = Follow(follower=currentUser, following=followerInput)
    foll.save()
    user_id = followerInput.id

    return HttpResponseRedirect(reverse(profile, kwargs={'user_id': user_id}))

def unfollow(request):
    userUnfollow = request.POST['unfollow']
    currentUser = User.objects.get(pk=request.user.id)
    followerInput = User.objects.get(username=userUnfollow)
    foll = Follow.objects.get(follower=currentUser, following=followerInput)
    foll.delete()
    user_id = followerInput.id

    return HttpResponseRedirect(reverse(profile, kwargs={'user_id': user_id}))
