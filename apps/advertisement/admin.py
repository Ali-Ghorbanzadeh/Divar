from django.contrib import admin
from .models import Category, Ad, Image, Video, ProvinceOrCity, CategoryFields

class CategoryFieldsAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            kwargs['queryset'] = Category.objects.filter(childes__isnull=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Category)
admin.site.register(Ad)
admin.site.register(Image)
admin.site.register(Video)
admin.site.register(ProvinceOrCity)
admin.site.register(CategoryFields, CategoryFieldsAdmin)
