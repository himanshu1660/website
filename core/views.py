from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile, Post, Like_post, FollowerCount, Bookmarks, Message, Stories
from django.db.utils import IntegrityError
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Q, Prefetch




# Create your views here.
@login_required(login_url='login')
def index(request):
    user_profile=Profile.objects.get(user=request.user)
    posts=Post.objects.all()
    like_filter = Like_post.objects.filter(username=request.user.username).values_list('post_id', flat=True)
    bookmark_filter = Bookmarks.objects.filter(username=request.user.username).values_list('post_id', flat=True)
    all_stories = Stories.objects.all()
    
    first_story_per_user = {}
    
    # Filtering stories to include only the first story for each user
    for story in all_stories:
        if story.user not in first_story_per_user:
            first_story_per_user[story.user] = story
    
    # Creating a list of stories from the dictionary values
    stories = list(first_story_per_user.values())
    context = {
        'user_profile':user_profile,
        'posts':posts, 
        'stories':stories,
        'bookmark_filter':bookmark_filter,
        'like_filter':like_filter
    }
    return render(request, 'index.html', context)

def signup(request):
   if request.method=='POST':
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']

        if password==confirm_password:
            if User.objects.filter(email=email).exists():
                messages.info(request,'Email already taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request,'Username already taken')
                return redirect('signup')
            else:
                user=User.objects.create_user(username = username, email=email, password=password)
                user.first_name=firstname
                user.last_name=lastname
                user.save()

                user_login=auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                user_model=User.objects.get(username=username)
                new_profile= Profile.objects.create(user=user_model)
                new_profile.save()
                return redirect('settings')
        else:
            messages.info(request,'Password not matching')
            return redirect('signup')
   else:
    return render(request, 'signup.html')

def login(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']

        user=auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'login.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return render(request,'login.html')

@login_required(login_url='login')
def settings(request):
    user_profile=Profile.objects.get(user=request.user)

    if request.method=='POST':

        if request.FILES.get('image')==None:
            image=user_profile.profileimg
            bio = request.POST['bio']
            location=request.POST['location']

            user_profile.profileimg=image
            user_profile.bio=bio.capitalize()
            user_profile.location=location.capitalize()
            user_profile.save()
        
        if request.FILES.get('image') != None:
            image=request.FILES.get('image')
            bio = request.POST['bio']
            location=request.POST['location']

            user_profile.profileimg=image
            user_profile.bio=bio.capitalize()
            user_profile.location=location.capitalize()
            user_profile.save()
        
        if request.POST['bio'] == "":
            image=user_profile.profileimg
            bio = user_profile.bio
            location=request.POST['location']

            user_profile.profileimg=image
            user_profile.bio=bio.capitalize()
            user_profile.location=location.capitalize()
            user_profile.save()

        return redirect('index')
    return render(request, 'settings.html',{'user_profile':user_profile})

def upload(request):
    if request.method=='POST':
        user= request.user.username
        image=request.FILES.get('image')
        caption=request.POST['caption']

        new_post=Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()

        return redirect('/')
    else:
        return redirect('/')

def Delete_post(request):
    user = request.user.username
    post_id = request.GET.get('post_id')
    delete_post=Post.objects.filter(id=post_id).delete()
    success = 'object deleted successfully'
    return redirect(request.META.get('HTTP_REFERER', '/'))

def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')
    like = ''
    post = Post.objects.get(id=post_id)
    like_filter = Like_post.objects.filter(post_id=post_id, username=username).first()

    if like_filter is None:
        new_like = Like_post.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes + 1
        post.save()
        like = 'liked'

    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes - 1
        post.save()
        like = 'disliked'
    return HttpResponse(like)
    








    

@login_required(login_url='login')
def explore(request):
    user_profile=Profile.objects.get(user=request.user)
    return render(request, 'explore.html',{'user_profile':user_profile})

# ------------------------START BOOKMARKS-------------------------------
@login_required(login_url='login')
def bookmark_it(request):
    username = request.user.username
    post_id = request.GET.get('post_id')
    bookmark = ''
    # Check if a bookmark exists for the user and post_id
    try:
        bookmarked = Bookmarks.objects.get(username=username, post_id=post_id)
        # If bookmark exists, delete it
        bookmarked.delete()
        bookmark = 'notbookmarked'
    except Bookmarks.DoesNotExist:
        # If bookmark doesn't exist, create a new one
        try:
            new_bookmark = Bookmarks.objects.create(username=username, post_id=post_id)
            new_bookmark.save()
            bookmark = 'bookmarked'
        except IntegrityError:
            # If there's an integrity error (possibly due to duplicate entry), handle it
            pass
    return HttpResponse(bookmark)

def bookmark(request):
    user_profile = Profile.objects.get(user=request.user)
    username = request.user.username
    bookmarked_posts = Bookmarks.objects.filter(username=username)
    like_filter = Like_post.objects.filter(username=request.user.username).values_list('post_id', flat=True)
    bookmark_filter = Bookmarks.objects.filter(username=request.user.username).values_list('post_id', flat=True)
    bookmarked_posts_details = []
    for bookmark in bookmarked_posts:
        try:
            post = Post.objects.get(id=bookmark.post_id)
            bookmarked_posts_details.append(post)
        except Post.DoesNotExist:
            # Handle the case where the bookmarked post doesn't exist
            # For example, you can skip this bookmarked post or log the error
            pass
    context = {
        'user_profile': user_profile, 
        'bookmarked_posts': bookmarked_posts_details,
        'like_filter':like_filter,
        'bookmark_filter': bookmark_filter
    }
    return render(request, 'bookmark.html', context)

# ------------------------END BOOKMARKS-------------------------------


@login_required(login_url='login')
def profile(request, pk):
    user_object = get_object_or_404(User, username=pk)
    others_profile = get_object_or_404(Profile, user=user_object)
    user_posts= Post.objects.filter(user=pk)
    no_of_posts = len(user_posts)
    user_profile=Profile.objects.get(user=request.user)

    like_filter = Like_post.objects.filter(username=request.user.username).values_list('post_id', flat=True)
    bookmark_filter = Bookmarks.objects.filter(username=request.user.username).values_list('post_id', flat=True) 

    followers_count = FollowerCount.objects.filter(user=user_object)
    followers = [follower.follower for follower in followers_count]
    followers_objects = User.objects.filter(username__in=followers)

    followings_count = FollowerCount.objects.filter(follower=user_object)
    followings = [following.user for following in followings_count]
    followings_objects = User.objects.filter(username__in=followings)

    

    follower=request.user.username
    user = pk
    if FollowerCount.objects.filter(follower=follower, user=user):
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'

    user_followers=len(FollowerCount.objects.filter(user=pk))
    user_following=len(FollowerCount.objects.filter(follower=pk))

    context = {
        'user_object': user_object,
        'others_profile': others_profile,
        'user_posts':  user_posts,
        'no_of_posts': no_of_posts,
        'user_profile': user_profile,
        'button_text': button_text,
        'user_followers': user_followers,
        'user_following': user_following,
        'followers': followers_objects,
        'followings': followings_objects,
        'like_filter':like_filter,
        'bookmark_filter': bookmark_filter
    }
    return render(request, 'profile.html', context)


@login_required(login_url='login')
def follow(request):
    follower = request.user.username
    user = request.GET.get('user')

    if FollowerCount.objects.filter(user=user, follower=follower).first():
        delete_follower= FollowerCount.objects.get(follower=follower, user=user)
        delete_follower.delete()
    else:
        new_follower = FollowerCount.objects.create(follower=follower, user=user)
        new_follower.save()

    return redirect('/profile/' + user)


# -------------------START MESSAGES-----------------
@login_required(login_url='login')
def chats(request): 
    user_profile=Profile.objects.get(user=request.user)
    user=request.user
    messages = Message.get_message(user=user)
    active_direct = None
    directs = None

    if messages:
        message = messages[0]
        active_direct = message['user'].username
        directs = Message.objects.filter(user=user, reciepient=message['user'])
        directs.update(is_read=True)

        for message in messages:
            if message['user'].username == active_direct:
                message['unread'] = 0
    context = {
        'directs': directs,
        'messages': messages,
        'active_direct': active_direct,
        'user_profile':user_profile,
    }
    return render(request, 'messages.html', context)

def directs(request, username):
    user_profile=Profile.objects.get(user=request.user)
    user_object=User.objects.get(username = username)
    others_profile = Profile.objects.get(user=user_object)
    
    user= request.user
    messages =  Message.get_message(user=user)
    active_direct = username
    directs = Message.objects.filter(user=user, reciepient__username = username)
    directs.update(is_read=True)

    for message in messages:
        if message['user'].username == username:
            message['unread'] = 0
    context = {
        'directs': directs,
        'messages': messages,
        'active_direct': active_direct,
        'user_object': user_object,
        'others_profile': others_profile,
        'user_profile': user_profile,
    }
    return render(request, 'directs.html', context)

def SendMessage(request):
    from_user = request.user
    to_user_username = request.POST.get('to_user')
    body = request.POST.get('body')

    if request.method == "POST":
        to_user = User.objects.get(username=to_user_username)
        Message.send_message(from_user, to_user, body)
        success = 'Message sent'
        return HttpResponse(success)


def NewMessage(request, username):
    from_user = request.user
    body = ''
    try:
        to_user = User.objects.get(username=username)
    except Exception as e:
        return redirect('searchuser')
    if from_user != to_user:
        Message.send_message(from_user, to_user, body)
    return redirect('chats')

# -------------------END MESSAGES-----------------


def SearchUser(request):
    user_profile = Profile.objects.get(user=request.user)
    query = request.POST.get('search')
    if query:
        users = User.objects.filter(Q(username__icontains=query))
        paginator = Paginator(users, 8)
        page_number = request.GET.get('page')
        users_paginator = paginator.get_page(page_number)
    else:
        users_paginator = []

    return render(request, 'searchuser.html', {'users': users_paginator, 'user_profile': user_profile, 'query': query})



def PostStory(request):
    if request.method=='POST':
        user= request.user.username
        story_image=request.FILES.get('story_image')

        new_story=Stories.objects.create(user=user, story_image=story_image)
        new_story.save()

        return redirect('/')
    else:
        return redirect('/')
    
def stories(request):
    user_profile = Profile.objects.get(user=request.user)
    all_stories = Stories.objects.all()
    return render(request, 'stories.html', {'user_profile': user_profile, 'all_stories':all_stories})