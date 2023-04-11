from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import CharField, EmailField

User = get_user_model()


class CreationForm(UserCreationForm):
    email = EmailField(
        required=True,
        label='Почта',
        error_messages={'unique': 'Почта уже занята.'}
    )
    first_name = CharField(
        required=True,
        label='Имя'
    )
    last_name = CharField(
        required=True,
        label='Фамилия'
    )
    username = CharField(required=True, label='Имя пользователя')

    class Meta(UserCreationForm.Meta):
        fields = ('email', 'first_name', 'last_name', 'username')
        model = User
