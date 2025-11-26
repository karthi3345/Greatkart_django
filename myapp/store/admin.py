from django.contrib import admin
from .models import Product, Variation
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'slug', 'description', 'price','product_image_tag','stock', 'is_available', 'category','created_date','modified_date')
    prepopulated_fields = {"slug": ("product_name",)}


    def product_image_tag(self, obj):
        if obj.img:
            return format_html('<img src="{}" style="width: 100px; height:100px;" />', obj.img.url)
        return "-"
    
    product_image_tag.short_description = 'Product Image'
    
class VariationAdmin(admin.ModelAdmin):
    list_display = ['product','variation_category', 'variation_value', 'is_active', 'created_date']
    list_editable = ['is_active']
    list_filter = ['product','variation_category', 'variation_value']

admin.site.register(Variation, VariationAdmin)

