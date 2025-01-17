from rest_framework import serializers
from medical_centers.models import Speciality, Procedure


class ProcedureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Procedure
        fields = ['id', 'name', 'code']  
class SpecialitySerializer(serializers.ModelSerializer):
    procedures = serializers.SerializerMethodField()

    class Meta:
        model = Speciality
        fields = ['id', 'name', 'code', 'procedures']  

    def get_procedures(self, obj):
        # İlgili Speciality'ye bağlı Procedures
        procedures = Procedure.objects.filter(speciality=obj)
        return ProcedureSerializer(procedures, many=True).data
