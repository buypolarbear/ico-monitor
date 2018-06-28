from rest_framework import serializers
from .models import Token, Volume


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ('name', 'address')

    def validate_address(self, address):
        if not address.startswith('0x') or len(address)<42 or len(address)>50:
            raise serializers.ValidationError('Address is not valid.')
        return address

class VolumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Volume
        fields = '__all__'
