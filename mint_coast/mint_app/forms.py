from django.forms import ModelForm
from django import forms
from .models import MModel, Ticket, Album
from django.contrib.auth.models import User
from snowpenguin.django.recaptcha3.fields import ReCaptchaField
from allauth.account.forms import SignupForm


class MModelForm(ModelForm):
    captcha = ReCaptchaField()

    class Meta:
        model = MModel
        fields = ['name',
                  'mesh',
                  'format',
                  'price',
                  'for_sale',
                  'category',
                  'tags',
                  'mview',
                  'polygons',
                  'tris',
                  'animate',
                  'textures',
                  'is_pbr',
                  'is_unwrapped',
                  'is_low_poly',
                  'is_scan',
                  'is_print',
                  'video',
                  'style',
                  'created_with',
                  'rendered_with',
                  'photo00',
                  'photo01',
                  'photo02',
                  'photo03',
                  'photo04',
                  'photo05',
                  'description']


class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = ['theme',
                  'body']


class UserRegForm(ModelForm):
    captcha = ReCaptchaField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'username']


class UserForm(ModelForm):
    captcha = ReCaptchaField()

    class Meta:
        model = User
        fields = ['email', 'password']


class AlbumForm(forms.ModelForm):
    captcha = ReCaptchaField()

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['model'].queryset = MModel.objects.filter(user=user)

    class Meta:
        model = Album
        fields = ['name', 'model', "captcha"]
        widgets = {                                                                       # виджет CheckboxSelectMultiple позволяет выбирать несколько значений из представленного списка
            'model': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),   # и задаёт css класс form-check-input из Bootstrap
        }


class MySignUpForm(SignupForm):
    captcha = ReCaptchaField()
