from rest_framework import serializers
from App.models import DetailPembuatJanji


class JanjiSerializer (serializers.ModelSerializer):
    class Meta:
        model = DetailPembuatJanji
        fields = '__all__'

class JanjiSerializerUpdate (serializers.ModelSerializer):
    class Meta:
        model = DetailPembuatJanji
        fields = ['perusahaan', 'alamat_perusahaan', 'email_perusahaan', 'nomor_perusahaan',
                  'web_perusahaan', 'meeting', 'alamat_meeting', 'rencana_tanggal', 'waktu_tanggal']


class JanjiSerializerCostumUpdate (serializers.ModelSerializer):
    class Meta:
        model = DetailPembuatJanji
        fields = '__all__'

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
