from celery import shared_task
from .models import RefreshAccessToken, Settings, WebhookIssueCreated, WebhookIssueUpdated, WebhookIssueDeleted

@shared_task
def delete_hook_data():
    WebhookIssueCreated.objects.all().delete()
    WebhookIssueUpdated.objects.all().delete()
    WebhookIssueDeleted.objects.all().delete()



@shared_task
def access_refresh():
    import requests
    try:
        refresh_token_instance = RefreshAccessToken.objects.first()
        settings_instance = Settings.objects.first()

        if refresh_token_instance and settings_instance:
            data = {
                "client_id": settings_instance.amo_id,
                "client_secret": settings_instance.amo_secret_key,
                "grant_type": "refresh_token",
                "refresh_token": refresh_token_instance.refresh_token,
                "redirect_uri": settings_instance.redirect_url
            }
            response = requests.post(f"https://{settings_instance.subdomain}.amocrm.ru/oauth2/access_token", json=data)
            
            if response.status_code == 200:
                response_data = response.json()
                if 'refresh_token' in response_data and 'access_token' in response_data:
                    refresh_token_instance.refresh_token = response_data["refresh_token"]
                    refresh_token_instance.access_token = response_data["access_token"]
                    refresh_token_instance.save()
                    print("Tokens updated successfully.")
                else:
                    # Handle the case where 'refresh_token' or 'access_token' is not in response
                    print("Expected token(s) not in response. Response:", response_data)
            else:
                # Handle non-successful status codes
                print(f"Failed to refresh token. Status code: {response.status_code}, Response: {response.text}")
        else:
            print("Refresh token instance or settings instance not found.")
    except Exception as e:
        print(f"An error occurred: {e}")



