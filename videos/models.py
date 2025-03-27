from django.db import models
from django.conf import settings


class Video(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # noqa: E501
    date = models.DateTimeField(auto_now_add=True)
    post = models.TextField(max_length=255)
    video_file = models.FileField(upload_to='videos/', blank=True, null=True)
    parent = models.ForeignKey('Video', null=True, blank=True, on_delete=models.CASCADE)  # noqa: E501
    comments = models.IntegerField(default=0)

    def __str__(self):
        return self.post

    def get_comments(self):
        return Video.objects.filter(parent=self).order_by('-date')

    def calculate_comments(self):
        self.comments = Video.objects.filter(parent=self).count()
        self.save()
        return self.comments

    def comment(self, user, post):
        video_comment = Video(user=user, post=post, parent=self)
        video_comment.save()
        self.comments = Video.objects.filter(parent=self).count()
        self.save()
        return video_comment
    
    def total_likes(self):
        return self.likes.all().count()

class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, related_name="likes", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'video')
    
    def __str__(self):
        return f"{self.user} likes {self.video}"
    


class Subscription(models.Model):
    subscriber = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="subscriptions")
    subscribed_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="subscribers")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('subscriber', 'subscribed_to')

    def __str__(self):
        return f"{self.subscriber} → {self.subscribed_to}"


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user} - {self.message}"