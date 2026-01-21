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

# 🚗 Workshop Service Manager

Aplikasi manajemen bengkel berbasis microservices dengan monitoring menggunakan Grafana.

---

## 🚀 Cara Menjalankan

### ✅ Prasyarat
- Docker
- Docker Compose  
(Pastikan keduanya sudah terinstal)

---

### ▶️ Langkah 1: Clone Repository
```bash
git clone <url-repositori-anda>
cd workshop-service-manager
```
### ▶️ Langkah 2: Jalankan Semua Layanan
```bash
docker-compose up -d
```
### ▶️ Langkah 3: Akses Aplikasi
- Frontend (UI): http://localhost:8085
- Backend API: http://localhost:5000/api
Contoh endpoint:
- /api/customers
- /api/vehicles
- /api/services
Grafana (Monitoring): http://localhost:3001
Login: admin / admin

