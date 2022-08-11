from rest_framework import serializers
from .models import user,Application


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = ['name','email','phone_number','password']
        
    def create(self,validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
            instance.is_active=True
            
        instance.save()
        return instance
    
class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = ['name','email','phone_number','password']
        
    def create(self,validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
            instance.is_active=True
            instance.is_admin=True
            instance.is_staff=True
            instance.is_superuser=True
        instance.save()
        return instance
    

class ALSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['name','address','city',]
        
    def create(self,validated_data):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        instance = self.Meta.model(**validated_data)
        instance.user = user
        instance.save()
        return instance