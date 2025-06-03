from django.contrib import admin

from . import models

# Register your models here.

class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ['name','id','icon',]

class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['name','title','id','category','price','is_available','quantity','image','discount_percentages','description','created_at','updated_at','created_by']


class ReviewModelAdmin(admin.ModelAdmin):
    list_display = ['product','id','reviewer','comment','rating']



admin.site.register(models.Category,CategoryModelAdmin)
admin.site.register(models.Product,ProductModelAdmin)
admin.site.register(models.Review,ReviewModelAdmin)
admin.site.register(models.Order)
