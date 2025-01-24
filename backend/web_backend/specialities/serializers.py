from rest_framework import serializers
from medical_centers.models import Speciality, Procedure

class ProcedureSerializer(serializers.ModelSerializer):
    """
    ProcedureSerializer is for serializing the retrieve data, and validating or creating data.

    data:
        'id', 'name', 'code', 'speciality'
    return data:
        'id', 'name', 'code'
    """
    class Meta:
        model = Procedure
        fields = ['id', 'name', 'code', 'speciality']  
        extra_kwargs = {
            "speciality": {"write_only": True}
        }
class SpecialitySerializer(serializers.ModelSerializer):

    """
    SpecialitySerializer is for serializing the retrieve data, and validating or creating data.

    data:
        'id', 'name', 'code'
    return data:
        'id', 'name', 'code', procedures
    """

    procedures = serializers.SerializerMethodField()

    class Meta:
        model = Speciality
        fields = ['id', 'name', 'code', 'procedures']  
        extra_kwargs = {
            "procedures": {"read_only": True}
        }

    def get_procedures(self, obj):
        """
            Retrieves Procedures linked to the relevant Speciality
        """
        procedures = Procedure.objects.filter(speciality=obj)
        return ProcedureSerializer(procedures, many=True).data
