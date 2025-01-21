from rest_framework import serializers
from patient.models import MedicalCenterRequest
from medical_centers.models import MedicalCenter

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
    


class AdminMedicalCenterSerializer(serializers.ModelSerializer):

    city = serializers.SerializerMethodField()
    specialities = serializers.SerializerMethodField()
    procedures = serializers.SerializerMethodField()

    class Meta:
        model = MedicalCenter
        fields = [
            "center_name", "center_type", 
            "city", 
            "specialities", "procedures"
        ]

    def get_procedures(self, obj):
        return [
                {
                "id": procedure.id, 
                "name": procedure.name, 
                "code":procedure.code, 
                "speciality":procedure.speciality.id
                } 
                for procedure in obj.procedures.all() 
            ]
    
    def get_specialities(self, obj):
        return [{
                "id": speciality.id, 
                "name": speciality.name, 
                "code":speciality.code,
                } for speciality in obj.specialities.all() 
            ] 
    
    def get_city(self, obj):
        return {
            "id" : obj.city.id,
            "city": obj.city.name
        }