from .models import Ad
from re import search
from django.utils import timezone

class VisitAdvertisementMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    @staticmethod
    def get_client_ip(request):
        return _.split(',')[0] if (_ := request.META.get('HTTP_X_FORWARDED_FOR')) else request.META.get('REMOTE_ADDR')

    def __call__(self, request):
        response = self.get_response(request)
        path = request.path
        pattern = r'^/api/advertisement/\d+/$'
        if search(pattern, path) and (pk := response.data.get('id')):
            advertisement = Ad.objects.get(pk=pk)
            username = request.user.username
            ip = self.get_client_ip(request)
            if (request.user.is_authenticated and (username not in advertisement.viewed_users)) or \
                (request.user.is_anonymous and (ip not in advertisement.viewed_users)):
                if username:
                    advertisement.viewed_users.append(username)
                elif ip:
                    advertisement.viewed_users.append(ip)
                time = timezone.now()
                advertisement.max_count_view += 1
                advertisement.views.setdefault(f'{time.month}/{time.day}', 0)
                advertisement.views[f'{time.month}/{time.day}'] += 1
                advertisement.save()
        return response
