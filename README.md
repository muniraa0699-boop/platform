# 🗑️ Chiqindi Platform — O'zbekiston Chiqindi Muammolari Tizimi

Fuqarolar chiqindi joylarini xaritada belgilab hokimiyatga yuborishi, hokimiyat esa xabarlarni ko'rib chiqib holat yangilashi mumkin bo'lgan to'liq Django tizimi.

## 🚀 O'rnatish va ishga tushirish

### 1. Python virtualenv yaratish
```bash
python -m venv venv

# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate
```

### 2. Kutubxonalarni o'rnatish
```bash
pip install -r requirements.txt
```

### 3. Ma'lumotlar bazasini yaratish
```bash
python manage.py migrate
```

### 4. Test ma'lumotlarini yuklash
```bash
python manage.py seed_data
```

### 5. Serverni ishga tushirish
```bash
python manage.py runserver
```

Brauzerda ochish: **http://127.0.0.1:8000**

---

## 👤 Login ma'lumotlari (test)

| Foydalanuvchi | Parol | Rol |
|---|---|---|
| `admin` | `admin123` | Superuser |
| `fuqaro1` | `fuqaro123` | Fuqaro |
| `fuqaro2` | `fuqaro123` | Fuqaro |
| `hokimiyat1` | `hokimiyat123` | Hokimiyat xodimi |
| `hokimiyat2` | `hokimiyat123` | Hokimiyat xodimi |

Admin panel: **http://127.0.0.1:8000/admin/**

---

## 📋 Sahifalar

| URL | Tavsif |
|---|---|
| `/` | Bosh sahifa – xarita va statistika |
| `/report/create/` | Yangi chiqindi xabari yuborish |
| `/my-reports/` | Mening xabarlarim |
| `/authority/` | Hokimiyat boshqaruv paneli |
| `/authority/export/` | CSV eksport |
| `/notifications/` | Bildirishnomalar |
| `/statistics/` | Statistika va grafiklar |
| `/profile/` | Profil |

---

## 🗺️ Xususiyatlar

- **Interaktiv xarita** (Leaflet.js + OpenStreetMap, API kalitsiz)
- **Rangli markerlar**: Qizil (kutilmoqda), Sariq (jarayonda), Yashil (tozalandi)
- **Ikki rol**: Fuqaro va Hokimiyat xodimi
- **Avtomatik bildirishnomalar** sayt ichida
- **Email bildirishnomalar** (konsolga chiqadi)
- **CSV eksport** hokimiyat uchun
- **Viloyat/Tuman bo'yicha filtrlash**
- **Statistika grafiklar** (Chart.js)
- **Rasm yuklash** imkoniyati
- **Bootstrap 5** responsive dizayn

---

## 🔧 Texnik tafsilotlar

- **Backend**: Django 4.2
- **Ma'lumotlar bazasi**: SQLite (mahalliy)
- **Xarita**: Leaflet.js + OpenStreetMap (bepul, API kerak emas)
- **Frontend**: Bootstrap 5 + Chart.js
- **Email**: Django Console Backend (real SMTP talab qilinmaydi)
