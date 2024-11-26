from django.contrib import admin
from .models import Category, Ad, Image, Video, ProvinceOrCity, CategoryFields

admin.site.register(Category)
admin.site.register(Ad)
admin.site.register(Image)
admin.site.register(Video)
admin.site.register(ProvinceOrCity)
admin.site.register(CategoryFields)
