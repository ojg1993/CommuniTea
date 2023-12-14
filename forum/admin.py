from django.contrib import admin
from . import models

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

@admin.register(models.Post)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title',)}

