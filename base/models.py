from codecs import backslashreplace_errors
from doctest import BLANKLINE_MARKER
from django.utils import timezone
# from datetime import datetime
from .validations import DescriptionValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db.models.signals import pre_save


class UserManager(BaseUserManager):
    def create_user(self, email, name, city, age, password=None):
        if not email:
            raise ValueError('Email can\'t be null')
        if not name:
            raise ValueError('Name can\'t be null')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            city=city,
            age=age,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, city, age, password):
        user = self.create_user(
            email=self.normalize_email(email),
            name=name,
            city=city,
            age=age,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    name = models.CharField(max_length=50)
    age = models.IntegerField(default=0, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    users = UserManager()

    def __str__(self) -> str:
        return self.name

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def save(self, *args, **kwargs):
        self.country = 'Pakistan'
        self.created = timezone.now()
        return super(User, self).save(*args, **kwargs)


class TaskQuerySet(models.QuerySet):
    def sorted(self, param):
        return self.order_by(f'{param}')


class TaskManager(models.Manager):
    def get_queryset(self):
        return TaskQuerySet(model=self.model, using=self._db)


class Task(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(validators=[DescriptionValidator])
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField()

    REQUIRED_FIELDS = ['title', 'description']

    tasks = TaskManager()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.updated = timezone.now()
        return super(Task, self).save(*args, **kwargs)

    class Meta:
        ordering = ['complete']


def task_pre_save(sender, instance, *args, **kwargs):
    if not instance.title.istitle():
        instance.title = instance.title.title()
        instance.save()

    if instance.description and not instance.description[0].isupper():
        instance.description = instance.description.capitalize()
        instance.save()


pre_save.connect(task_pre_save, sender=Task)
