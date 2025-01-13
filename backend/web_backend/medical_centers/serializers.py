from rest_framework import serializers
from .models import *

from django.shortcuts import get_object_or_404


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ["name", "surname", "title", "major", "minor"]

class MedicalCenterPhotosSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalCenterPhotos
        fields = ["image_name", "image", "uploaded_at"]

class MedicalCenterVideosSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalCenterVideos
        fields = ["video_name", "video_link", "uploaded_at"]

class MedicalCenterSerializer(serializers.ModelSerializer):
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
        return [speciality.name for speciality in obj.specialities.all()]

    def get_procedures(self, obj):
        return [procedure.name for procedure in obj.procedures.all()]

    def get_contracted_health_institutions(self, obj):
        return [inst.name for inst in obj.contracted_health_institutions.all()]


# class MedicalCenterUpdateSerializer(serializers.ModelSerializer):
#     specialities = serializers.ListField(
#         child=serializers.IntegerField(), required=False
#     )
#     procedures = serializers.ListField(
#         child=serializers.IntegerField(), required=False
#     )
#     contracted_health_institutions = serializers.ListField(
#         child=serializers.IntegerField(), required=False
#     )

#     class Meta:
#         model = MedicalCenter
#         fields = [
#             "center_name", "center_type", "city", 
#             "contact_number", "mail_address", "web_site", 
#             "preview_text", "overview_text", 
#             "specialities", "procedures", "contracted_health_institutions"
#         ]
#         extra_kwargs = {
#             "specialities": {"required": False}, 
#             "procedures": {"required": False}, 
#             "contracted_health_institutions": {"required": False}
#         }

#     def update(self, instance, validated_data):
#         specialities_data = validated_data.pop("specialities", None)
#         procedures_data = validated_data.pop("procedures", None)
#         health_institutions_data = validated_data.pop("contracted_health_institutions", None)

#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)
        
#         if specialities_data is not None:
#             specialities = Speciality.objects.filter(id__in=specialities_data).get()
#             instance.specialities.set(specialities)
#             print("specialities done")

#         if procedures_data is not None:
#             procedures = Procedure.objects.filter(id__in=procedures_data).get()
#             instance.procedures.set(procedures)
#             print("procedures done")

#         if health_institutions_data is not None:
#             health_institutions = HealthInstitutions.objects.filter(id__in=health_institutions_data).get()
#             instance.contracted_health_institutions.set(health_institutions)
#             print("sigorta done")

#         instance.save()
#         print(instance)
#         return instance


class MedicalCenterUpdateSerializer(serializers.ModelSerializer):
    specialities = serializers.PrimaryKeyRelatedField(queryset=Speciality.objects.all(), many=True)
    procedures = serializers.PrimaryKeyRelatedField(queryset=Procedure.objects.all(), many=True)
    contracted_health_institutions = serializers.PrimaryKeyRelatedField(queryset=HealthInstitutions.objects.all(), many=True)

    class Meta:
        model = MedicalCenter
        fields = [
            "center_name", "center_type", "city", 
            "contact_number", "mail_address", "web_site", 
            "preview_text", "overview_text", 
            "specialities", "procedures", "contracted_health_institutions"
        ]
