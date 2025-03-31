from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import get_user_model
from accounts.models import CustomUser
from videos.models import Notification, Subscription, Video, Like
from videos.forms import VideoForm

User = get_user_model()


@login_required
def home(request):
    videos = Video.objects.filter(parent=None).order_by('?')
    paginator = Paginator(videos, 12)
    page = request.GET.get('page')
    all_videos = paginator.get_page(page)
    notifications = Notification.objects.filter(user=request.user, is_read=False).order_by("-created_at")
    return render(request, "videos/home.html", {'videos': all_videos,'notifications': notifications})  


@login_required
def add_video(request):
    data = {}
    form = VideoForm()
    if request.method == "POST":
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.user = request.user
            video.video_file = form.cleaned_data.get('video_file')
            video.post = form.cleaned_data.get('post')
            video.save()
            data['form_is_valid'] = True

            # Notify subscribers
            subscribers = Subscription.objects.filter(subscribed_to=request.user).values_list('subscriber', flat=True)
            for subscriber_id in subscribers:
                Notification.objects.create(
                    user_id=subscriber_id,
                    message=f"{request.user.username} uploaded a new video: {video.post}"
                )

            return JsonResponse(data)
        else:
            data['form_is_valid'] = False
            data['video_form'] = render_to_string("videos/video_form.html", {'form': form}, request=request)  

    data['video_form'] = render_to_string("videos/video_form.html", {'form': form}, request=request)  
    return JsonResponse(data)


@login_required
def edit_video(request, id):
    data = {}
    video = get_object_or_404(Video, pk=id)
    form_instance = VideoForm(instance=video)
    if request.method == "POST":
        form = VideoForm(request.POST, request.FILES, instance=video)
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            return JsonResponse(data)
        else:
            data['form_is_valid'] = False
            data['edited_video'] = render_to_string("videos/edit_video.html", {'form': form}, request=request)  

    data['edit_video'] = render_to_string("videos/edit_video.html", {'form': form_instance}, request=request)  
    return JsonResponse(data)


@login_required
def video(request, id):
    video = get_object_or_404(Video, id=id)
    side_videos = Video.objects.filter(parent=None).order_by('?').exclude(id=id)[:4]  
    notifications = Notification.objects.filter(user=request.user, is_read=False).order_by("-created_at")

    return render(request, 'videos/video.html', {'video': video, 'side_videos': side_videos, 'notifications':notifications})  


@login_required
def comment(request):
    data = {}
    if request.method == 'POST':
        video_id = request.POST['video_id']
        video = Video.objects.get(pk=video_id)
        post = request.POST['post']
        post = post.strip()
        if len(post) > 0:
            user = request.user
            video.comment(user=user, post=post)
            data['partial_video_comments'] = render_to_string('videos/partial_video_comments.html', {'video': video}, request=request)  
            data['comment_count'] = video.calculate_comments()
            Notification.objects.create(
                user=video.user,
                message=f"{request.user.username} commented on your video: {post}"
            )
            return JsonResponse(data)
        else:
            return JsonResponse(data)


@login_required
def profile(request, username):
    page_user = get_object_or_404(User, username=username)
    all_videos = Video.objects.filter(parent=None).filter(user=page_user)
    notifications = Notification.objects.filter(user=request.user, is_read=False).order_by("-created_at")

    return render(request, 'videos/profile.html', {'page_user': page_user, 'all_videos': all_videos,'notifications':notifications})  


@login_required
def remove(request):
    data = {}
    comment_id = request.POST.get('comment_id')
    comment = Video.objects.get(pk=comment_id)
    if comment.user == request.user:
        parent = comment.parent
        comment.delete()
        data['comment_count'] = parent.calculate_comments()

    data['partial_video_comments'] = render_to_string('videos/partial_video_comments.html', {'video': parent}, request=request) 
    return JsonResponse(data)


@login_required
def delete_video(request, id):
    data = {}
    video = get_object_or_404(Video, pk=id)
    if video.user == request.user:
        video.delete()
        data['success'] = True
        data['message'] = 'Video deleted successfully.'
    else:
        data['success'] = False
        data['message'] = 'You are not authorized to delete this video.'
    data['data']=render_to_string('videos/delete_video_successful.html', request=request)
    return JsonResponse(data)
    

@login_required
def delete_video_confirmation(request, id):
    data={}
    data['data']=render_to_string('videos/delete_video.html', {'video_id': id}, request=request)
    return JsonResponse(data)


def search_results(request):
    query = request.GET.get('q', '')
    results = Video.objects.filter(post__icontains=query) if query else []
    notifications = Notification.objects.filter(user=request.user, is_read=False).order_by("-created_at")

    return render(request, 'videos/search_results.html', {'results': results, 'query': query, 'notifications': notifications}) 
    

@login_required
def like_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    like, created = Like.objects.get_or_create(user=request.user, video=video)

    if not created:
        like.delete() 
        liked = False
    else:
        liked = True
        Notification.objects.create(
            user=video.user,
            message=f"{request.user.username} liked your video: {video.post}"
        )
        
    total_likes = Like.objects.filter(video=video).count()
    
    
    return JsonResponse({"total_likes": total_likes, 'liked': liked})

@login_required
def liked_videos(request):
    liked_videos = Video.objects.filter(likes__user=request.user).distinct().order_by('-date')
    paginator = Paginator(liked_videos, 12)  
    page = request.GET.get('page')
    liked_videos_page = paginator.get_page(page)
    notifications = Notification.objects.filter(user=request.user, is_read=False).order_by("-created_at")

    
    return render(request, "videos/home.html", {'videos': liked_videos_page, 'notifications': notifications})  


@login_required
def subscribe_user(request, user_id):
    user_to_subscribe = get_object_or_404(User, id=user_id)
    subscription, created = Subscription.objects.get_or_create(subscriber=request.user, subscribed_to=user_to_subscribe)
    
    if not created:
        subscription.delete()  
        is_subscribed = False
    else:
        is_subscribed = True

    return JsonResponse({"is_subscribed": is_subscribed, "total_subscribers": user_to_subscribe.subscribers.count()})


@login_required
def subscription_videos(request):
    subscribed_users = CustomUser.objects.filter(subscribers__subscriber=request.user)
    
    videos_by_users = {user: Video.objects.filter(user=user).order_by('-date') for user in subscribed_users}

    notifications = Notification.objects.filter(user=request.user, is_read=False).order_by("-created_at")

    return render(request, "videos/Subscriptions.html", {
        'videos_by_users': videos_by_users, 
        'notifications': notifications})


@login_required
def notifications(request):
    notifications = Notification.objects.filter(user=request.user, is_read=False).order_by("-created_at")
    return render(request, "videos/notifications.html", {"notifications": notifications})

def mark_notifications_read(request):
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return redirect("notifications")

