from rest_framework import serializers
from .models import Produk, Kategori, Status

class ProdukSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produk
        fields = ['id_produk', 'nama_produk', 'harga', 'kategori', 'status']

    def validate_harga(self, value):
        if value < 0:
            raise serializers.ValidationError("Harga tidak boleh negatif")
        return value