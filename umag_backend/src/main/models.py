from django.db import models
from django.core.exceptions import ValidationError

class SingletonModel(models.Model):
    # Ваши поля здесь

    def save(self, *args, **kwargs):
        if not self.pk and SingletonModel.objects.exists():
            # Если вы пытаетесь сохранить новый объект, когда уже существует один, выбросите исключение
            raise ValidationError('There can be only one SingletonModel instance')
        return super(SingletonModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True  # Это делает модель абстрактной, чтобы она не создавала отдельную таблицу в базе данных


class SupportConsultation(models.Model):
    telegram_id = models.BigIntegerField(verbose_name="id пользователя в телеграмм")
    first_name = models.CharField(max_length=100, db_index=True, verbose_name="Имя пользователя")
    franchise_name = models.CharField(max_length=100, verbose_name="Наименование франшизы")
    phone_number = models.CharField(max_length=15, verbose_name="Номер телефона")
    description_problem = models.TextField(verbose_name="Описание проблемы")
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"{self.telegram_id} {self.first_name}"

    class Meta:
        verbose_name = "объект 'Консультация'"
        verbose_name_plural = "Консультации"

class Settings(models.Model):
    telegram_filed = models.CharField(verbose_name="Название поля для телеграм", max_length=255)
    username = models.CharField(verbose_name="Название пользователя jira", max_length= 100)
    api_token = models.TextField(verbose_name="Токен аккаунта jira")
    jira_url = models.URLField(verbose_name="Ссылка на базовый путь проекта")
    amo_id = models.TextField(verbose_name="ID интеграций")
    amo_secret_key = models.TextField(verbose_name="Секретный ключь")
    amo_auth_key = models.TextField(verbose_name="Код авторизаций")
    redirect_url = models.URLField(verbose_name="Путь перенаправления")
    subdomain = models.CharField(max_length=120, verbose_name="Субдомен в АМО СРМ")

    def __str__(self):
        return f"{self.telegram_filed}"

    class Meta:
        verbose_name = "Настройка"
        verbose_name_plural = "Настойки"



class WebhookIssueCreated(models.Model):
    issue_id = models.CharField( max_length=255, verbose_name="Идентификатор")
    project_name = models.TextField(verbose_name="Название проекта")
    status = models.CharField(max_length=255, verbose_name="Статус", blank=True, null=True)
    description = models.TextField(blank=True, verbose_name="ответ на вебхук")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    def __str__(self):
        return f"{self.id} "

    class Meta:
        verbose_name = "Создание проблемы"
        verbose_name_plural = "Создание проблемы"



class WebhookIssueUpdated(models.Model):
    issue_id = models.CharField( max_length=255, verbose_name="Идентификатор")
    project_name = models.TextField(verbose_name="Название проекта")
    status = models.CharField(max_length=255, verbose_name="Статус", blank=True, null=True)
    description = models.TextField(blank=True, verbose_name="ответ на вебхук")
    timestamp = models.TextField(verbose_name="Дата и время создания", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    def __str__(self):
        return f"{self.id} "

    class Meta:
        verbose_name = "Проблема обновлена"
        verbose_name_plural = "Проблема обновлена"

class WebhookIssueDeleted(models.Model):
    issue_id = models.CharField( max_length=255, verbose_name="Идентификатор")
    project_name = models.TextField(verbose_name="Название проекта")
    status = models.CharField(max_length=255, verbose_name="Статус", blank=True, null=True)

    description = models.TextField(blank=True, verbose_name="ответ на вебхук")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    def __str__(self):
        return f"{self.id} "

    class Meta:
        verbose_name = "Проблема удалена"
        verbose_name_plural = "Проблема удалена"


class AmoCrmWebhookModel(models.Model):
    description = models.TextField(blank=True, verbose_name="ответ на вебхук")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    def __str__(self):
        return f"{self.id} "

    class Meta:
        verbose_name = "Webhook Amo crm"
        verbose_name_plural = "Webhook Amo crm"

class RefreshAccessToken(models.Model):
    access_token = models.TextField(verbose_name="Токен доступа")
    refresh_token = models.TextField(verbose_name="Токен обновления")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Время обновления")

    def __str__(self):
        return f"{self.id}"

    class Meta:
        verbose_name = "Токен доступа и обновления"
        verbose_name_plural = "Токен доступа и обновления"