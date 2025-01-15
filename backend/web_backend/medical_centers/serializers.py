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

class MedicalCenterSerializer(serializers.ModelSerializer):
    # custom serializer methods
    city = serializers.SerializerMethodField()
    specialities = serializers.SerializerMethodField()
    procedures = serializers.SerializerMethodField()
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
            "procedures",                       # Many-to-many ilişkiler
            "contracted_health_institutions",   # Many-to-many ilişkiler
            "doctors",                          # One-to-many ilişki
            "medical_center_photos",            # One-to-many ilişki
            "medical_center_videos",            # One-to-many ilişki
        ]
        extra_kwargs = {
            "user": {"read_only": True},
        }

    def get_specialities(self, obj):
        return [{"id": speciality.id, "name": speciality.name, "code":speciality.code}  for speciality in obj.specialities.all()] 
    
    def get_procedures(self, obj):
        return [{"id": procedure.id, "name": procedure.name, "code":procedure.code, "speciality":procedure.speciality.id} for procedure in obj.procedures.all()]

    def get_contracted_health_institutions(self, obj):
        return [{"id":inst.id, "name":inst.name, "code": inst.code} for inst in obj.contracted_health_institutions.all()]

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
