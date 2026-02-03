from .forms import ProdukForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Produk
from django.contrib import messages

# Create your views here.
def index(request):
    # produk_list = Produk.objects.filter(status__nama_status__icontains='bisa dijual')
    produk_list = Produk.objects.filter(status_id__exact=1)
    
    context = {
        'produk_list': produk_list
    }
    return render(request, 'manajemen_produk/index.html', context)

def hapus_produk(request, id_produk):
    produk = get_object_or_404(Produk, id_produk=id_produk)
    produk.delete()
    messages.success(request, 'Produk berhasil dihapus!')
    return redirect('index')


def tambah_produk(request):
    if request.method == 'POST':
        form = ProdukForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produk berhasil ditambahkan!')
            return redirect('index')
    else:
        form = ProdukForm()
    
    return render(request, 'manajemen_produk/form_produk.html', {'form': form, 'title': 'Tambah Produk'})

def edit_produk(request, id_produk):
    produk = get_object_or_404(Produk, id_produk=id_produk)
    
    if request.method == 'POST':
        form = ProdukForm(request.POST, instance=produk)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produk berhasil diperbarui!')
            return redirect('index')
    else:
        form = ProdukForm(instance=produk)
    
    return render(request, 'manajemen_produk/form_produk.html', {'form': form, 'title': 'Edit Produk'})