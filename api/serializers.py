# backend/api/serializers.py
from rest_framework import serializers
from .models import CR, Student

class CRSerializer(serializers.ModelSerializer):
    class Meta:
        model = CR
        fields = '__all__'
        
    def create(self, validated_data):
        request = self.context.get('request')
        cr_id = request.data.get('cr_id')  # frontend should send cr_id or assign default
        if cr_id:
            validated_data['cr'] = CR.objects.get(id=cr_id)
        return super().create(validated_data)


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
        
  