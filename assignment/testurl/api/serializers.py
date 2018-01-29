from rest_framework import serializers

from testurl.models import Check


class CheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Check
        fields = '__all__'


#         fields = ('name', 'helpline_no')
