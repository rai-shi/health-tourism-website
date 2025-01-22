from rest_framework import serializers
from .models import Patient
from .models import MedicalCenterRequest, MedicalCenterRequestFile
import time

class PatientSerializers(serializers.ModelSerializer):
    # return field with their __str__ return 
    country = serializers.StringRelatedField()  
    city = serializers.StringRelatedField()  

    class Meta: 
        model = Patient
        fields = [
                  "id",     # Primary Key 
                  "user",   # Relation to user model
                  "gender", 
                  "birthday", 
                  "phone_number", 
                  "country", 
                  "city",
                  "created_at"
                ]
        extra_kwargs = {
            "created_at": {"read_only": True},  # read-only
        }
    

class MedicalCenterRequestFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalCenterRequestFile
        fields = ['id', 'file']

class MedicalCenterRequestSerializer(serializers.ModelSerializer):
    # files = MedicalCenterRequestFileSerializer(many=True, required=False)
    # city = serializers.SerializerMethodField()
    # country = serializers.SerializerMethodField()
    # speciality = serializers.SerializerMethodField()
    # procedure = serializers.SerializerMethodField()

    class Meta:
        model = MedicalCenterRequest
        fields = [
            'id', 'patient', 'medical_center', 'speciality', 'procedure',
            'name', 'surname', 'gender', 'birthday', 'phone', 'email',
            'country', 'city', 
            'disease_history', 'previous_disease', 'previous_surgery',
            'previous_treatment', 'other_comments', 
            # 'files'
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
    


class MedicalCenterRequestViewSerializer(serializers.ModelSerializer):
    # files = MedicalCenterRequestFileSerializer(many=True, required=False)
    city = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()
    speciality = serializers.SerializerMethodField()
    procedure = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = MedicalCenterRequest
        fields = [
            'id', 'patient', 'medical_center', 'speciality', 'procedure',
            'name', 'surname', 'gender', 'birthday', 'phone', 'email',
            'country', 'city', 
            'disease_history', 'previous_disease', 'previous_surgery',
            'previous_treatment', 'other_comments', 
            'created_at',   
            # 'files'
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
    def get_created_at(self, obj):
        format = "%m/%d/%Y, %H:%M:%S"
        time_obj = obj.created_at
        return time_obj.strftime(format)