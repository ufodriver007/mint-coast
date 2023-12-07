from django.shortcuts import redirect, render
from .models import Ban
from django.http import HttpResponseForbidden
from datetime import datetime
from pytz import timezone
from django.contrib.auth import logout
from django.core.cache import cache
from django.conf import settings


class BanMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/logout/':
            logout(request)
        if request.user.is_authenticated:
            if Ban.objects.filter(user=request.user.id).exists():
                ban = Ban.objects.get(user=request.user)
                if ban.start_date <= datetime.now(timezone('Europe/Moscow')) <= ban.end_date:
                    return render(request, 'banned.html', status=403, context={'reason': ban.reason, 'end_date': ban.end_date})
        response = self.get_response(request)
        return response


class ThrottlingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Получаем IP-адрес пользователя или другую уникальную строку для идентификации
        # здесь используется IP-адрес, но это не самое надежное решение
        client_ip = request.META['REMOTE_ADDR']

        if client_ip in settings.BLACKLIST:
            return HttpResponseForbidden('Ваш IP заблокирован!')

        # Устанавливаем ключ для кэша, используя IP-адрес и префикс
        cache_key = f'throttle_{client_ip}'

        # Получаем текущее количество запросов из кэша
        request_count = cache.get(cache_key, 0)

        # Проверка на превышение лимита запросов
        if request_count >= 1000:  # Примерно 1000 запросов в час
            return HttpResponseForbidden('Превышен лимит запросов')

        # Увеличиваем счетчик запросов и сохраняем его в кэше
        cache.set(cache_key, request_count + 1, 3600)  # Сохраняем на час

        # Пропускаем запрос дальше по стеку middleware
        response = self.get_response(request)

        return response
