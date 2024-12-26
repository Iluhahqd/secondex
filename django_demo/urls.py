from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from first import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.catalog, name='catalog'),
    path('registration/', views.registration, name='registration'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('about/', views.about, name='about'),
    path('support/', views.support, name='support'),
    path('product/<int:id>', views.show_product, name='show_product'),
    path('product/add', views.creating_product, name='creating_product'),
    path('profile/', views.profile, name='profile'),
    path('cart/', views.get_cart, name='cart'),
    path('report/<int:id>', views.report, name='report'),
    path('reportComplete', views.reportComplete, name='reportComplete'),
    path('AddAnswer/<int:id>', views.add_answer, name='AddAnswer'),
    path('AddComment/<int:id>', views.add_comment, name='AddComment'),
    path('BuyProduct/<int:id>', views.buy_product, name='BuyProduct'),
    path('BuyProducts/', views.buy_products, name='BuyProducts'),
    path('rating/', views.rating_of_sellers, name='rating_of_sellers'),
    path('product/<int:id>/rating/', views.rating, name='rating_of_'),
    path('favorites/', views.favorites_products, name='favorites_products'),
    path('profile/<int:id>/', views.other_profile, name='other_profile'),
    path('filter_products/', views.filter_products, name='filter_products'),
    path('tech_supp/', views.tech_supp, name='tech_supp'),
    path('add_to_fav_ajax/', views.add_to_favorite, name='add_to_fav_ajax'),
    path('add_to_cart_ajax/', views.add_to_cart, name='add_to_cart_ajax'),
    path('del_from_cart_ajax/', views.delete_from_cart, name='del_from_cart_ajax'),
    path('del_from_fav_ajax/', views.delete_from_fav, name='del_from_fav_ajax'),
    path('filter_products/add_to_fav_ajax/', views.add_to_favorite, name='add_to_fav_ajax'),
    path('profile/password_change/', views.password_change, name='password_change'),
    path('buy/<int:id>', views.buy_product, name='buy_product'),
    path('AddToCart/<int:id>', views.add_to_cart, name='AddToCart'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
