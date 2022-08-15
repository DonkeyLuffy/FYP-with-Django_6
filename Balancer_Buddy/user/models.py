from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from django.utils.translation import gettext_lazy as _
# Min and Max validators
from django.core.validators import MinValueValidator, MaxValueValidator
# datetime

# Create your models here.

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

from datetime import datetime
# Create your models here.

dateTimeObj = datetime.now()
today = dateTimeObj.strftime("%Y-%m-%d")     

class Profile(models.Model):
    WEIGHT_TYPE = (
            ('kg','kg'),
            ('lbs', 'lbs'),
    )

    SIZE_TYPE = (
            ('US/Canada', 'US/Canada'),
            ('UK', 'UK'),
            ('Europe', 'Europe'),
            ('Japan', 'Japan'),
            ('Length(cm)', 'Length(cm)'),
            ('Length(inch)', 'Length(inch)'),
    )

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, unique=True, db_index=True)
    birth_date = models.DateField(default=today, blank=True)
    adress = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.BigIntegerField(blank=True, null=True)
    weight = models.SmallIntegerField(validators=[MinValueValidator(30), MaxValueValidator(150)], blank=True, null=True)
    weight_type = models.CharField(max_length=255, choices=WEIGHT_TYPE, default='US/Canada')
    shoe_size = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(60)], blank=True, null=True)
    size_type = models.CharField(max_length=255, choices=SIZE_TYPE, default='kg')
    @property
    def age(self):
        return int((datetime.now().date() - self.birth_date).days / 365.25)

    def __str__(self):
        return  f"User: {self.user}| Phone Number: {self.phone_number}| Age:{self.age} |Weight: {self.weight}{self.weight_type}| Shoe Size: {self.shoe_size}{self.size_type} "

class DeviceData(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, unique=False, db_index=True)
    heel = models.BooleanField(default=False)
    bigtoe = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)

    @property
    def timing(self):
        return {self.time}

    def __str__(self):
        return f"Heel: {self.heel}| Bigtoe: {self.bigtoe}| Date: {self.date}| Time: {self.time}"