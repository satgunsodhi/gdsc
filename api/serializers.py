from rest_framework.serializers import ModelSerializer
from api.models import News

class NewsSerializer(ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'