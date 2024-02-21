"""Controller"""
import logging
import zipfile
import re
from urllib.parse import urlencode
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .forms import MModelForm, TicketForm, UserRegForm, UserForm, AlbumForm
from .models import Category, MModel, Ticket, Ban, Tag, Album, News
from cart.models import Order, Cart
from django.db.models.functions import Lower
from django.contrib import messages
from django.conf import settings
import os
from django.utils import timezone
from rest_framework.viewsets import ModelViewSet
from .serializers import CategorySerializer, BanSerializer, UserSerializer, MModelSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from datetime import datetime, timedelta
from pytz import timezone
from django.http import HttpResponseForbidden, HttpResponse
from django.forms.models import model_to_dict
from .services import ban_user, unban_user, validate_user
from allauth.socialaccount.models import SocialAccount
from django.core.paginator import Paginator
import decimal


logger = logging.getLogger("my_views")


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name']
    search_fields = ['name', 'id']
    ordering_fields = ['name', 'path']
    permission_classes = [IsAuthenticatedOrReadOnly]


class BanViewSet(ModelViewSet):
    queryset = Ban.objects.all()
    serializer_class = BanSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user']
    permission_classes = [IsAdminUser]


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['username']
    permission_classes = [IsAdminUser]


class MModelViewSet(ModelViewSet):
    queryset = MModel.objects.all()
    serializer_class = MModelSerializer


class IndexView(View):
    def get(self, request, *args, **kwargs):
        news = News.objects.order_by('-date')[:3]
        models = MModel.objects.order_by('-loading_date')[:9]

        return render(request, 'index.html', {'models': models, 'news': news})


class TestView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'test.html')


class MyLoginView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            form = UserForm()
            return render(request, 'login.html', {'form': form})

    def post(self, request, *args, **kwargs):
        email = request.POST.get("email")
        password = request.POST.get("password")
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            if check_password(password, user.password):
                user = authenticate(request, username=user.email, password=password)
                login(request, user)
                return redirect('home')

        return render(request, 'login.html', {'message': 'Неверный Email или пароль'})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')


class UserProfileView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            albums = Album.objects.filter(user_id=request.user.id)
            models = MModel.objects.filter(user_id=request.user.id)
            tickets = Ticket.objects.filter(user_id=request.user.id).exclude(is_open=True)

            email_confimed = request.user.emailaddress_set.filter(primary=True, verified=True).exists()
            is_social_acc = SocialAccount.objects.filter(user=request.user).exists()

            albums_and_previews = {}
            if albums:
                for al in albums:
                    album_models = MModel.objects.filter(album=al)
                    if album_models:
                        albums_and_previews[al] = album_models[0].photo00

            return render(request, 'user_profile.html', {'albums_and_previews': albums_and_previews, 'models': models, 'tickets': tickets, 'email_confirmed': email_confimed, 'is_social_acc': is_social_acc})
        else:
            return redirect('home')


class UserProfileEditView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return render(request, 'edit_profile.html')
        else:
            return redirect('home')

    def post(self, request, *args, **kwargs):
        first_name = request.POST.get("first_name")     # Получаем данные формы из запроса
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        if validate_user(first_name, last_name, username):
            user = request.user
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.save()

            return render(request, 'edit_profile.html', {'success': 'success'})

        return render(request, 'edit_profile.html', {'success': 'false'})


class SearchView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('query')
        if not query:
            query = ''

        category = request.GET.get('category')
        if category == 'all' or category == '':
            category = ''
            category_name = Category.objects.get(path='all').name
        else:
            category_name = Category.objects.get(path=category).name

        page = request.GET.get('page', 1)
        try:
            page = int(page)
        except ValueError:
            page = 1

        tags = request.GET.get('tags')

        if category and query != '':
            models = MModel.objects.annotate(lower_name=Lower('name')).filter(lower_name__icontains=query, category__path=category).order_by('loading_date')
        elif category:
            models = MModel.objects.filter(category__path=category).order_by('loading_date')
        else:
            models = MModel.objects.annotate(lower_name=Lower('name')).filter(lower_name__icontains=query).order_by('loading_date')

        # pagination
        p = Paginator(models, 20)
        models = p.get_page(page)               # все объекты страницы
        pages = p.page_range                    # range из страниц
        last_page = p.num_pages                 # количество страниц

        query_string = re.sub(r'&page=[^&]*', r'', urlencode(request.GET))

        return render(request, 'search.html', {'query': query, 'category': category, 'category_name': category_name, 'tags': tags, 'models': models, 'page': page, 'pages': pages, 'last_page': last_page, 'query_string': query_string})


class ModelView(View):
    def get(self, request, model_id):
        model = MModel.objects.get(id=model_id)
        tags = Tag.objects.filter(mmodel=model)
        photos = []
        if model.photo01:
            photos.append(model.photo01)
        if model.photo02:
            photos.append(model.photo02)
        if model.photo03:
            photos.append(model.photo03)
        if model.photo04:
            photos.append(model.photo04)
        if model.photo05:
            photos.append(model.photo05)
        return render(request, 'model.html', {'model': model, 'tags': tags, 'photos': photos})


class ModelEditView(View):
    def get(self, request, model_id):
        if request.user.is_authenticated and MModel.objects.filter(id=model_id).exists():
            model = MModel.objects.get(id=model_id)
            if model.user == request.user or request.user.is_staff:
                initial_data = model_to_dict(model)
                form = MModelForm(initial=initial_data)
                return render(request, 'model_edit.html', {'form': form, 'model': model})
        return redirect('home')

    def post(self, request, *args, **kwargs):
        form = MModelForm(request.POST, request.FILES)  # Получаем данные формы из запроса
        if form.is_valid():
            # Получаем заполненную модель
            edited_model = form.save(commit=False)
            # Дополнительно обрабатываем модель
            model = MModel.objects.get(id=request.POST.get("model_id"))
            model.name = edited_model.name
            model.mesh = edited_model.mesh or model.mesh
            model.format = edited_model.format
            model.price = edited_model.price
            model.for_sale = edited_model.for_sale
            model.category = edited_model.category
            model.mview = edited_model.mview or model.mview
            model.polygons = edited_model.polygons
            model.tris = edited_model.tris
            model.animate = edited_model.animate
            model.textures = edited_model.textures or model.textures
            model.is_pbr = edited_model.is_pbr
            model.is_unwrapped = edited_model.is_unwrapped
            model.is_low_poly = edited_model.is_low_poly
            model.is_scan = edited_model.is_scan
            model.is_print = edited_model.is_print
            model.video = edited_model.video or model.video
            model.style = edited_model.style
            model.created_with = edited_model.created_with
            model.rendered_with = edited_model.rendered_with
            model.photo00 = edited_model.photo00 or model.photo00
            model.photo01 = edited_model.photo01 or model.photo01
            model.photo02 = edited_model.photo02 or model.photo02
            model.photo03 = edited_model.photo03 or model.photo03
            model.photo04 = edited_model.photo04 or model.photo04
            model.photo05 = edited_model.photo05 or model.photo05
            model.description = edited_model.description

            # Очистка связанных объектов ManyToMany
            model.tags.clear()
            # Получаем список выделенных опций
            for tag in request.POST.getlist('tags'):
                if tag:
                    # Добавляем новые связанные объекты ManyToMany
                    model.tags.add(Tag.objects.get(id=tag))

            model.save()
            return render(request, 'model_edit.html', {'success': 'success'})

        model = MModel.objects.get(id=request.POST.get("model_id"))
        errors = form.errors
        logger.debug(f'Failed to edit. Model: {model.name}. Owner: {model.user} Errors: {errors}')
        return render(request, 'model_edit.html', {'success': 'false', 'form': form})


class ModelDeleteView(View):
    def post(self, request, *args, **kwargs):
        model = MModel.objects.get(id=request.POST.get("model_id"), user=request.user)
        model.delete()

        return redirect('profile')


class AddNewModelView(View):
    def get(self, request, *args, **kwargs):
        if os.getenv('ALLOW_USERS_UPLOADS') != 'TRUE':
            messages.error(request, 'Загрузки запрещены администраторм')
            return redirect('profile')

        if request.user.is_authenticated:
            if not request.user.emailaddress_set.filter(primary=True, verified=True).exists():
                return render(request, 'adding_model.html', {'email_confirmed': 'False'})
            form = MModelForm()
            return render(request, 'adding_model.html', {'form': form})
        else:
            return redirect('home')

    def post(self, request, *args, **kwargs):
        if os.getenv('ALLOW_USERS_UPLOADS') != 'TRUE':
            messages.error(request, 'Загрузки запрещены администраторм')
            return redirect('profile')

        form = MModelForm(request.POST, request.FILES)  # Получаем данные формы из запроса
        user = request.user
        if form.is_valid() and user.emailaddress_set.filter(primary=True, verified=True).exists():
            # Получаем заполненную модель
            new_model = form.save(commit=False)
            # Дополнительно обрабатываем модель
            new_model.user = user
            new_model.save()

            # Очистка связанных объектов ManyToMany
            for tag in request.POST.getlist('tags'):
                if tag:
                    # Добавляем новые связанные объекты ManyToMany
                    new_model.tags.add(Tag.objects.get(id=tag))

            # Получаем количество МБ свободного пространства на диске
            cmd = "df -m / | awk 'NR==2 {print $4}'"
            output = int(os.popen(cmd).read())

            # Если меньше 10 гигабайт, пишем warning
            if output < 10000:
                logger.warning(f'Free disk space is running out! {output} MB left!')
            else:
                logger.info(f'Free space {output} MB')

            return render(request, 'adding_model.html', {'success': 'success'})

        return render(request, 'adding_model.html', {'success': 'false', 'form': form})


class CreateTicketView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            form = TicketForm()
            return render(request, 'create_ticket.html', {'form': form})
        return redirect('home')

    def post(self, request, *args, **kwargs):
        form = TicketForm(request.POST)  # Получаем данные формы из запроса
        if form.is_valid():
            # Получаем заполненную модель
            new_ticket = form.save(commit=False)
            # Дополнительно обрабатываем модель
            new_ticket.user = request.user
            new_ticket.save()
            return render(request, 'create_ticket.html', {'success': 'success'})

        return render(request, 'create_ticket.html', {'success': 'false', 'form': form})


class ClosedTicketsView(View):
    def get(self, request, *args, **kwargs):
        tickets = Ticket.objects.filter(user_id=request.user.id).exclude(is_open=True)
        return render(request, 'closed_tickets.html', {'tickets': tickets})


class BannedUserView(View):
    def get(self, request):
        return render(request, 'banned.html')


class BanUserView(View):
    def get(self, request, u_id):
        if request.user.is_staff:
            user = get_object_or_404(User, id=u_id)
            end_date = datetime.now(timezone('Europe/Moscow')) + timedelta(weeks=2)
            reason = 'Нарушение правил сообщества.'
            if user:
                ban_user(user, end_date, reason)
                return redirect('admin:auth_user_changelist')
        else:
            return HttpResponseForbidden("User dont has permissions")


class UnBanUserView(View):
    def get(self, request, u_id):
        if request.user.is_staff:
            user = get_object_or_404(User, id=u_id)
            unban_user(user)
            return redirect('admin:auth_user_changelist')
        else:
            return HttpResponseForbidden("User dont has permissions")


class AddNewAlbumView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            models = MModel.objects.filter(user=request.user)
            form = AlbumForm(user=request.user)

            return render(request, 'create_album.html', {'form': form, 'models': models})
        return redirect('home')

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.emailaddress_set.filter(primary=True, verified=True).exists():
            user = request.user

            form = AlbumForm(user, request.POST)
            if form.is_valid():
                album = form.save(commit=False)
                album.user = user
                album.save()  # СОХРАНЕНИЕ ЭКЗЕМПЛЯРА ФОРМЫ
                form.save_m2m()  # сохранение связей ManyToManyField

                return render(request, 'create_album.html', {'success': 'success'})

        return render(request, 'create_album.html', {'success': 'false'})


class AlbumView(View):
    def get(self, request, a_id):
        album = get_object_or_404(Album, id=a_id)
        models = MModel.objects.filter(album=album)
        return render(request, 'album.html', {'album': album, 'models': models})


class AlbumDelete(View):
    def post(self, request):
        if request.user.is_authenticated:
            album = Album.objects.get(id=request.POST.get("a_id"))
            if album.user == request.user:
                album.delete()
        return redirect('profile')


class AlbumEditView(View):
    def get(self, request, a_id):
        album = get_object_or_404(Album, id=a_id)
        user = request.user

        if request.user.is_authenticated and album.user == request.user:
            form = AlbumForm(user=user, instance=album)
            return render(request, 'album_edit.html', {'form': form, 'album': album})
        else:
            return redirect('home')

    def post(self, request, a_id, *args, **kwargs):
        album = get_object_or_404(Album, id=a_id)
        user = request.user

        form = AlbumForm(user, request.POST, instance=album)
        if form.is_valid():
            album = form.save(commit=False)
            album.user = user
            album.save()           # СОХРАНЕНИЕ ЭКЗЕМПЛЯРА ФОРМЫ
            form.save_m2m()        # сохранение связей ManyToManyField

            return render(request, 'album_edit.html', {'success': 'success', 'album': album})
        return render(request, 'album_edit.html', {'success': 'false', 'album': album})


class NewsListView(View):
    def get(self, request):
        news = News.objects.all()
        return render(request, 'news_list.html', {'news': news})


class NewsDetailView(View):
    def get(self, request, n_id):
        news = get_object_or_404(News, id=n_id)
        return render(request, 'news_detail.html', {'news': news})


class SaleView(View):
    def get(self, request, *args, **kwargs):
        if request.GET:
            ids = [k for k, v in request.GET.items()]

            order = Order.objects.create(user=request.user)
            price = decimal.Decimal("0.00")
            carts = []
            for i in ids:
                cart = Cart.objects.get(id=i)
                cart.order = order
                cart.save()
                price += cart.products_price()
                carts.append(cart)

            order.price = price
            order.save()
        else:
            return redirect('cart')

        if request.user.is_authenticated:
            return render(request, 'sale.html', {'order': order, 'carts': carts})
        else:
            messages.warning(request, 'Для покупки/скачивания нужно залогиниться')
            return redirect('login')


class ModelDownloadingView(View):
    @staticmethod
    def download_file(model):
        # Путь к файлу, который нужно скачать
        mesh_path = os.path.join(settings.MEDIA_ROOT, str(model.mesh))
        textures_path = ''
        if model.textures:
            textures_path = os.path.join(settings.MEDIA_ROOT, str(model.textures))

        z = zipfile.ZipFile(f'{model.name}.zip', 'w')     # Создание нового архива
        z.write(mesh_path, os.path.basename(mesh_path))             # относительные пути, т.е. добавляются сами файлы без каталогов
        if textures_path:
            z.write(textures_path, os.path.basename(textures_path))
        z.close()

        # Открываем файл для чтения в бинарном режиме
        with open(f'{model.name}.zip', 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/octet-stream')

            # Устанавливаем заголовок для указания имени файла
            response['Content-Disposition'] = f'attachment; filename="your_model.zip"'   # str(model.mesh).split("/")[-1]

            os.remove(f'{model.name}.zip')

            return response

    def post(self, request, model_id, *args, **kwargs):
        # здесь должна быть проверка куплена ли модель/владеет ли пользователь моделью
        model = MModel.objects.get(id=model_id)

        return ModelDownloadingView.download_file(model)


class OrdersView(View):
    def get(self, request, *args, **kwargs):
        orders = Order.objects.filter(user=request.user)
        return render(request, 'orders.html', context={'orders': orders})


class OrderDeleteView(View):
    def post(self, request, order_id, *args, **kwargs):
        order = Order.objects.get(id=order_id)
        order.delete()

        return redirect('orders')
