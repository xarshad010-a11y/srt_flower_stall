from django.contrib import admin
from django.utils.html import mark_safe
from .models import Flower, Garland


class FlowerInline(admin.TabularInline):
    model = Flower
    fields = ('name', 'price', 'available_stock', 'image_tag')
    readonly_fields = ('image_tag',)
    extra = 0

    def image_tag(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="width:80px; height:auto; border-radius:6px;"/>')
        return '-'
    image_tag.short_description = 'Image'


@admin.register(Garland)
class GarlandAdmin(admin.ModelAdmin):
    list_display = ('name', 'flower_count', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at',)
    inlines = (FlowerInline,)


@admin.register(Flower)
class FlowerAdmin(admin.ModelAdmin):
    list_display = ('name', 'garland', 'price', 'available_stock', 'image_tag', 'created_at')
    list_editable = ('price', 'available_stock')
    list_display_links = ('name',)
    search_fields = ('name', 'description', 'garland__name')
    list_filter = ('garland', 'created_at')
    list_per_page = 25
    ordering = ('name',)
    readonly_fields = ('image_tag',)
    save_on_top = True

    def image_tag(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="width:80px; height:auto; border-radius:6px;"/>')
        return '-'
    image_tag.short_description = 'Image'
