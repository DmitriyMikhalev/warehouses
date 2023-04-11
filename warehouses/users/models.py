from django.contrib.auth.models import AbstractUser
from django.db.models import EmailField, CharField


class User(AbstractUser):
    email = EmailField(verbose_name='Почта', unique=True)
    first_name = CharField(verbose_name='Имя', max_length=150)
    last_name = CharField(verbose_name='Фамилия', max_length=150)

    REQUIRED_FIELDS = ('email', 'first_name', 'last_name')

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    def get_full_name(self):
        full_name = f'{self.first_name} {self.last_name}'
        return full_name.strip()

    def get_short_name(self):
        return self.first_name
