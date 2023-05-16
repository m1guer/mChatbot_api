from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from whatsapp.serializers.clients_serializer import ClientsSerializers
from whatsapp.models import Clients
import requests
import json


class ClientViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Clients.objects.all()
        serializer = ClientsSerializers(queryset, many=True)
        return Response(serializer.data)

    def sent_message(self, numero, nome):
        url = "https://graph.facebook.com/v16.0/121601520926198/messages"
        headers = {
            "Authorization": "Bearer EAACDHcMuPpIBAIrtbpsyIi8bCLOn4JLNaiKgGZCCPAAHark0CugEVRh0aOjRZC8h9xbcUpA5yZATZCzWNVZAu2Pp6zvZA7jPXuxMmIyoZBPjeUZAuDPMbb6Q3ZCIzqMpMgmii6IAYZBzEXosZAI4NY2Tw0Wx7tblA8FmpGwgZCP4KY0DnHEBZBF5dZCrwJBtk3a055g8OR0cvdnxccywZDZD",
            "Content-Type": "application/json",
        }
        body = {
            "messaging_product": "whatsapp",
            "to": numero,
            "type": "text",
            "text": {
                "body": "Olá " + nome
            }
        }

        r = requests.post(url, headers=headers, data=json.dumps(body))
        return r

    @action(detail=False, methods=['get', 'post'])
    def webhook(self, request, *args, **kwargs):
        # verificação do faecbook para meu webhook
        if request.method == 'GET':
            hub_challenge = request.query_params.get('hub.challenge')
            data = json.loads(hub_challenge)
            return Response(data)

        cliente = Clients()
        json_data = request.data
        if request.method == 'POST':
            if 'contacts' in json_data['entry'][0]['changes'][0]['value']:
                name = json_data['entry'][0]['changes'][0]['value']['contacts'][0]['profile']['name']
                numero = json_data['entry'][0]['changes'][0]['value']['contacts'][0]["wa_id"]
                try:
                    verify_numero_exists = Clients.objects.get(
                        numero_whatsapp=numero)
                    self.sent_message(nome=name, numero=numero)
                    return Response({'status': 'ok'})
                except Clients.DoesNotExist:
                    cliente.nome = name
                    cliente.numero_whatsapp = numero
                    cliente.save()
                    self.sent_message(nome=name, numero=numero)
                    return Response({'status': 'ok'})
            else:
                status_message = json_data['entry'][0]['changes'][0]['value']['statuses'][0]['status']
                status = ''
                if "sent" in status_message:
                    status = Clients.SENT
                elif "delivered" in status_message:
                    status = Clients.DELIVERIED
                if 'conversation' in json_data['entry'][0]['changes'][0]['value']['statuses']:
                    conversation_id = json_data['entry'][0]['changes'][0]['value']['statuses'][0]['conversation']['id']
                    recipient_id = json_data['entry'][0]['changes'][0]['value']['statuses'][0]['recipient_id']
                    try:
                        updateClientsInfo = Clients.objects.get(
                            numero_whatsapp=recipient_id)
                        updateClientsInfo.conversation_id = conversation_id
                        updateClientsInfo.status_mensage = status
                        updateClientsInfo.save()
                        return Response({'status': 'ok'})
                    except Clients.DoesNotExist:
                        return Response({'status': 'error'})
                else:
                    try:
                        recipient_id = json_data['entry'][0]['changes'][0]['value']['statuses'][0]['recipient_id']
                        lastStatusMessage = Clients.objects.get(
                            numero_whatsapp=recipient_id)
                        lastStatusMessage.status_mensage = Clients.READ
                        lastStatusMessage.save()
                        return Response({'status': 'message updated to read'})
                    except Clients.DoesNotExist:
                        return Response({'status': 'error'})
