from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Category, MModel, Album, Ticket, Ban, Tag, News
from datetime import datetime
from django.utils.safestring import mark_safe


admin.site.register(Album)
admin.site.register(Tag)

admin.site.site_title = 'MINT-COAST.RU'


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("is_open", "theme", "user", "reg")
    search_fields = ["theme"]
    list_filter = ("is_open", "reg")


@admin.register(MModel)
class MModelAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "category", "price", "get_html_photo", "is_hidden")
    search_fields = ["name"]
    list_filter = ("category", "price")

    def get_html_photo(self, object):
        return mark_safe(f"<img src='{object.photo00.url}' width=70>")

    get_html_photo.short_description = 'Фото'


@admin.register(News)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("title", "short_description", "description", "posted_by", "date")
    search_fields = ["title", "description"]
    list_filter = ("posted_by", "date")


@admin.register(Category)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "path")
