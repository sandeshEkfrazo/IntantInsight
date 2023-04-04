from rest_framework import serializers
from .models import *


class userOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSurveyOffers
        fields = '__all__'

class userPointsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSurveyPoints
        fields = '__all__'