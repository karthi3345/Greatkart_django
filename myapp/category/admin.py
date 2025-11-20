from django.contrib import admin
from django.utils.html import format_html
from .models import Category

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'slug', 'description', 'category_image_tag')
    prepopulated_fields = {'slug': ('category_name',)}

    def category_image_tag(self, obj):
        if obj.category_img:
            return format_html('<img src="{}" style="width: 100px; height:100px;" />', obj.category_img.url)
        return "-"
    
    category_image_tag.short_description = 'Category Image'

admin.site.register(Category, CategoryAdmin)
