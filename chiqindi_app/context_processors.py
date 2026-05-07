from .models import Notification


def notifications_count(request):
    count = 0
    if request.user.is_authenticated:
        count = Notification.objects.filter(recipient=request.user, is_read=False).count()
    return {'unread_notifications_count': count}
