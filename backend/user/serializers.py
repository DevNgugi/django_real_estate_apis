from rest_framework import serializers 
from django.contrib.auth  import get_user_model
User=get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('name','email','is_realtor')
        
    def capitalize_each_word(self, value):
        # Capitalize each word in the string
        return ' '.join(word.capitalize() for word in value.split())

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['name'] = self.capitalize_each_word(data['name'])
        
        return data
