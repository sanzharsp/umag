
from django.urls import path
from .views import *

urlpatterns = [
    path('support-consultation/', SupportConsultationPost.as_view()),
    path('webhook/issue_created', IssueCreatedWebhook.as_view()),
    path('webhook/issue_updated', IssueUpdatedWebhook.as_view()),
    path('webhook/issue_deleted', IssueDeletedWebhook.as_view()),
    path('webhook/amo_crm', AmoCrmWebhook.as_view()),
    path('token/get', AccessTokenApi .as_view()),
    
]
