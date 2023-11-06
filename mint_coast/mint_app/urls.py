"""
URL configuration for mint_coast project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from .views import IndexView, MyLoginView, LogoutView, UserProfileView, UserProfileEditView, SearchView, ModelView, ModelEditView, AddNewModelView, CreateTicketView, ClosedTicketsView, ModelDeleteView, BannedUserView, BanUserView, UnBanUserView, AddNewAlbumView, AlbumView, AlbumDelete, AlbumEditView, NewsListView, NewsDetailView
from rest_framework.routers import SimpleRouter
from .views import CategoryViewSet, BanViewSet, UserViewSet
from allauth.account.views import SignupView, ConfirmEmailView, LoginView
from .forms import MySignUpForm


router = SimpleRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'banned_users', BanViewSet)
router.register(r'user', UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('news/<int:n_id>/', NewsDetailView.as_view()),
    path('news/', NewsListView.as_view()),

    path('add_album/', AddNewAlbumView.as_view()),
    path('album/edit/<int:a_id>/', AlbumEditView.as_view()),
    path('album/<int:a_id>/', AlbumView.as_view()),
    path('album/delete/', AlbumDelete.as_view()),

    path('ban/<int:u_id>/', BanUserView.as_view(), name='ban_user'),
    path('unban/<int:u_id>/', UnBanUserView.as_view(), name='unban_user'),
    path('banned/', BannedUserView.as_view(), name='ban_page'),

    path('create_ticket/', CreateTicketView.as_view()),
    path('closed_tickets/', ClosedTicketsView.as_view()),

    path('add_model/', AddNewModelView.as_view()),
    path('search/', SearchView.as_view()),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('model/<int:model_id>', ModelView.as_view()),
    path('model/delete/', ModelDeleteView.as_view()),
    path('model/edit/<int:model_id>', ModelEditView.as_view()),
    path('user_profile/edit/', UserProfileEditView.as_view()),
    path('accounts/signup/', SignupView.as_view(template_name='registration.html', form_class=MySignUpForm), name='account_signup'),
    path('accounts/login/', MyLoginView.as_view(), name='login'),
    path('accounts/profile/', UserProfileView.as_view(), name='profile'),
    path('accounts/', include('allauth.urls')),
    path('', IndexView.as_view(), name='home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += router.urls
