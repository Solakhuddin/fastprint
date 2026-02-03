from django import forms
from .models import Produk

class ProdukForm(forms.ModelForm):
    def clean_harga(self):
            harga = self.cleaned_data.get('harga')
            if harga < 0:
                raise forms.ValidationError("Harga tidak boleh negatif !")
            return harga
    
    class Meta:
        model = Produk
        fields = ['nama_produk', 'harga', 'kategori', 'status']
        widgets = {
            'nama_produk': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan nama produk'}),
            'harga': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'placeholder': 'Masukkan harga produk'}),
            'kategori': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
        