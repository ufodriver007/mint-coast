from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Category, Ban, User, MModel


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class BanSerializer(ModelSerializer):
    class Meta:
        model = Ban
        fields = '__all__'


class UserSerializer(ModelSerializer):
    models_count = SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'models_count')

    def get_models_count(self, instance):
        return MModel.objects.filter(user=instance).count()


class MModelSerializer(ModelSerializer):
    class Meta:
        model = MModel
        fields = '__all__'
