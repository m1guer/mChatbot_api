from rest_framework.serializers import ModelSerializer
from ..models import Clients


class ClientsSerializers(ModelSerializer):
    class Meta:
        model = Clients
        fields = "__all__"
