from rest_framework import serializers
from .models import GPT,Business 



# create serializer 
# create Views
# create Urls 

class GPTSerializer(serializers.ModelSerializer):
    class Meta:
        model = GPT
        fields = '__all__' #will include all fields from the model

class  BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = '__all__' #will include all fields from the model