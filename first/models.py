from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime


class Profile(models.Model):
    user = models.OneToOneField("CustomUser", on_delete=models.CASCADE)


class CustomUser(AbstractUser):
    image = models.ImageField(upload_to='user_img/', default='user_img/user_default.png')
    phone_number = models.CharField(max_length=15)
    birth_date = models.DateField(null=True, blank=True)
    rating = models.FloatField(default=5.00, validators=[MaxValueValidator(8.00), MinValueValidator(2.00)])
    votes = models.IntegerField(default=0)


class ProductInTheCart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    # Когда пользователь доб. товар в корзину, создаётся такой объект, хранящий id пользователя и товара


class ProductInFavorites(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    # Когда пользователь доб. товар в избранное, создаётся такой объект, хранящий id пользователя и товара


class Product(models.Model):
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    type = models.CharField(max_length=200, default='snowboard')
    rost = models.CharField(max_length=200, default=' ')
    zhest = models.CharField(max_length=200, default=' ')
    progib = models.CharField(max_length=200, default=' ')
    brand = models.CharField(max_length=200, default=' ')
    image = models.ImageField(upload_to='product_img/', default="product_img/snowboard_default.png")
    available = models.BooleanField(default=True)
    creation_date = models.DateTimeField(default=datetime.date.today)
    is_purchased = models.BooleanField(default=False)

class PurchasedProduct(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)

    def __str__(self):
        return self.product.title


class snowboard(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, primary_key=True)
    rost = models.CharField(max_length=20)
    zhest = models.CharField(max_length=20)
    progib = models.CharField(max_length=20)
    brand = models.CharField(max_length=20)

    class Meta:
        db_table = 'snowboards'


class skis(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, primary_key=True)
    rost = models.CharField(max_length=20)
    brand = models.CharField(max_length=20)
    ridingstyle = models.CharField(max_length=20)
    leveloftraining = models.CharField(max_length=20)

    class Meta:
        db_table = 'skis'


class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    text = models.CharField(max_length=1000)


class Ratingtabls(models.Model):
    user1 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    user2 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True, related_name='user1')
    rating = models.IntegerField()

    def __str__(self):
        return self.title


class Report(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    reason = models.CharField(max_length=100)
    description = models.CharField(max_length=100)


class Coment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)


class Answer(models.Model):
    coment = models.ForeignKey(Coment, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
