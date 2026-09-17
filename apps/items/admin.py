from django.contrib import admin

from .models import Category, Item


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "owner", "status", "created_at")
    list_filter = ("status", "category", "created_at")
    search_fields = ("title", "description", "location_name", "owner__username")
    readonly_fields = ("created_at",)
    date_hierarchy = "created_at"