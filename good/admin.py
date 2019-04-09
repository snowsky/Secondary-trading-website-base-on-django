from django.contrib import admin

# Register your models here.
from good.models import Good, GoodPictures, Category


@admin.register(Good)
class GoodAdmin(admin.ModelAdmin):
    fields = ('title', 'original_price', 'current_price', 'sell_method', 'good_status', 'content')
    list_display = ('title', 'owner_user','current_price', 'sell_method', 'good_status')


@admin.register(GoodPictures)
class GoodPicturesAdmin(admin.ModelAdmin):
    fields = ('image', 'is_main_pic', 'good')
    list_display = ('image', 'is_main_pic', 'good')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ('name', )
    list_display = ('name', )

