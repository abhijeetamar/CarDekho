from rest_framework import serializers
from .models import Carlist,Showroomlist,Review

def alphanumeric(value):
    if not str(value).isalnum():
        raise serializers.ValidationError('only alphanumeric characters are allowed')
    
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=Review
        fields="__all__"



class CarSerializer(serializers.ModelSerializer):
    discounted_price = serializers.SerializerMethodField()
    Reviews = ReviewSerializer(many=True,read_only = True)
    class Meta:
        model=Carlist
        fields="__all__"



    def get_discounted_price(self,object):
        if object.price is not None:
            return object.price - 5000
        return None
        

    
    #field level validator
    
    def validate_price(self,value):
        if value<=20000.00:
            raise serializers.ValidationError('Price must be greater than 20000.00')
        return value
    
     # Object-level validator
    def validate(self, data):
        if data['name'].lower() == data['description'].lower():
            raise serializers.ValidationError("Name and Description cannot be same")
        return data

class ShowroomSerializer(serializers.ModelSerializer):
    #Showrooms=CarSerializer(many=True,read_only=True)
    #Showrooms=serializers.StringRelatedField(many=True)
    #Showrooms=serializers.PrimaryKeyRelatedField(many=True,read_only=True)
    Showrooms=serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='car_detail'
    )
    class Meta:
        model=Showroomlist
        fields="__all__"

