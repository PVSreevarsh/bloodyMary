import json

# from rest_framework import serializers

# from .models import Message, Thread

from rest_framework import serializers
from .models import Investment,SME,Sector


class smeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SME
        fields = ['sector','askamt','givenamt', 'name','label', 'gstn','amtpaid', 'phoneNumber']

class InvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investment
        fields = ['bank', 'sector', 'amount', 'timestamp']


class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = ['name', 'risk_classification','total_amount', 'total_ask','id']
