from rest_framework import serializers
from .models import *

from django.shortcuts import get_object_or_404


class DoctorSerializer(serializers.ModelSerializer):
    related_center = serializers.PrimaryKeyRelatedField(queryset=MedicalCenter.objects.all())

    class Meta:
        model = Doctor
        fields = '__all__' 


class MedicalCenterPhotosSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalCenterPhotos
        fields = ["image_name", "image", "uploaded_at"]

class MedicalCenterVideosSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalCenterVideos
        fields = ["video_name", "video_link", "uploaded_at"]


class MedicalCenterSpecialitySerializer(serializers.ModelSerializer):
    # procedures = serializers.SerializerMethodField('medical_center_procedures')
    procedures = serializers.SerializerMethodField()
    class Meta:
        model = Speciality
        fields = ['id', 'name', 'code', 'procedures'] 

    def get_procedures(self, obj):
        medcent = self.context.get("medcent")
        return [
                {
                "id": procedure.id, 
                "name": procedure.name,                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
                "code":procedure.code, 
                "speciality":procedure.speciality.id
                } 
                for procedure in medcent.procedures.all() 
                if procedure.speciality.id == obj.id
            ]

class MedicalCenterSpecialityUpdateSerializer(serializers.ModelSerializer):
    specialities = serializers.ListField(
        child=serializers.IntegerField(), required=False
    )
    procedures = serializers.ListField(
        child=serializers.IntegerField(), required=False
    )

    class Meta:
        model = MedicalCenter
        fields = ["specialities", "procedures"]

    def update(self, instance, validated_data):
        # Verilen verilerdeki specialities ve procedures'ı al
        specialities_data = validated_data.pop("specialities", [])
        procedures_data = validated_data.pop("procedures", [])

        # Yeni verileri mevcut ilişkilere ekle
        if specialities_data:
            instance.specialities.add(*specialities_data)  # Mevcut specialities'a ekle

        if procedures_data:
            instance.procedures.add(*procedures_data)  # Mevcut procedures'a ekle

        # Diğer verileri güncelle
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

class MedicalCenterProcedureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Procedure
        fields = '__all__' 

class MedicalCenterSerializer(serializers.ModelSerializer):
    # custom serializer methods
    city = serializers.SerializerMethodField()
    specialities = serializers.SerializerMethodField()
    # procedures = serializers.SerializerMethodField()
    contracted_health_institutions = serializers.SerializerMethodField()

    doctors = DoctorSerializer(many=True, read_only=True)  # related_name="doctors"
    medical_center_photos = MedicalCenterPhotosSerializer(many=True, read_only=True)  # related_name="medical_center_photos"
    medical_center_videos = MedicalCenterVideosSerializer(many=True, read_only=True)  # related_name="medical_center_videos"

    class Meta:
        model = MedicalCenter
        fields = [
            "user",
            "center_name",
            "center_type",
            "city",
            "contact_number",
            "mail_address",
            "web_site",
            "preview_text",
            "overview_text",
            "specialities",                     # Many-to-many ilişkiler
            # "procedures",                       # Many-to-many ilişkiler
            "contracted_health_institutions",   # Many-to-many ilişkiler
            "doctors",                          # One-to-many ilişki
            "medical_center_photos",            # One-to-many ilişki
            "medical_center_videos",            # One-to-many ilişki
        ]
        extra_kwargs = {
            "user": {"read_only": True},
        }
    
    def get_procedures(self, obj, id):
        return [
                {
                "id": procedure.id, 
                "name": procedure.name, 
                "code":procedure.code, 
                "speciality":procedure.speciality.id
                } 
                for procedure in obj.procedures.all() 
                if procedure.speciality.id == id
            ]
    
    def get_specialities(self, obj):
        return [{
            "id": speciality.id, 
            "name": speciality.name, 
            "code":speciality.code,
            "procedures": self.get_procedures(obj=obj, id=speciality.id ),
            } for speciality in obj.specialities.all() ] 

    def get_contracted_health_institutions(self, obj):
        return [{
            "id":inst.id, 
            "name":inst.name, 
            "code": inst.code
            } for inst in obj.contracted_health_institutions.all()]

    def get_city(self, obj):
        return {
            "city_code": obj.city, 
            "city": dict(MedicalCenter.CITY_CHOICES).get(obj.city) 
        }
    
class MedicalCenterUpdateSerializer(serializers.ModelSerializer):
    specialities = serializers.PrimaryKeyRelatedField(
        queryset=Speciality.objects.all(), 
        many=True)
    procedures = serializers.PrimaryKeyRelatedField(
        queryset=Procedure.objects.all(), 
        many=True)
    contracted_health_institutions = serializers.PrimaryKeyRelatedField(
        queryset=HealthInstitutions.objects.all(), many=True)

    class Meta:
        model = MedicalCenter
        fields = [
            "center_name", "center_type", "city", 
            "contact_number", "mail_address", "web_site", 
            "preview_text", "overview_text", 
            "specialities", "procedures", "contracted_health_institutions"
        ]










# from rest_framework import serializers
# from .models import Speciality, Procedure

# class ProcedureSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Procedure
#         fields = ['id', 'name', 'code']  # Gerekli alanları ekleyin

# class SpecialitySerializer(serializers.ModelSerializer):
#     procedures = serializers.SerializerMethodField()

#     class Meta:
#         model = Speciality
#         fields = ['id', 'name', 'code', 'procedures']  # İlişkili prosedürler dahil

#     def get_procedures(self, obj):
#         # İlgili Speciality'ye bağlı Procedures
#         procedures = Procedure.objects.filter(speciality=obj)
#         return ProcedureSerializer(procedures, many=True).data
