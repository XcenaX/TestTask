from django.db import models
from main.managers import CustomUserManager
from django.contrib.auth.models import AbstractUser


class ChildCompany(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название компании')
    address = models.CharField(max_length=255, verbose_name='Адрес')
    industry = models.CharField(max_length=100, verbose_name='Отрасль')

    class Meta:
        verbose_name = 'Дочерняя компания'
        verbose_name_plural = 'Дочерние компании'

    def __str__(self):
        return self.name


class Contractor(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название компании')
    address = models.CharField(max_length=255, verbose_name='Адрес')
    service_domain = models.CharField(max_length=100, verbose_name='Сфера услуг')
    license_number = models.CharField(max_length=100, verbose_name='Номер лицензии')

    class Meta:
        verbose_name = 'Подрядчик'
        verbose_name_plural = 'Подрядчики'

    def __str__(self):
        return self.name


class ContractRole(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название должности')
    description = models.TextField(blank=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Роль по договору'
        verbose_name_plural = 'Роли по договорам'

    def __str__(self):
        return self.name
    

class Contract(models.Model):
    child_company = models.ForeignKey(ChildCompany, related_name='contracts', on_delete=models.CASCADE, verbose_name='Дочерняя компания')
    contractor = models.ForeignKey(Contractor, related_name='contracts', on_delete=models.CASCADE, verbose_name='Подрядчик')
    name = models.TextField(default="Контракт", verbose_name='Имя')
    description = models.TextField(default="", verbose_name='Описание')
    roles = models.ManyToManyField(ContractRole, related_name='contracts', verbose_name='Роли имеющие доступ к контракту', blank=True)
    start_date = models.DateField(verbose_name='Дата начала')
    end_date = models.DateField(verbose_name='Дата окончания')
    contract_document = models.FileField(upload_to='contracts/', verbose_name='Документ договора')

    class Meta:
        verbose_name = 'Договор'
        verbose_name_plural = 'Договоры'

    def __str__(self):
        return f'{self.child_company} - {self.contractor}'


class User(AbstractUser):
    email = models.EmailField(unique=True, db_index=True, verbose_name='Email адрес')
    roles = models.ManyToManyField(ContractRole, related_name='users', verbose_name='Роли пользователя', blank=True)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email
    

class ContractAccess(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, verbose_name='Договор')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    role = models.ForeignKey(ContractRole, on_delete=models.CASCADE, verbose_name='Роль по договору')

    class Meta:
        verbose_name = 'Доступ к договору'
        verbose_name_plural = 'Доступы к договорам'

    def __str__(self):
        return f'{self.user} - {self.contract} - {self.role}'