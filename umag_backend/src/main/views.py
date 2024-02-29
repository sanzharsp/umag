from rest_framework import generics, status
from .serializers import SupportConsultationSerializer, KeySerializer
from rest_framework.response import Response
from .models import *
from .send_bot import send_telegram_message
from rest_framework.permissions import AllowAny
import json
import requests
from django.http import JsonResponse



def message_result(id:int, status:str, type:str, key:str) -> str:

    STATUS ={
        "Создание заявки": f"Ваш {type} с аббревиатурой *{key}* зарегистрирован ✅",
        "Проверка бага": f"Ваш {type} с аббревиатурой *{key}* на проверке у баг-менеджера 🔍",
        "Backlog": f"Ваш {type} с аббревиатурой *{key}* был добавлен в Беклог в IT-блоке 🗂️📌",
        "Selected for Development": f"Ваш {type} с аббревиатурой *{key}* был взят в спринт у IT-блока 📅🚀",
        "In Progress": f"Ваш {type} с аббревиатурой *{key}* в разработке у IT-блока 👩‍💻👨‍💻",
        "Review": f"Ваш {type} с аббревиатурой *{key}* на проверке у ТехЛида/Старшего разработчика 👨‍💻🔍",
        "Test": f"Ваш {type} с аббревиатурой *{key}* на проверке у команды тестирования 📝✅",
        "Ready to deploy": f"Ваш {type} с аббревиатурой *{key}* скоро будет решен 👨‍💻",
        "Done": f"Ваш {type} с аббревиатурой *{key}* был исправлен ✔️",
        "Ожидает IT-решения": f"Ваш {type} с аббревиатурой *{key}* требует архитектурных решений Продукта, решение займет большего времени 👨‍💻📝",
        "Ожидает продуктового решения": f"Ваш {type} с аббревиатурой *{key}* требует пересмотра бизнес-логики Продукта, решение займет большего времени 📝",
        "Отказано": f"Ваш {type} с аббревиатурой *{key}* не будет взят в работу. Ознакомьтесь с принчинами ❌",
    }

    return STATUS.get(status, f"Ваш {type} с ID {id} с ключем {key} обновлен 📝. Статус (*{status}* ))""")



class SupportConsultationPost(generics.GenericAPIView):
    serializer_class = SupportConsultationSerializer
    queryset = SupportConsultation.objects.all()
    def post(self, request, *args, **kwargs):
        serializer = SupportConsultationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class IssueCreatedWebhook(generics.GenericAPIView):
    queryset = WebhookIssueCreated.objects.all()
    permission_classes = (AllowAny, )


    def post(self, request, *args, **kwargs):
        data = json.dumps(request.data, indent=2, ensure_ascii=False)
        instance = WebhookIssueCreated.objects.create(description=data)
        obj = json.loads(data)
        instance.issue_id = obj['issue']['id']
        instance.project_name =obj['issue']['fields']['project']['name']
        instance.status =obj['issue']['fields']['status']['name']
        instance.save()
        id = obj['issue']['fields'][f'{Settings.objects.first().telegram_filed}']
        #message = f"""Ваш {obj['issue']['fields']['issuetype']['name']} с ID {obj['issue']['id']} с ключем {obj['issue']['key']} зарегистрирован ✅. Статус (**{obj['issue']['fields'][('status')]['name']}** )"""
        message = f"""Ваш {obj['issue']['fields']['issuetype']['name']} с аббревиатурой {obj['issue']['key']} зарегистрирован ✅."""
        try:
            send_telegram_message(id, message)
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': e}, status=status.HTTP_400_BAD_REQUEST)





# class IssueUpdatedWebhook(generics.GenericAPIView):
#     queryset = WebhookIssueUpdated.objects.all()
#     permission_classes = (AllowAny, )
#
#
#     def post(self, request, *args, **kwargs):
#         data = json.dumps(request.data, indent=2, ensure_ascii=False)
#         instance = WebhookIssueUpdated.objects.create(description=data)
#         #data = WebhookIssueUpdated.objects.get(id=1).description
#         obj = json.loads(data)
#         instance.issue_id = obj['issue']['id']
#         instance.project_name =obj['issue']['fields']['project']['name']
#         instance.status =obj['issue']['fields']['status']['name']
#         instance.save()
#
#         id = obj['issue']['fields'][f'{Settings.objects.first().telegram_filed}']
#         message = f"""Ваш {obj['issue']['fields']['issuetype']['name']} с ID {obj['issue']['id']} с ключем {obj['issue']['key']} обновлен 📝. Статус (*{obj['issue']['fields'][('status')]['name']}* ))"""
#         try:
#             send_telegram_message(id, message)
#             return Response(status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error': e}, status=status.HTTP_400_BAD_REQUEST)


from datetime import timedelta
import datetime
import pytz

class IssueUpdatedWebhook(generics.GenericAPIView):
    queryset = WebhookIssueUpdated.objects.all()
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        data = json.dumps(request.data, indent=2, ensure_ascii=False)
        obj = json.loads(data)

        # Проверка на уникальность события
        issue_id = obj['issue']['id']
        project_name = obj['issue']['fields']['project']['name']
        status_name = obj['issue']['fields']['status']['name']

        timestamp_text = str(obj['timestamp'])  # Получаем timestamp как текст

        tz = pytz.timezone('Asia/Almaty')
        timestamp_datetime = datetime.datetime.utcfromtimestamp(int(timestamp_text) / 1000.0)
        timestamp_datetime = timestamp_datetime.replace(tzinfo=pytz.utc).astimezone(tz)

        # Переводим timestamp_datetime обратно в UTC, чтобы сравнить с created_at
        timestamp_utc = timestamp_datetime.astimezone(pytz.utc)

        # Определяем временной интервал для поиска дубликатов в UTC
        start_time = timestamp_utc - datetime.timedelta(seconds=3)
        end_time = timestamp_utc + datetime.timedelta(seconds=3)
        webhookupdate = WebhookIssueUpdated.objects.filter(issue_id=issue_id, status=status_name,
                                                  created_at__range=(start_time, end_time))
        # Проверяем, существует ли уже запись с таким же issue_id и timestamp/status
        if not webhookupdate.exists():
            instance = WebhookIssueUpdated.objects.create(description=data)
            instance.issue_id = issue_id
            instance.project_name = project_name
            instance.status = status_name
            # Если используете timestamp, сохраните его в модели
            instance.timestamp = timestamp_text
            instance.save()

            id = obj['issue']['fields'][f'{Settings.objects.first().telegram_filed}']
            message = message_result(issue_id, status_name, obj['issue']['fields']['issuetype']['name'], obj['issue']['key'])
            # = f"""Ваш {obj['issue']['fields']['issuetype']['name']} с ID {issue_id} с ключем {obj['issue']['key']} обновлен 📝. Статус (*{status_name}* ))"""
            try:
                send_telegram_message(id, message)
                return Response(status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            webhookupdate.first().delete()
            # Запись существует, игнорируем дубликат
            return JsonResponse({'message': 'Event already processed'}, status=status.HTTP_200_OK)



class IssueDeletedWebhook(generics.GenericAPIView):
    queryset = WebhookIssueDeleted.objects.all()
    permission_classes = (AllowAny, )


    def post(self, request, *args, **kwargs):
        data = json.dumps(request.data, indent=2, ensure_ascii=False)
        instance = WebhookIssueDeleted.objects.create(description=data)
        obj = json.loads(data)
        instance.issue_id = obj['issue']['id']
        instance.project_name =obj['issue']['fields']['project']['name']
        instance.status =obj['issue']['fields']['status']['name']
        instance.save()
        id = obj['issue']['fields'][f'{Settings.objects.first().telegram_filed}']
        #message = f"""Ваш {obj['issue']['fields']['issuetype']['name']} с ID {obj['issue']['id']} с ключем {obj['issue']['key']} удалено ❌ со статусом (**{obj['issue']['fields'][('status')]['name']}** )"""
        message = f"""Ваш {obj['issue']['fields']['issuetype']['name']} с аббревиатурой {obj['issue']['key']} удален ❌."""
        try:
            send_telegram_message(id, message)
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': e}, status=status.HTTP_400_BAD_REQUEST)



class AmoCrmWebhook(generics.GenericAPIView):
    queryset = AmoCrmWebhookModel.objects.all()
    permission_classes = (AllowAny, )


    def post(self, request, *args, **kwargs):
        pass
        #telegram = requests.post('https://pay.ziz.kz/api/webhook/amo_crm', json = request.data)
        #telegram = requests.post('https://umag.ziz.kz/api/webhook/amo_crm', json = request.data)
        #telegram = requests.post('https://pay.ziz.kz/api/bot', json = request.data)
        #requests.post('https://amojo.amocrm.ru/~external/hooks/telegram?t=6397638357:AAEF4kljx7MgkA56vx5jTbB-lAjWkLVLVk4', json = request.data)
        #data = json.dumps(request.data, indent=2, ensure_ascii=False)
        #AmoCrmWebhookModel.objects.create(description=request.data)
        #return Response(status=status.HTTP_200_OK)


class AccessTokenApi(generics.GenericAPIView):
    permission_classes = (AllowAny, )
    serializer_class = KeySerializer


    def post(self, request, *args, **kwargs):
        serializer = KeySerializer(data=request.data)
        if serializer.is_valid(raise_exception = True):
            if serializer.data['key'] == Settings.objects.first().amo_secret_key:
                return Response({'access_token': RefreshAccessToken.objects.first().access_token}, status=status.HTTP_200_OK)
            return Response({"detail": "Ваш ключь не актуален или не верен"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(status=status.HTTP_400_BAD_REQUEST)