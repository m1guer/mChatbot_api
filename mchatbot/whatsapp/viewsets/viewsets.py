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
            "Authorization": "Bearer EAACDHcMuPpIBAI2ZA4V5LXg62YPWh8FuAlWQSebZBbaHfMZCjui2t5U1yLEULauqJxuC5kki0OlDKxed6W7qt0AoZC8DwJRdL8dAGNgg1kpV9vhSMZALVp2IjQ0HEITjPz9Yn3GRveL70Va1EryPOjZCiAd1ZAc7tMPevc0AdyFKemSaJFb2E5dssImHVZC0H0nz2xM7pRRAuQZDZD",
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
        name = json_data['entry'][0]['changes'][0]['value']['contacts'][0]['profile']['name']
        numero = json_data['entry'][0]['changes'][0]['value']['contacts'][0]["wa_id"]
        if request.method == 'POST':
            if 'contacts' in json_data['entry'][0]['changes'][0]['value']:
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
