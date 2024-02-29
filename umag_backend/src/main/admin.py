from django.contrib import admin
from unfold.contrib.import_export.forms import ExportForm, ImportForm
from import_export.admin import ImportExportModelAdmin
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from unfold.admin import ModelAdmin
from django.contrib.auth.models import User




admin.site.unregister(User)


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    pass
class SupportConsultationAdmin(ModelAdmin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    list_display = ('telegram_id', 'first_name', 'franchise_name', 'phone_number', 'creation_date')
    list_filter = ('creation_date', )
    search_fields = ('telegram_id', 'first_name', 'franchise_name', 'phone_number', 'description_problem')
    list_editable = ('first_name', 'franchise_name', 'phone_number', )


class SettingsModelAdmin(ModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    def has_add_permission(self, request):
        # Разрешить добавление, только если записей еще нет
        return not Settings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Опционально: запретить удаление
        return False

    def has_change_permission(self, request, obj=None):
        # Опционально: разрешить изменение только если уже есть запись
        return Settings.objects.exists()


class RefreshAccessTokenAdmin(ModelAdmin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    list_display = ('created_at', 'updated_at', )
    def has_add_permission(self, request):
        # Разрешить добавление, только если записей еще нет
        return not RefreshAccessToken.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Опционально: запретить удаление
        return False

    def has_change_permission(self, request, obj=None):
        # Опционально: разрешить изменение только если уже есть запись
        return RefreshAccessToken.objects.exists()


class WebhookIssueCreatedAdmin(ModelAdmin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    list_display = ('created_at', 'issue_id', 'project_name', 'status', 'id', )
    list_per_page = 25
    list_max_show_all = 1000
class WebhookIssueUpdatedAdmin(ModelAdmin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    list_display = ('created_at', 'issue_id', 'project_name', 'status', 'id', )
    list_per_page = 25
    list_max_show_all = 1000

class WebhookIssueDeletedAdmin(ModelAdmin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    list_display = ('created_at', 'issue_id', 'project_name', 'status', 'id', )
    list_per_page = 25
    list_max_show_all = 1000



admin.site.register(SupportConsultation, SupportConsultationAdmin)
admin.site.register(Settings, SettingsModelAdmin)
admin.site.register(RefreshAccessToken, RefreshAccessTokenAdmin)
admin.site.register(WebhookIssueCreated, WebhookIssueCreatedAdmin)
admin.site.register(WebhookIssueUpdated, WebhookIssueUpdatedAdmin)
admin.site.register(AmoCrmWebhookModel)
admin.site.register(WebhookIssueDeleted, WebhookIssueDeletedAdmin)