from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from whatsapp.serializers.clients_serializer import ClientsSerializers
from whatsapp.models import Clients


class ClientViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Clients.objects.all()
        serializer = ClientsSerializers(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get', 'post'])
    def webhook(self, request, *args, **kwargs):
        json_data = request.data
        name = json_data['entry'][0]['changes'][0]['value']['contacts'][0]['profile']['name']
        numero_client = json_data['entry'][0]['changes'][0]['value']['contacts'][0]['wa_id']
        client = Clients()
        client.nome = name
        client.numero_whatsapp = numero_client
        client.save()
        return Response({'OK'})
