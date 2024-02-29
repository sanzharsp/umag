# Generated by Django 5.0.1 on 2024-01-27 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RefreshAccessToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_token', models.TextField(verbose_name='Токен доступа')),
                ('refresh_token', models.TextField(verbose_name='Токен обновления')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Время обновления')),
            ],
            options={
                'verbose_name': 'Токен доступа и обновления',
                'verbose_name_plural': 'Токен доступа и обновления',
            },
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_filed', models.CharField(max_length=255, verbose_name='Название поля для телеграм')),
                ('username', models.CharField(max_length=100, verbose_name='Название пользователя jira')),
                ('api_token', models.TextField(verbose_name='Токен аккаунта jira')),
                ('jira_url', models.URLField(verbose_name='Ссылка на базовый путь проекта')),
                ('amo_id', models.TextField(verbose_name='ID интеграций')),
                ('amo_secret_key', models.TextField(verbose_name='Секретный ключь')),
                ('amo_auth_key', models.TextField(verbose_name='Код авторизаций')),
                ('redirect_url', models.URLField(verbose_name='Путь перенаправления')),
                ('subdomain', models.CharField(max_length=120, verbose_name='Субдомен в АМО СРМ')),
            ],
            options={
                'verbose_name': 'Настройка',
                'verbose_name_plural': 'Настойки',
            },
        ),
        migrations.CreateModel(
            name='SupportConsultation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_id', models.BigIntegerField(verbose_name='id пользователя в телеграмм')),
                ('first_name', models.CharField(db_index=True, max_length=100, verbose_name='Имя пользователя')),
                ('franchise_name', models.CharField(max_length=100, verbose_name='Наименование франшизы')),
                ('phone_number', models.CharField(max_length=15, verbose_name='Номер телефона')),
                ('description_problem', models.TextField(verbose_name='Описание проблемы')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
            ],
            options={
                'verbose_name': "объект 'Консультация'",
                'verbose_name_plural': 'Консультации',
            },
        ),
        migrations.CreateModel(
            name='WebhookIssueCreated',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, verbose_name='ответ на вебхук')),
            ],
            options={
                'verbose_name': 'Создание проблемы',
                'verbose_name_plural': 'Создание проблемы',
            },
        ),
        migrations.CreateModel(
            name='WebhookIssueDeleted',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, verbose_name='ответ на вебхук')),
            ],
            options={
                'verbose_name': 'Проблема удалена',
                'verbose_name_plural': 'Проблема удалена',
            },
        ),
        migrations.CreateModel(
            name='WebhookIssueUpdated',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, verbose_name='ответ на вебхук')),
            ],
            options={
                'verbose_name': 'Проблема обновлена',
                'verbose_name_plural': 'Проблема обновлена',
            },
        ),
    ]
