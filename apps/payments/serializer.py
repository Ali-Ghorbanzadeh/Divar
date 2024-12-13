from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer
from .models import Payment, Flags
from apps.advertisement.models import Ad

class PaymentSerializer(ModelSerializer):
    price = SlugRelatedField(
        slug_field='flag__price',
        read_only=True
    )
    class Meta:
        model = Payment
        fields = ['advertise',
                  'status',
                  'flag',
                  'price']

        extra_kwargs = {
            {'status': {'required': False,'read_only': True}},
            {'price': {'required': False,'read_only': True}},
        }

    def create(self, validated_data):
        flag = Flags.objects.filter(name=validated_data.data.get('flag'))
        assert flag.exists(), 'Flag does not exist'

        advertise = Ad.objects.filter(id=validated_data.data.get('advertise'))
        assert advertise.exists(), 'Advertise does not exist'
        instance = Payment.objects.get_or_create(advertise=advertise[0], flag=flag[0])
        return instance

    def update(self, instance, validated_data):
        # Before changing the payment status, there is a need to check whether the payment was successful from the portal
        # new_status = ...
        # instance.status = new_status
        # instance.save()

        instance.status = validated_data.get('status', instance.status)
        return instance