from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)
    profile_pic = models.ImageField(null=True, blank=True, upload_to="images/profile/")

def __str__(self):
    return str(self.user)

class Category(models.Model):
    Tank = 'TK'
    Healer = 'HL'
    Damage_dealer = 'DD'
    Trader = 'TD'
    Guild_master ='GM'
    Quest_giver = 'QG'
    Blacksmith = 'BS'
    Tanner = 'TN'
    Potion_master = 'PM'
    Spell_master = 'SM'

    Categories = [
    (Tank, 'Танки'),
    (Healer, 'Хилеры'),
    (Damage_dealer, 'Дамагеры'),
    (Trader, 'Торговцы'),
    (Guild_master, 'Гилдмастеры'),
    (Quest_giver, 'Квестгиверы'),
    (Blacksmith, 'Кузнецы'),
    (Tanner, 'Кожевники'),
    (Potion_master, 'Зельевары'),
    (Spell_master, 'Мастер заклинаний'),
    ]

    cetegory = models.CharField(max_length=2, choices=Categories, Default=Tank)

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.name = None

        def __str__(self):
            return f"{self.caregory}"


class Post(models.Model):
    title = models.CharField(max_length=120, verbose_name='Заголовок')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Автор')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    content = models.RichTextField(verbose_name='Текст поста')
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/{self.pk}'

class Reply(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Как статья?')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    dateCreation = models.DeteTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.post} ==> {self.author}: {self.text}'