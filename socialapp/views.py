from .models import Post,Profile
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect,get_object_or_404
from django.urls import reverse
from django.contrib import messages
from .forms import ProfileForm
from .forms import UpdateProfilePictureForm
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import Profile,FriendRequest
from django.views.generic import ListView, RedirectView
from django.urls import reverse_lazy
from .models import FriendRequest



def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('view_profile') 
        else:
            return render(request, 'registration/login.html', {'error_message': 'Invalid username or password. Please try again.'})

    return render(request, 'registration/login.html')


def user_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password1')

        try:
           
            user = User.objects.create_user(username=username, password=password)

            profile = Profile.objects.create(user=user)

            messages.success(request, 'Registration successful. Welcome!')
        except Exception as e:
            messages.error(request, f'Error during registration: {str(e)}')

        return redirect('home')

    return render(request, 'registration/register.html')



def home(request):
    posts = Post.objects.all() 
    return render(request, 'home.html', {'posts': posts})




from django.http import Http404


def view_profile(request):
    user = request.user
    profile = Profile.objects.get(user=user)

    if request.method == 'POST':
        form = UpdateProfilePictureForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile picture updated successfully.')
            return redirect('view_profile')
        else:
            messages.error(request, 'Error updating profile picture. Please try again.')

    else:
        form = UpdateProfilePictureForm()

    return render(request, 'profile.html', {'profile': profile, 'form': form})


def change_profile_picture(request):
    user_profile = request.user.userprofile

    if request.method == 'POST':
        form = UpdateProfilePictureForm(request.POST, request.FILES)
        if form.is_valid():
            profile_picture = form.cleaned_data['profile_picture']
            user_profile.profile_picture = profile_picture
            user_profile.save()
            return redirect('edit_profile')  # Redirect to the edit profile page or any other desired page
    else:
        form = UpdateProfilePictureForm()

    return render(request, 'change_profile_picture.html', {'form': form})


def edit_profile(request):
    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('view_profile')
    else:
        form = ProfileForm(instance=profile)

    profile_picture_form = UpdateProfilePictureForm()

    return render(request, 'edit_profile.html', {'form': form, 'profile_picture_form': profile_picture_form})




@login_required
def profile(request):
    friend_requests_received = FriendRequest.objects.filter(to_user=request.user)
    friend_requests_sent = FriendRequest.objects.filter(from_user=request.user)

    context = {
        'friend_requests_received': friend_requests_received,
        'friend_requests_sent': friend_requests_sent,
    }
    return render(request, 'profile.html', context)

from django.http import JsonResponse

from .models import FriendRequest

@login_required
def friend_requests(request):
    friend_requests_received = FriendRequest.objects.filter(to_user=request.user)
    friend_requests_sent = FriendRequest.objects.filter(from_user=request.user)

    context = {
        'friend_requests_received': friend_requests_received,
        'friend_requests_sent': friend_requests_sent,
    }
    return render(request, 'friend_requests.html', context)

@login_required
def send_friend_request(request, to_user_id):
    try:
        # Get the user to whom the friend request is being sent
        to_user = get_object_or_404(User, id=to_user_id)

        # Check if a friend request already exists
        existing_request = FriendRequest.objects.filter(from_user=request.user, to_user=to_user)
        if existing_request.exists():
            raise Exception('Friend request already sent.')

        # Create a new friend request
        friend_request = FriendRequest(from_user=request.user, to_user=to_user)
        friend_request.save()

        # Return a JSON response on success
        return JsonResponse({'success': True})
    except Exception as e:
        # Return a JSON response on failure
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
def accept_friend_request(request, friend_request_id):
    friend_request = FriendRequest.objects.get(id=friend_request_id)
    friend_request.delete()  # You may want to keep a record in the database, instead of deleting
    return redirect('view_profile')  # Redirect to the user's profile or any other page

@login_required
def reject_friend_request(request, friend_request_id):
    try:
        # Get the friend request
        friend_request = get_object_or_404(FriendRequest, id=friend_request_id)

        # Check if the logged-in user is the recipient of the friend request
        if friend_request.to_user != request.user:
            raise Exception('You are not authorized to reject this friend request.')

        # Delete the friend request
        friend_request.delete()

        # Return a JSON response on success
        return JsonResponse({'success': True})
    except Exception as e:
        # Return a JSON response on failure
        return JsonResponse({'success': False, 'error': str(e)})

from django.db.models import Q

@login_required
def search_friends(request):
    search_query = request.GET.get('search', '')
    
    friend_requests_sent = FriendRequest.objects.filter(from_user=request.user)

    if search_query:
        
        search_results = User.objects.filter(
            Q(username__icontains=search_query) | Q(first_name__icontains=search_query) | Q(last_name__icontains=search_query)
        ).exclude(id=request.user.id)
    else:
        search_results = []

    context = {
        'friend_requests_sent': friend_requests_sent,
        'search_results': search_results,
    }
    return render(request, 'friend_requests.html', context)
    
    
'''from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Post , Profile
from .forms import ProfileForm 
from .forms import PostForm 
from django.contrib.auth.decorators import login_required

def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home') 
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

@login_required
def view_profile(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'profile.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect('home') 
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})





def post_detail(request, post_id):
    post = Post.objects.get(pk=post_id)
    return render(request, 'post_detail.html', {'post': post})

def like_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('post_detail', post_id=post_id)
'''