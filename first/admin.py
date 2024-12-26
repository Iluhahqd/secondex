from django.contrib import admin
from .models import CustomUser, Product, ProductInTheCart, ProductInFavorites, PurchasedProduct

# Register your models here.

admin.site.register(Product)
admin.site.register(CustomUser)
admin.site.register(ProductInTheCart)
admin.site.register(ProductInFavorites)
admin.site.register(PurchasedProduct)
