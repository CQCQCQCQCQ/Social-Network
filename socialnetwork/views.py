from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404, HttpResponse
from django.urls import reverse
from django.core import serializers

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.utils.dateparse import parse_datetime
from django.views.decorators.csrf import ensure_csrf_cookie

from django.utils import timezone

from socialnetwork.forms import LoginForm, RegistrationForm, ProfileForm, PostForm
from socialnetwork.models import Profile, Post, Comment

from datetime import datetime


@ensure_csrf_cookie
@login_required
def add_post(request):
    context = {}
    if request.method == 'GET':
        context['form'] = PostForm()
        context['posts'] = Post.objects.all().order_by('-date')
        context['comments'] = Comment.objects.all().order_by('comment_date_time')
        # print(context['comments'])
        return render(request, 'socialnetwork/global_stream.html', context)
    new_post = Post()
    new_post.poster = request.user
    new_post.poster_name = new_post.poster.username
    new_post.poster_user_id = new_post.poster.id
    print("time_now: ", timezone.now())
    new_post.date = parse_datetime(timezone.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-4])
    # new_post.date = parse_datetime(timezone.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-4])
    print("NEW_POST_DATE:", new_post.date)
    new_form = PostForm(request.POST, instance=new_post)
    if not new_form.is_valid():
        context = {'form': new_form}
    else:
        new_form.save()
        context['form'] = PostForm()

    context['posts'] = Post.objects.all().order_by('-date')
    context['comments'] = Comment.objects.all().order_by('comment_date_time')
    return render(request, 'socialnetwork/global_stream.html', context)


@ensure_csrf_cookie
@login_required
def add_comment(request, post_id):
    if request.method != 'POST':
        raise Http404

    if not 'comment_text' in request.POST or not request.POST['comment_text']:
        message = 'You must enter an comment to add.'
        json_error = '{ "error": "' + message + '" }'
        return HttpResponse(json_error, content_type='application/json')

    # print("Comment: ", request.POST.get('comment_text'))
    # print("post_id: ", request.POST.get('post_ref'))
    new_comment = Comment()
    new_comment.comment_text = request.POST.get('comment_text')
    new_comment.post_ref = request.POST.get('post_ref')
    new_comment.post = Post.objects.get(id=post_id)
    new_comment.comment_profile = Profile.objects.get(user=request.user)
    new_comment.user_name = new_comment.comment_profile.user.username
    new_comment.user_id = new_comment.comment_profile.user.id
    new_comment.comment_date_time = parse_datetime(timezone.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-4])
    # new_comment.comment_date_time = parse_datetime(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-4])
    print("NEW_COMMENT_DATE:", new_comment.comment_date_time)
    new_comment.comment_user = request.user
    new_comment.save()

    response_text = serializers.serialize('json', Comment.objects.filter(id=new_comment.id))
    return HttpResponse(response_text, content_type='application/json')


@login_required
def return_following(request):
    context = {}
    return_posts = []
    temp_posts = Post.objects.all().order_by('-date')
    return_comments = Comment.objects.all().order_by('comment_date_time')
    curr_user = Profile.objects.filter(user_id=request.user.id).last()
    for post in temp_posts:
        if post.poster in curr_user.following.all():
            return_posts.append(post)
    context['posts'] = return_posts
    context['comments'] = return_comments
    return render(request, 'socialnetwork/follower_stream.html', context)


@login_required
def return_cat(request):
    return render(request, 'socialnetwork/cat.html', {})


@login_required
def return_dog(request):
    return render(request, 'socialnetwork/dog.html', {})


@login_required
def update_profile(request, id):
    user_profile = Profile.objects.filter(user_id=request.user.id).last()
    context = {}
    context['profile'] = user_profile
    if id != request.user.id:
        try:
            other = Post.objects.filter(poster_id=id).last().poster
        except:  # This should be a link from comment.
            other = Comment.objects.filter(user_id=id).last().comment_profile.user

        other_profile = Profile.objects.filter(user_id=other.id).last()
        context['others'] = other_profile
        context['current_user'] = user_profile
        return render(request, 'socialnetwork/otherProfile.html', context)

    if request.method == 'GET':
        form = ProfileForm(request.POST, request.FILES)
        context['form'] = form
        return render(request, 'socialnetwork/myProfile.html', context)

    # Must copy content_type into a new model field because the model
    # FileField will not store this in the database.  (The uploaded file
    # is actually a different object than what's return from a DB read.)
    form = ProfileForm(request.POST, request.FILES, instance=user_profile)
    if not form.is_valid():
        context['form'] = form
        return render(request, 'socialnetwork/myProfile.html', context)
    pic = form.cleaned_data['profile_picture']
    # print('Uploaded picture: {} (type={})'.format(pic, type(pic)))
    form.save()
    if user_profile.content_type is None:
        user_profile.content_type = pic.content_type
    user_profile.profile_picture = pic
    user_profile.userBio = request.POST['bio_text']
    # print(user_profile)
    user_profile.save()
    print('Profile #{0} saved.'.format(user_profile.id))
    # context['message'] = 'Item #{0} saved.'.format(new_profile.id)
    context['form'] = ProfileForm()

    return render(request, 'socialnetwork/myProfile.html', context)


@login_required()
def follow_update(request, id):
    context = {}
    curr_user = Profile.objects.filter(user_id=request.user.id).last()
    user_to_follow = Profile.objects.filter(user_id=id).last()
    context['others'] = user_to_follow
    if user_to_follow.user not in curr_user.following.all():
        print("Before follow: {}".format(curr_user.following.all()))
        curr_user.following.add(user_to_follow.user)
        curr_user.save()
        print("After follow: {}".format(curr_user.following.all()))
        context['current_user'] = curr_user
        return render(request, 'socialnetwork/otherProfile.html', context)
    # print("Before unfollow: {}".format(curr_user.following.all()))
    curr_user.following.remove(user_to_follow.user)
    curr_user.save()
    context['current_user'] = curr_user
    return render(request, 'socialnetwork/otherProfile.html', context)


def login_action(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = LoginForm()
        return render(request, 'socialnetwork/login.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    form = LoginForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'socialnetwork/login.html', context)

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

    login(request, new_user)
    return redirect(reverse('home'))


def logout_action(request):
    logout(request)
    return redirect(reverse('login'))


def register_action(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request, 'socialnetwork/register.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    form = RegistrationForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'socialnetwork/register.html', context)

    # At this point, the form data is valid.  Register and login the user.
    new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                        password=form.cleaned_data['password1'],
                                        email=form.cleaned_data['email'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'])
    new_user.save()

    new_Profile = Profile(user=new_user)
    print(new_Profile)
    new_Profile.save()

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password1'])

    login(request, new_user)
    return redirect(reverse('home'))


@login_required
def get_photo(request, id):
    # print(id)

    profile = get_object_or_404(Profile, user_id=id)
    print(
        'Picture #{} fetched from db: {} (type={})'.format(id, profile.profile_picture, type(profile.profile_picture)))

    # Maybe we don't need this check as form validation requires a picture be uploaded.
    # But someone could have delete the picture leaving the DB with a bad references.
    if not profile.profile_picture:
        raise Http404

    return HttpResponse(profile.profile_picture, content_type=profile.content_type)


def refresh_global(request):
    if 'last_refresh' not in request.GET or not request.GET['last_refresh']:
        message = 'No last_refresh time.'
        json_error = '{ "error": "' + message + '" }'
        return HttpResponse(json_error, content_type='application/json')
    last_time = parse_datetime(request.GET['last_refresh'])
    print("Last time:", last_time)
    try:
        posts = Post.objects.filter(date__gt=last_time).order_by("-date")
        comments = Comment.objects.filter(comment_date_time__gt=last_time).order_by("comment_date_time")
        # print("global posts:", posts.values())
        # print("comments:", comments.values())
        json_response = {'posts': list(posts.values()), 'comments': list(comments.values())}
    except:
        json_response = {'posts': list(), 'comments': list()}

    return JsonResponse(json_response)


def refresh_following(request):
    if 'last_refresh' not in request.GET or not request.GET['last_refresh']:
        message = 'No last_refresh time.'
        json_error = '{ "error": "' + message + '" }'
        return HttpResponse(json_error, content_type='application/json')
    last_time = parse_datetime(request.GET['last_refresh'])
    print("Last time:", last_time)

    try:
        curr_user = Profile.objects.filter(user_id=request.user.id).last()
        following = curr_user.following.all()
        posts = Post.objects.filter(poster__in=following, date__gt=last_time).order_by("-date")
        posts_all = Post.objects.filter(poster__in=following).all()
        comments = Comment.objects.filter(post__in=posts_all, comment_date_time__gt=last_time).order_by("comment_date_time")
        # print("follow posts:", posts.values())
        print("comments:", comments.values())
        json_response = {'posts': list(posts.values()), 'comments': list(comments.values())}
    except:
        json_response = {'posts': list(), 'comments': list()}
    return JsonResponse(json_response)
