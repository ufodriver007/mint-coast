from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Category, MModel, Album, Ticket, Ban, Tag, News
from datetime import datetime
from django.utils.safestring import mark_safe

admin.site.register(Category)
admin.site.register(Album)
admin.site.register(Tag)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("is_open", "theme", "user", "reg")
    search_fields = ["theme"]
    list_filter = ("is_open", "reg")


@admin.register(MModel)
class MModelAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "category", "price", "is_hidden")
    search_fields = ["name"]
    list_filter = ("category", "price")


@admin.register(News)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("title", "short_description", "description", "posted_by", "date")
    search_fields = ["title", "description"]
    list_filter = ("posted_by", "date")

