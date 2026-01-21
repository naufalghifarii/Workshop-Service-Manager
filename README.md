# 🛠️ Workshop Service Manager – Cloud-Native Application

Sebuah aplikasi web cloud-native sederhana untuk manajemen bengkel kendaraan, dibangun tanpa framework frontend berat dan mengikuti prinsip desain modern: **containerization**, **observabilitas**, dan **pemisahan komponen**.

Dibuat oleh **Naufal Ghifari Hidayat** (2702314460) – Ilmu Komputer, BINUS University  
Mata Kuliah: **Cloud Services**

---

## 🎯 Fitur Utama

- **Manajemen data**: Pelanggan (*Customers*), Kendaraan (*Vehicles*), dan Layanan (*Services*)
- **Frontend ringan**: HTML + CSS + Vanilla JavaScript
- **Backend RESTful API**: Python Flask
- **Database relasional**: PostgreSQL 15
- **Observabilitas real-time**: Prometheus + Grafana + Node Exporter
- **Deployment terpadu**: Docker Compose

---

## 🏗️ Arsitektur Sistem

| Komponen       | Teknologi               | Port Eksternal | Deskripsi |
|----------------|-------------------------|----------------|-----------|
| **Frontend**   | Nginx (Alpine)          | `8085`         | Menyajikan file statis (HTML/CSS/JS) |
| **Backend API**| Python Flask            | `5000`         | Menyediakan endpoint CRUD untuk Customers, Vehicles, Services |
| **Database**   | PostgreSQL 15 (Alpine)  | —              | Data disimpan persisten via Docker Volume `postgres_data` |
| **Monitoring** | Prometheus + Grafana + Node Exporter | `3001` | Visualisasi metrik performa & infrastruktur |

> Semua komponen berjalan dalam jaringan Docker internal bernama `workshop-net`. Hanya port 8085, 5000, dan 3001 yang diekspos ke host.

---

## 🚀 Cara Menjalankan

### ✅ Prasyarat:
- Docker
- Docker Compose
(Pastikan sudah terinstal di sistem Anda)

▶️ Langkah 1: Clone repositori
git clone <url-repositori-anda>
cd workshop-service-manager

▶️ Langkah 2: Jalankan semua layanan di background
docker-compose up -d

▶️ Langkah 3: Akses aplikasi via browser
 • Frontend (UI):        http://localhost:8085
 • Backend API:          http://localhost:5000/api/... 
   (contoh endpoint: /api/customers, /api/vehicles, /api/services)
 • Grafana (Monitoring): http://localhost:3001
     Login: admin / admin

▶️ Langkah 4 (Opsional): Simulasi beban

 --- Skenario Beban Normal (1 RPS) ---
 Jalankan di PowerShell (Windows):
 1..100 | %{
   Invoke-RestMethod -Uri "http://localhost:5000/api/vehicles" -Method Get
   Write-Host "Request $_ sent..."
   Start-Sleep -Seconds 1
 }

 Atau di Bash (Linux/macOS):
for i in {1..100}; do
  curl -s http://localhost:5000/api/vehicles > /dev/null
  echo "Request $i sent..."
  sleep 1
done

 --- Skenario Beban Tinggi (>50 RPS) ---
 Jalankan di PowerShell (Windows) — lakukan di 3 terminal sekaligus:
 1..500 | %{
   $body = @{ name = "Stress Test User"; email = "stress@test.com" } | ConvertTo-Json
   try {
     Invoke-RestMethod -Uri "http://localhost:5000/api/customers" -Method Post -Body $body -ContentType "application/json"
     Invoke-RestMethod -Uri "http://localhost:5000/api/customers" -Method Get
   } catch {
     Write-Host "Error"
   }
 }

 Atau di Bash (Linux/macOS):
for i in {1..500}; do
  curl -s -X POST http://localhost:5000/api/customers \
    -H "Content-Type: application/json" \
    -d '{"name": "Stress Test User", "email": "stress@test.com"}' > /dev/null
  curl -s http://localhost:5000/api/customers > /dev/null
done

 ▶️ Langkah 5: Hentikan semua layanan
docker-compose down

 ⚠️ Catatan: Data PostgreSQL tetap aman karena disimpan di volume 'postgres_data'
