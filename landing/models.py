from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _


# Company Model
class Company(models.Model):
    company_name = models.CharField(max_length=30, unique=True)
    created_by = models.ForeignKey("CustomUser",on_delete=models.CASCADE,related_name="created_companies",)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey("CustomUser",on_delete=models.CASCADE,related_name="updated_companies",)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name

# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_("The Email field must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError(_("Superuser must have is_staff=True."))
        if not extra_fields.get('is_superuser'):
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(email, password, **extra_fields)

# Custom User Model
class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=15, unique=True)
    company = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,
        related_name="users",
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email

class BillDetails(models.Model):
    BillNumber = models.CharField(max_length=100, unique=True)
    date = models.DateField()
    time = models.TimeField()
    TableNumber = models.CharField(max_length=100)
    Waiter = models.CharField(max_length=100)
    PaymentType = models.CharField(max_length=100)
    Cashier = models.CharField(max_length=100)
    FoodMenu = models.JSONField()
    Price = models.FloatField()
    GSTPercentage = models.FloatField()
    GSTValue = models.FloatField()
    RoundOff = models.FloatField()
    TotalPrice = models.FloatField()

    def __str__(self):
        return self.BillNumber

class deletedBillDetails(models.Model):
    BillNumber = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    TableNumber = models.CharField(max_length=100)
    Waiter = models.CharField(max_length=100)
    PaymentType = models.CharField(max_length=100)
    Cashier = models.CharField(max_length=100)
    FoodMenu = models.JSONField()
    Price = models.FloatField()
    GSTPercentage = models.FloatField()
    GSTValue = models.FloatField()
    RoundOff = models.FloatField()
    TotalPrice = models.FloatField()

    def __str__(self):
        return self.BillNumber

