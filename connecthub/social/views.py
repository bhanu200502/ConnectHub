from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from .models import Profile, Post, Comment, Like, Follower

# ==================== HOME / FEED ====================
@login_required
def home(request):
    # Get users that current user follows
    following_users = Follower.objects.filter(
        follower=request.user
    ).values_list('following', flat=True)

    # Get posts from followed users and own posts
    posts = Post.objects.filter(
        user__in=list(following_users)
    ) | Post.objects.filter(user=request.user)

    posts = posts.order_by('-created_at')

    # Get liked posts by current user
    liked_posts = Like.objects.filter(
        user=request.user
    ).values_list('post_id', flat=True)

    # Suggested users to follow
    suggested_users = User.objects.exclude(
        id=request.user.id
    ).exclude(
        id__in=following_users
    )[:5]

    return render(request, 'social/home.html', {
        'posts': posts,
        'liked_posts': liked_posts,
        'suggested_users': suggested_users,
    })

# ==================== REGISTER ====================
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, 'Passwords do not match!')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists!')
            return redirect('register')

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # Create profile automatically
        Profile.objects.create(user=user)

        messages.success(request, 'Account created! Please login.')
        return redirect('login')

    return render(request, 'social/register.html')

# ==================== LOGIN ====================
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password!')
            return redirect('login')

    return render(request, 'social/login.html')

# ==================== LOGOUT ====================
def user_logout(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('login')

# ==================== PROFILE ====================
@login_required
def profile(request, username):
    user_obj = get_object_or_404(User, username=username)
    profile_obj, created = Profile.objects.get_or_create(user=user_obj)
    posts = Post.objects.filter(user=user_obj)

    # Check if current user follows this profile
    is_following = Follower.objects.filter(
        follower=request.user,
        following=user_obj
    ).exists()

    followers_count = profile_obj.get_followers_count()
    following_count = profile_obj.get_following_count()
    posts_count = profile_obj.get_posts_count()

    return render(request, 'social/profile.html', {
        'profile_user': user_obj,
        'profile': profile_obj,
        'posts': posts,
        'is_following': is_following,
        'followers_count': followers_count,
        'following_count': following_count,
        'posts_count': posts_count,
    })

# ==================== EDIT PROFILE ====================
@login_required
def edit_profile(request):
    profile_obj, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        bio = request.POST.get('bio', '')
        profile_picture = request.FILES.get('profile_picture')

        profile_obj.bio = bio
        if profile_picture:
            profile_obj.profile_picture = profile_picture
        profile_obj.save()

        messages.success(request, 'Profile updated successfully!')
        return redirect('profile', username=request.user.username)

    return render(request, 'social/edit_profile.html', {
        'profile': profile_obj
    })

# ==================== CREATE POST ====================
@login_required
def create_post(request):
    if request.method == 'POST':
        caption = request.POST.get('caption', '')
        image = request.FILES.get('image')

        if not caption and not image:
            messages.error(request, 'Please add a caption or image!')
            return redirect('create_post')

        Post.objects.create(
            user=request.user,
            caption=caption,
            image=image
        )

        messages.success(request, 'Post created successfully!')
        return redirect('home')

    return render(request, 'social/create_post.html')

# ==================== DELETE POST ====================
@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk, user=request.user)
    post.delete()
    messages.success(request, 'Post deleted successfully!')
    return redirect('home')

# ==================== POST DETAIL ====================
@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=post)
    liked = Like.objects.filter(
        user=request.user,
        post=post
    ).exists()

    return render(request, 'social/post_detail.html', {
        'post': post,
        'comments': comments,
        'liked': liked,
    })

# ==================== ADD COMMENT ====================
@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        comment_text = request.POST.get('comment_text', '')
        if comment_text:
            Comment.objects.create(
                user=request.user,
                post=post,
                comment_text=comment_text
            )
            messages.success(request, 'Comment added!')
        else:
            messages.error(request, 'Comment cannot be empty!')

    return redirect('post_detail', pk=pk)

# ==================== DELETE COMMENT ====================
@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk, user=request.user)
    post_pk = comment.post.pk
    comment.delete()
    messages.success(request, 'Comment deleted!')
    return redirect('post_detail', pk=post_pk)

# ==================== LIKE POST ====================
@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    like, created = Like.objects.get_or_create(
        user=request.user,
        post=post
    )

    if not created:
        like.delete()
        liked = False
    else:
        liked = True

    # Return JSON for AJAX
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'liked': liked,
            'likes_count': post.get_likes_count()
        })

    return redirect(request.META.get('HTTP_REFERER', 'home'))

# ==================== FOLLOW USER ====================
@login_required
def follow_user(request, username):
    user_to_follow = get_object_or_404(User, username=username)

    if user_to_follow == request.user:
        messages.error(request, 'You cannot follow yourself!')
        return redirect('profile', username=username)

    follow, created = Follower.objects.get_or_create(
        follower=request.user,
        following=user_to_follow
    )

    if not created:
        follow.delete()
        messages.success(request, f'Unfollowed {username}!')
    else:
        messages.success(request, f'Following {username}!')

    return redirect('profile', username=username)

# ==================== SEARCH USERS ====================
@login_required
def search_users(request):
    query = request.GET.get('q', '')
    users = []

    if query:
        users = User.objects.filter(
            username__icontains=query
        ).exclude(id=request.user.id)

    return render(request, 'social/search.html', {
        'users': users,
        'query': query
    })

# ==================== DASHBOARD ====================
@login_required
def dashboard(request):
    profile_obj, created = Profile.objects.get_or_create(
        user=request.user
    )
    posts = Post.objects.filter(user=request.user)
    followers_count = profile_obj.get_followers_count()
    following_count = profile_obj.get_following_count()

    return render(request, 'social/dashboard.html', {
        'profile': profile_obj,
        'posts': posts,
        'followers_count': followers_count,
        'following_count': following_count,
    })