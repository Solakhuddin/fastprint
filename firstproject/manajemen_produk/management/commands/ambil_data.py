from django.core.management.base import BaseCommand
import requests, hashlib
from datetime import datetime
from manajemen_produk.models import Produk, Kategori, Status
from manajemen_produk.serializers import ProdukSerializer

class Command(BaseCommand):
    help = 'Mengambil dan menyimpan data dari API FastPrint'

    def handle(self, *args, **kwargs):
        now = datetime.now()
        day = now.strftime("%d")
        month = now.strftime("%m")
        year = now.strftime("%y")
        
        username = f"tesprogrammer{day}{month}{year}C13"
        raw_password = f"bisacoding-{day}-{month}-{year}"
        password_md5 = hashlib.md5(raw_password.encode()).hexdigest()

        url = "https://recruitment.fastprint.co.id/tes/api_tes_programmer"
        payload = {'username': username, 'password': password_md5}

        self.stdout.write("Menghubungi API...")
        
        try:
            response = requests.post(url, data=payload)
            if response.status_code != 200:
                self.stdout.write(self.style.ERROR(f"Gagal koneksi: {response.status_code}"))
                return

            json_data = response.json()
            
            data_list = json_data.get('data', []) 
            
            if not data_list: 
                self.stdout.write(self.style.WARNING("Tidak ada data ditemukan atau format JSON berbeda."))
                print(json_data) # Debugging: lihat isi mentahnya
                return

            self.stdout.write(f"Menerima {len(data_list)} data. Mulai proses penyimpanan...")

            sukses_count = 0
            
            for item in data_list:
                kat_obj, _ = Kategori.objects.get_or_create(
                    nama_kategori=item.get('kategori', 'Tanpa Kategori')
                )
                
                stat_obj, _ = Status.objects.get_or_create(
                    nama_status=item.get('status', 'Tanpa Status')
                )

                try:
                    harga_parse = int(item.get('harga', 0))
                except:
                    harga_parse = 0

                produk_data = {
                    'id_produk': item.get('id_produk'),
                    'nama_produk': item.get('nama_produk'),
                    'harga': harga_parse,
                    'kategori': kat_obj.id_kategori, 
                    'status': stat_obj.id_status     
                }

                try:
                    produk_exist = Produk.objects.get(id_produk=produk_data['id_produk'])
                    serializer = ProdukSerializer(produk_exist, data=produk_data)
                except Produk.DoesNotExist:
                    serializer = ProdukSerializer(data=produk_data)

                if serializer.is_valid():
                    serializer.save()
                    sukses_count += 1
                else:
                    self.stdout.write(self.style.ERROR(f"Gagal simpan {item.get('nama_produk')}: {serializer.errors}"))

            self.stdout.write(self.style.SUCCESS(f"Selesai! Berhasil menyimpan {sukses_count} produk."))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error Script: {e}"))
