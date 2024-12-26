from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string

from django_demo import settings
from .forms import LoginUserForm, ReportForm, FindForm, AddCommentForm, AddAnswerForm
from .forms import LoginUserForm, FindForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import SignUpForm
from .models import CustomUser, Ratingtabls, Answer, Coment, snowboard, skis, PurchasedProduct
from django.shortcuts import render
from .models import Product, Answer, Coment
from .forms import EditProfileForm
import collections
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .forms import SignUpForm, EditProfileForm, LoginUserForm, AddProductForm, ReportForm, EditImageForm
from .models import Profile, CustomUser, Product, Report, ProductInFavorites
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Profile, CustomUser, Product, Report, ProductInFavorites, ProductInTheCart
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

User = get_user_model()


def registration(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password, email=form.cleaned_data.get('email'),
                                phone_number=form.cleaned_data.get('phone_number'),
                                image=form.cleaned_data.get('image'))
            login(request, user)
            return HttpResponseRedirect(reverse('catalog'))
    else:
        form = SignUpForm()
    return render(request, 'registration.html', context={'form': form})


def login(request):
    if request.method == 'POST':
        form = LoginUserForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user and user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('catalog'))
    else:
        form = LoginUserForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('catalog'))


def catalog(request):
    context = {'title': 'Главная страница',}
    context['auth'] = request.user.is_authenticated
    if request.user.is_authenticated:
        cur_user = CustomUser.objects.get(id=request.user.id)
        context['user_id'] = request.user.id
    else:
        context['user_id'] = -2
    if request.method == 'POST':
        form = FindForm(request.POST)
        context['form'] = form
        if form.is_valid():
            name = form.cleaned_data['name']
            prods = Product.objects.filter(title__contains=name, is_purchased=False)
            if request.user.is_authenticated:
                context['products'] = [(prod, ProductInFavorites.objects.filter(product=prod, user=cur_user).exists(),
                                        prod.seller.username != request.user.username) for prod in prods]
            else:
                context['products'] = [(prod, False, True) for prod in prods]
            return render(request, 'catalog.html', context)
        else:
            context['products'] = Product.objects.filter(is_purchased=False)
    else:
        form = FindForm()
        context['form'] = form
        prods = Product.objects.filter(is_purchased=False).order_by('-creation_date')
        if request.user.is_authenticated:
            context['products'] = [(prod, ProductInFavorites.objects.filter(product=prod, user=cur_user).exists(),
                                    prod.seller.username != request.user.username) for
                                   prod in prods]
        else:
            context['products'] = [(prod, False, True) for prod in prods]
        return render(request, 'catalog.html', context)


def add_to_favorite(request):
    id = request.GET.get('id', -1)
    if id == -1:
        print("err")
        return
    user_id = request.GET.get('user_id', -1)
    if user_id == -2:
        return HttpResponse(request)
    user = CustomUser.objects.get(id=user_id)
    prod = Product.objects.get(id=id)
    if ProductInFavorites.objects.filter(product=prod, user=user).exists():
        ProductInFavorites.objects.filter(product=prod, user=user).delete()
    else:
        if prod.seller != user:
            rec = ProductInFavorites(product=prod, user=user)
            rec.save()
    return HttpResponse(request)


def add_to_cart(request):

    id = request.GET.get('id', -1)
    if id == -1:
        print("err")
        return
    user_id = request.GET.get('user_id', -1)
    if user_id == -2:
        return HttpResponse(request)
    user = CustomUser.objects.get(id=user_id)
    prod = Product.objects.get(id=id)
    if ProductInTheCart.objects.filter(product=prod, user=user).exists():
        pass
    else:
        if prod.seller != user:
            rec = ProductInTheCart(product=prod, user=user)
            rec.save()
    return HttpResponse(request)


def delete_from_cart(request):
    id = request.GET.get('id', -1)
    if id == -1:
        print("err")
        return
    user_id = request.GET.get('user_id', -1)
    if user_id == -2:
        return HttpResponse(request)
    user = CustomUser.objects.get(id=user_id)
    prod = Product.objects.get(id=id)
    if ProductInTheCart.objects.filter(product=prod, user=user).exists():
        ProductInTheCart.objects.filter(product=prod, user=user).delete()
        print("product deleted")
    else:
        print("ERROR\nDELETING UNEXISTING PRODUCTINTHECART")
    return HttpResponseRedirect('/cart')


def delete_from_fav(request):
    id = request.GET.get('id', -1)
    if id == -1:
        print("err")
        return
    user_id = request.GET.get('user_id', -1)
    if user_id == -2:
        return HttpResponse(request)
    user = CustomUser.objects.get(id=user_id)
    prod = Product.objects.get(id=id)
    if ProductInFavorites.objects.filter(product=prod, user=user).exists():
        ProductInFavorites.objects.filter(product=prod, user=user).delete()
        print("product deleted from fav")
    else:
        print("ERROR\nDELETING UNEXISTING PRODUCTINTHEFAV")
    return HttpResponseRedirect('/favorites')


@login_required(login_url='login')
def filter_products(request):
    context = {}
    context['auth'] = request.user.is_authenticated

    products = Product.objects.all()

    # Получение данных из запроса
    product_type = request.GET.get('type', None)
    price_min = request.GET.get('price_min', None)
    price_max = request.GET.get('price_max', None)

    # Фильтрация по типу продукта
    if product_type:
        products = products.filter(type=product_type)

    # Фильтрация по диапазону цен
    if price_min:
        products = products.filter(price__gte=price_min)
    if price_max:
        products = products.filter(price__lte=price_max)

    # Фильтрация для сноубордов
    if product_type == 'snowboard':
        snowboard_params = {}
        for field in ['rost', 'zhest', 'progib', 'brand']:
            value = request.GET.get(f'snowboard{field}', None)
            if value:
                snowboard_params[field] = value

        # Фильтрация продуктов с использованием связанных записей snowboard
        if snowboard_params:
            snowboard_ids = snowboard.objects.filter(**snowboard_params).values_list('product', flat=True)
            products = products.filter(id__in=snowboard_ids)

    # Фильтрация для лыж
    elif product_type == 'skis':
        skis_params = {}
        for field in ['rost', 'brand', 'ridingstyle', 'leveloftraining']:
            value = request.GET.get(f'skis{field}', None)
            if value:
                skis_params[field] = value

        # Фильтрация продуктов с использованием связанных записей skis
        if skis_params:
            skis_ids = skis.objects.filter(**skis_params).values_list('product', flat=True)
            products = products.filter(id__in=skis_ids)

    products = products.filter(is_purchased=False)
    if request.user.is_authenticated:
        cur_user = CustomUser.objects.get(id=request.user.id)
        context['user_id'] = request.user.id
    else:
        context['user_id'] = -2
    if request.method == 'POST':
        form = FindForm(request.POST)
        context['form'] = form
        if form.is_valid():
            name = form.cleaned_data['name']
            products = products.filter(title__contains=name, is_purchased=False)
            if request.user.is_authenticated:
                cur_user = CustomUser.objects.get(id=request.user.id)
                context['products'] = [(prod, ProductInFavorites.objects.filter(product=prod, user=cur_user).exists(),
                                        prod.seller != cur_user)
                                       for prod in products]
            else:
                context['products'] = [(prod, False, True) for prod in products]
            return render(request, 'catalog.html', context)
        else:
            context['products'] = products.filter(is_purchased=False)
    else:
        form = FindForm()
        context['form'] = form
        products = products.filter(is_purchased=False).order_by('-creation_date')
        if request.user.is_authenticated:
            cur_user = CustomUser.objects.get(id=request.user.id)
            context['products'] = [
                (prod, ProductInFavorites.objects.filter(product=prod, user=cur_user).exists(), prod.seller != cur_user)
                for
                prod in products]
        else:
            context['products'] = [(prod, False, True) for prod in products]
        return render(request, 'catalog.html', context)


def rating_of_sellers(request):
    context = {}
    context['products'] = Product.objects.order_by('-creation_date')[:4]
    return render(request, 'rating_of_sellers.html', context)


def about(request):
    return render(request, 'home.html', context={})


def support(request):
    return render(request, 'support.html', context={})


@login_required(login_url='login')
def favorites_products(request):
    context = {}
    cur_user = CustomUser.objects.get(id=request.user.id)
    context['products'] = [elem.product for elem in ProductInFavorites.objects.filter(user=cur_user) if
                           elem.product.is_purchased == False]
    context['user_id'] = request.user.id
    # передаются объекты типа Product, чтобы легче было обращаться к полям
    return render(request, 'favorites.html', context=context)


@login_required(login_url='login')
def creating_product(request):
    context = {
        'title': 'Добавление товара',
        'loginform': LoginUserForm(),
        'user': request.user,
    }
    if request.method == 'POST':
        product_type = request.POST.get('productType', 'snowboard')
        if len(request.FILES) != 0:
            File = request.FILES['productPhoto']
            with open(f"{settings.MEDIA_ROOT}/product_img/{File.name}", "wb+") as destination:
                for chunk in File.chunks():
                    destination.write(chunk)
            img_url = 'product_img/' + File.name
        else:
            img_url = 'product_img/snowboard_default.jpg'
        record = Product(
            title=request.POST.get('productName', "UnnamedProduct"),
            description=request.POST.get('productDescription', ""),
            price=request.POST.get('productPrice', -1),
            type=product_type,
            seller=request.user,  # Уже имеем объект пользователя, нет нужды его заново получать
            available=request.POST.get('productAvailable', 'True') == 'True',  # Для BooleanField
            image=img_url
        )
        record.save()

        if product_type == 'snowboard':
            # Сохраняем дополнительные параметры сноуборда
            snowboard_record = snowboard(
                product=record,
                rost=request.POST.get('snowboardrost'),
                zhest=request.POST.get('snowboardzhest'),
                progib=request.POST.get('snowboardprogib'),
                brand=request.POST.get('snowboardbrand'),
            )
            snowboard_record.save()
        elif product_type == 'skis':
            # Сохраняем дополнительные параметры лыж
            skis_record = skis(
                product=record,
                rost=request.POST.get('skisrost'),
                brand=request.POST.get('skisbrand'),
                ridingstyle=request.POST.get('skisridingstyle'),
                leveloftraining=request.POST.get('skisleveloftraining'),
            )
            skis_record.save()

        return redirect('show_product', id=record.id)
    return render(request, 'creation_of_the_lot.html', context)


def show_product(request, id):
    context = {
        'title': 'title',
        'loginform': LoginUserForm(),
        'user': request.user,
    }
    try:
        record = Product.objects.get(id=id)
        context['seller'] = record.seller
        context['if_purchased'] = record.is_purchased
        context['is_seller'] = record.seller == request.user
        context['image'] = record.image
        context['record'] = record
        context['addform'] = AddProductForm(
            initial={
                'title': record.title,
                'description': record.description,
                'price': record.price,
                'available': record.available,
                'type': record.type
            }
        )
        if record.type == "snowboard":
            context['is_snowboard'] = True
            cur_snowboard = snowboard.objects.get(product_id=id)
            context['rost'] = cur_snowboard.rost
            context['zhest'] = cur_snowboard.zhest
            context['progib'] = cur_snowboard.progib
            context['brand'] = cur_snowboard.brand
        elif record.type == "skis":
            context['is_ski'] = True
            ski = skis.objects.get(product_id=id)
            context['rost'] = ski.rost
            context['brand'] = ski.brand
            context['ridingstyle'] = ski.ridingstyle
            context['leveloftraining'] = ski.leveloftraining
        context['id'] = id
        context['form'] = AddCommentForm(initial={'product': id})
        comments = {comment: {'answers': Answer.objects.filter(coment=comment),
                              'form': AddAnswerForm(initial={'comment': comment.id})} for comment in
                    Coment.objects.filter(product=id)}
        context['comments'] = comments
    except Product.DoesNotExist:
        return redirect('catalog')
    return render(request, 'show_product.html', context)


def add_answer(request, id):
    if request.method == 'POST':
        form = AddAnswerForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Answer.objects.create(coment=Coment.objects.get(id=data['comment']), user=request.user, text=data['text'])
    return HttpResponseRedirect(f'/product/{id}')


def add_comment(request, id):
    if request.method == 'POST':
        form = AddCommentForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Coment.objects.create(product=Product.objects.get(id=id), user=request.user, text=data['text'])
    return HttpResponseRedirect(f'/product/{id}')


def buy_product(request, id):
    if request.method == 'POST':
        product = Product.objects.get(id=id)
        if (product.is_purchased) == False:
            product.is_purchased = True
            product.save()
            user = request.user
            rec = PurchasedProduct(product=product, user=user)
            rec.save()
            Coment.objects.filter(product=product).delete()

    return HttpResponseRedirect(f'/product/{id}')


def buy_products(request):
    if request.method == 'POST':
        user = request.user
        cartProducts = ProductInTheCart.objects.filter(user=user)
        for i in cartProducts:
            product = i.product
            if (product.is_purchased) == False and i.product.seller != user:
                product.is_purchased = True
                product.save()
                user = request.user
                rec = PurchasedProduct(product=product, user=user)
                rec.save()
                Coment.objects.filter(product=product).delete()
            i.delete()
    return HttpResponseRedirect(f'/cart')


@login_required(login_url='login')
def profile(request):
    form = ''
    img_form = ''
    if 'change_data' in request.POST:
        form = EditProfileForm(request.POST, files=request.FILES, instance=request.user)
        if form.is_valid():
            changed_user = form.save(commit=False)
            changed_user.user = request.user
            changed_user.save()
            if changed_user and changed_user.is_active:
                login(request, changed_user)
                return HttpResponseRedirect(reverse('profile'))
    elif 'change_image' in request.POST:
        img_form = EditImageForm(request.POST, files=request.FILES, instance=request.user)
        if img_form.is_valid():
            changed_user = img_form.save(commit=False)
            changed_user.user = request.user
            changed_user.save()
            if changed_user and changed_user.is_active:
                login(request, changed_user)
                return HttpResponseRedirect(reverse('profile'))
    else:
        form = EditProfileForm()
        img_form = EditImageForm()
    sale_products = Product.objects.filter(seller=request.user.id)
    purchased_products = [purchased_product.product for purchased_product in
                          PurchasedProduct.objects.filter(user=request.user.id)]
    context = {'form': form,
               'img_form': img_form,
               'sale_products': sale_products,
               'username': CustomUser.objects.filter(id=request.user.id)[0].username,
               'email': request.user.email,
               'phone_number': request.user.phone_number,
               'image': CustomUser.objects.filter(id=request.user.id)[0].image,
               'rating': request.user.rating,
               'purchased_products': purchased_products
               }
    return render(request, 'profile.html', context)


@login_required(login_url='login')
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return HttpResponseRedirect(reverse('profile'))
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form': form
    }
    return render(request, 'password_change.html', context)


def other_profile(request, id):
    other_user = CustomUser.objects.filter(id=id)[0]
    sale_products = Product.objects.filter(seller_id=other_user.id)
    if 'rating' in request.POST:
        mark = request.POST['rating']
        other_user_rate = Ratingtabls.objects.filter(user2=other_user, user1=request.user)
        if other_user_rate:
            other_user_rate[0].rating = int(mark)
            other_user_rate[0].save()
        else:
            other_user_rate = Ratingtabls(user2=other_user, user1=request.user, rating=int(mark))
            other_user_rate.save()
        other_user.rating = ratingsumm(other_user)
        other_user.save()
    context = {'sale_products': sale_products,
               'username': other_user.username,
               'image': other_user.image,
               'rating': other_user.rating
               }
    return render(request, 'other_profile.html', context)


@login_required
def get_cart(request):
    cur_user = CustomUser.objects.get(id=request.user.id)
    users_cart = ProductInTheCart.objects.filter(user=cur_user)
    context = {}
    context['products'] = [elem.product for elem in users_cart]
    context['sum'] = sum(prod.price for prod in context['products'])
    context['cnt'] = len(users_cart)
    context['user_id'] = request.user.id
    return render(request, 'cart.html', context)


def delete_all_from_cart(request):
    cur_user = CustomUser.objects.get(id=request.user.id)
    ProductInTheCart.objects.filter(user=cur_user).delete()


@login_required
def report(request, id):
    context = {}
    product = Product.objects.filter(id=id)[0]
    seller = product.seller
    context['product'] = product
    context['seller'] = seller
    if request.method == 'POST':
        form = ReportForm(request.POST)
        context['form'] = form
        if form.is_valid():
            data = form.cleaned_data
            user = request.user
            Report.objects.create(product=product, user=user, reason=data['reason'], description=data['description'])
            return redirect(reverse('reportComplete'))
        else:
            return render(request, 'report.html', context)
    else:
        form = ReportForm()
        context['form'] = form
        return render(request, 'report.html', context)


def reportComplete(request):
    return render(request, 'reportComplete.html')


def catalogFind(request, title):
    context = {}
    if request.method == 'POST':
        form = FindForm(request.POST)
        context['form'] = form
        if form.is_valid():
            name = form.cleaned_data['name']
            return redirect('/catalog/' + name)
        else:
            return render(request, 'catalog.html', context)
    else:
        form = FindForm()
        context['form'] = form
        context['products'] = Product.objects.filter(title__contains=title)
        return render(request, 'catalog.html', context)


@login_required
def rating(request):
    current_user = request.user
    other_user = request.POST.clean_data['user_id']
    # Получить пользователя from BD
    other_user = CustomUser.objects.filter(id=other_user)
    mark = request.POST.clean_data['mark']
    item = Ratingtabls(uzer1=current_user, user2=other_user, rating=mark)
    # сохранить в бд
    item.save()
    return 200


def ratingsumm(user):
    listuser = Ratingtabls.objects.filter(user2=user)
    countall = 0
    allmarks = 0
    for u in listuser:
        allmarks += u.rating
        countall += 1
    return round(allmarks / countall, 1)


def votes_count(user):
    listuser = Ratingtabls.objects.filter(user2=user)
    countall = 0
    for u in listuser:
        countall += 1
    return countall


def tech_supp(request):
    context = {}
    return render(request, 'tech_supp.html', context)
