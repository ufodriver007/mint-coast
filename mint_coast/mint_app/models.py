from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
import shutil
from django.db.models.signals import pre_delete
from django.dispatch import receiver


class Tag(models.Model):
    name = models.CharField(max_length=100, verbose_name="Тэг")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название категории')
    path = models.TextField(default='/', verbose_name='Путь')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class MModel(models.Model):
    @staticmethod
    def get_time():
        return datetime.now().strftime('%m%d%y%H%M%S')

    FORMAT_CHOICES = (
        ('obj', 'obj'),          # 1 элемент - значение в базе, 2й - инфо для отображения в админке и т.д.
        ('fbx', 'fbx'),
        ('max', 'max'),
        ('mo', 'mo'),
        ('stl', 'stl'),
    )
    STYLE_CHOICES = (
        ('Stylized', 'Stylized'),
        ('Realistic', 'Realistic'),
        ('Anime', 'Anime'),
        ('Cartoon', 'Cartoon'),
    )
    name = models.CharField(max_length=200, verbose_name='Название')
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # один-ко-многим
    mesh = models.FileField(upload_to=f'./models/{get_time()}/', default=None, blank=True, verbose_name='Файл модели')
    format = models.CharField(max_length=300, choices=FORMAT_CHOICES, blank=False, default=None, verbose_name='Формат файла')  # множеств. выбор
    price = models.CharField(max_length=200, default='0', blank=True, verbose_name='Цена')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')  # один-ко-многим
    mview = models.FileField(upload_to=f'./models/{get_time()}/', default=None, blank=True)
    polygons = models.CharField(max_length=200, default=None, blank=True, verbose_name='Количество полигонов')
    tris = models.CharField(max_length=200, default=None, blank=True, verbose_name='Количество треугольников')
    animate = models.BooleanField(default=False, verbose_name='Анимация')
    textures = models.FileField(upload_to=f'./models/{get_time()}/textures/', default=None, blank=True, verbose_name='Архив с текстурами')
    is_pbr = models.BooleanField(default=False, verbose_name='PBR')
    is_unwrapped = models.BooleanField(default=False, verbose_name='Есть развёртка')
    is_low_poly = models.BooleanField(default=False, verbose_name='Лоу-поли модель')
    loading_date = models.DateTimeField(auto_now=True)
    is_scan = models.BooleanField(default=False, verbose_name='Скан')
    is_print = models.BooleanField(default=False, verbose_name='Для 3d печати')
    video = models.FileField(upload_to=f'./models/{get_time()}/', default=None, blank=True, verbose_name='Файл с видео')
    style = models.CharField(max_length=300, choices=STYLE_CHOICES, blank=False, default=None, verbose_name='Стиль')
    created_with = models.CharField(default=None, blank=True, verbose_name='Создано с помощью')
    rendered_with = models.CharField(default=None, blank=True, verbose_name='Программа для рендера')
    photo00 = models.FileField(upload_to=f'./models/{get_time()}/img/', default=None, blank=True, verbose_name='Фото 1')
    photo01 = models.FileField(upload_to=f'./models/{get_time()}/img/', default=None, blank=True, verbose_name='Фото 2')
    photo02 = models.FileField(upload_to=f'./models/{get_time()}/img/', default=None, blank=True, verbose_name='Фото 3')
    photo03 = models.FileField(upload_to=f'./models/{get_time()}/img/', default=None, blank=True, verbose_name='Фото 4')
    photo04 = models.FileField(upload_to=f'./models/{get_time()}/img/', default=None, blank=True, verbose_name='Фото 5')
    photo05 = models.FileField(upload_to=f'./models/{get_time()}/img/', default=None, blank=True, verbose_name='Фото 6')
    description = models.TextField(default=None, blank=True, verbose_name='Описание')
    is_hidden = models.BooleanField(default=False, blank=True, verbose_name='Скрытая модель')
    tags = models.ManyToManyField(Tag, verbose_name='Тэги')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Модель'
        verbose_name_plural = 'Модели'


class Album(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    model = models.ManyToManyField(MModel, verbose_name='Модели')  # многие-ко-многим
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # один-ко-многим

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Альбом'
        verbose_name_plural = 'Альбомы'


class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # один-ко-многим
    theme = models.CharField(max_length=200, verbose_name='Заголовок')
    body = models.TextField(verbose_name='Тикет')
    answer = models.TextField(default=None, null=True, blank=True)
    is_open = models.BooleanField(default=True)
    reg = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.theme}'

    class Meta:
        verbose_name = 'Тикет'
        verbose_name_plural = 'Тикеты'


class Ban(models.Model):
    user = models.OneToOneField(User, default=None, null=True, blank=True, on_delete=models.CASCADE)
    start_date = models.DateTimeField(verbose_name='Начало')
    end_date = models.DateTimeField(verbose_name='Окончание')
    reason = models.TextField(default=None, null=True, blank=True, verbose_name='Причина')


class News(models.Model):
    @staticmethod
    def get_time():
        return datetime.now().strftime('%m%d%y%H%M%S')

    title = models.CharField(max_length=250, verbose_name='Заголовок')
    short_description = models.TextField(verbose_name='Краткое описание')
    description = models.TextField(verbose_name='Описание')
    image = models.FileField(upload_to=f'./news/{get_time()}/', default=None, blank=True, verbose_name='Файл изображения')
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)


@receiver(pre_delete, sender=MModel)
def delete_model_files(sender, instance: MModel, **kwargs):
    """Удаление директории с файлами модели. Получаем сигнал от MModel перед удалением экземпляра."""
    path = f"./media/{'/'.join(str(instance.mesh).split('/')[:2])}"
    try:
        shutil.rmtree(path)
    except FileNotFoundError:
        pass
