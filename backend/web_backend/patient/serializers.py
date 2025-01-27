from rest_framework import serializers
from .models import Patient
from .models import MedicalCenterRequest, MedicalCenterRequestFile

class PatientSerializers(serializers.ModelSerializer):
    """
    PatientSerializers can be used for validation, creating, and serializing data.

    data:
        "gender", 
        "birthday", 
        "phone_number", 
        "country", 
        "city"
    return datas:
        "gender", 
        "birthday", 
        "phone_number", 
        "country", 
        "city",
        "created_at"
    """
    country = serializers.StringRelatedField()  
    city = serializers.StringRelatedField()  

    class Meta: 
        model = Patient
        fields = [
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

    """
    Medical Center Request Serializer

    Can be used for only creating MedicalCenterRequest. Do not user for viewing.

    Send ID to the required fields. (patient, medical_center, speciality, procedure, country, city)

    data: 
        'id', 'patient', 'medical_center', 'speciality', 'procedure',
        'name', 'surname', 'gender', 'birthday', 'phone', 'email',
        'country', 'city', 
        'disease_history', 'previous_disease', 'previous_surgery',
        'previous_treatment', 'other_comments', 
        
        later 'files' will be added
    """
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
    

class MedicalCenterRequestViewSerializer(serializers.ModelSerializer):
    """
    Medical Center Request Serializer

    Can be used for only viewing MedicalCenterRequest. Just use for serialize the retrieved data.

    return data: 
        'id', 'patient', 'medical_center', 'speciality', 'procedure',
            'name', 'surname', 'gender', 'birthday', 'phone', 'email',
            'country', 'city', 
            'disease_history', 'previous_disease', 'previous_surgery',
            'previous_treatment', 'other_comments', 
            'created_at',
        
        later 'files' will be added
    """

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