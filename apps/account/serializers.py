from core.serializers import ExModelSerializer
from django.contrib.auth.models import User

class UserSerializer(ExModelSerializer):
    class Meta:
        model = User
        exclude = ()
