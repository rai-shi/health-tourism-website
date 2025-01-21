from rest_framework import serializers
from patient.models import MedicalCenterRequest

class RequestsSerializer(serializers.ModelSerializer):

    city = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()
    speciality = serializers.SerializerMethodField()
    procedure = serializers.SerializerMethodField()

    class Meta:
        model = MedicalCenterRequest
        fields = [
            'id', 'patient', 'medical_center', 'speciality', 'procedure',
            'country', 'city', 
        ]

    def get_city(self, obj):
        return obj.city.name 
    
    def get_country(self, obj):
        return obj.country.name  
    
    def get_speciality(self, obj):
        return {
            "id" : obj.speciality.id, 
            "name" : obj.speciality.name
            } 
    
    def get_procedure(self, obj):
        return {
            "id" : obj.procedure.id, 
            "name" : obj.procedure.name
            } 