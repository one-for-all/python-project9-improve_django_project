from django.contrib import admin
from .models import Menu, Item, Ingredient


class IngredientAdmin(admin.ModelAdmin):
    list_per_page = 500


admin.site.register(Menu)
admin.site.register(Item)
admin.site.register(Ingredient, IngredientAdmin)
