from rest_framework import serializers
from sampling.models import *

class SamplingSerializer(serializers.ModelSerializer):
    quotas = serializers.StringRelatedField()
    class Meta:
        model = Sampling
        fields = '__all__'