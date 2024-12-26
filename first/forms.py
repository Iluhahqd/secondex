from django import forms
from django.contrib.auth.forms import UserCreationForm, User
from django.contrib.auth import get_user_model
from .models import CustomUser


class LoginUserForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Логин'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Пароль'}))


# class SigneUpForm(UserCreationForm):
#     class Meta:
#         model = CustomUser
#         fields = ('username', 'password1', 'password2', 'phone_number', 'email', 'image')
class SignUpForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя пользователя'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

class AddProductForm(forms.Form):
    seller = forms.ModelForm

    title = forms.CharField(
        label='Название',
        max_length=200,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    description = forms.CharField(
        label='Описание',
        max_length=200,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'style': 'height:40px; width:100%; resize: none;',
            }
        )
    )
    price = forms.IntegerField(label="Цена")
    type = forms.CharField(label='Тип товара', max_length=200)
    available = forms.BooleanField(label='Наличие')


class Meta(UserCreationForm.Meta):
    model = get_user_model()


class EditProfileForm(forms.ModelForm):
    username = forms.CharField(label='Новый логин', widget=forms.TextInput(attrs={'class': 'form-input'}),
                               empty_value=CustomUser.username)

    class Meta:
        model = CustomUser
        fields = ('username',)


class EditImageForm(forms.ModelForm):
    image = forms.ImageField()

    class Meta:
        model = CustomUser
        fields = ('image',)


class ReportForm(forms.Form):
    reason = forms.CharField(label='Причина репорта',
                             widget=forms.TextInput(attrs={'class': 'form-input', 'style': 'width:350px'}))
    description = forms.CharField(label='Описание репорта',
                                  widget=forms.Textarea(attrs={'class': 'form-control', 'style': 'height:500px'}))


class FindForm(forms.Form):
    name = forms.CharField(required=False, label='', widget=forms.TextInput(attrs={'class': 'form-find', 'placeholder': 'Искать товары', 'style':'width: 600px'}))


class AddAnswerForm(forms.Form):
    comment = forms.IntegerField(widget=forms.HiddenInput())
    text = forms.CharField(label='Текст',
                           widget=forms.Textarea(attrs={'class': 'form-control', 'style': 'height:100px'}))


class AddCommentForm(forms.Form):
    text = forms.CharField(label='Текст',
                           widget=forms.Textarea(attrs={'class': 'form-control', 'style': 'height:100px'}))
