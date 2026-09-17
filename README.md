# EcoShare Tashkent 🫱🏻‍🫲🏽

Aholi o'rtasida keraksiz, lekin ishlatishga yaroqli buyumlarni **bepul** ulashish platformasining MVP versiyasi.

Foydalanuvchilar o'zlariga kerak bo'lmagan buyumlarni (kitob, kiyim-kechak, maishiy texnika va boshqalar) e'lon qilib, boshqalarga bepul berib yuborishlari mumkin.

## Texnologiyalar

| Texnologiya | Maqsad |
|---|---|
| Python 3.11+ / Django 5.x | Backend |
| SQLite | Ma'lumotlar bazasi (dev) |
| Django Templates | Server-side rendering |
| Tailwind CSS (CDN) | Zamonaviy, quyuq (dark) responsiv UI |

## Live demo

🌐 **https://ecoshare-tashkent.onrender.com** — Render (Frankfurt) da joylashgan

## Funktsiyalar

- **Asosiy sahifa (`/`)** — barcha *available* e'lonlar kartochka ko'rinishida; kategoriya bo'yicha filterlash va qidiruv
- **Detail sahifa (`/item/<pk>/`)** — buyum haqida to'liq ma'lumot, rasm, manzil va ega ma'lumotlari; **"Ega bilan bog'lanish"** tugmasi (Telegram / telefon)
- **Yang e'lon (`/item/add/`)** — tizimga kirgan foydalanuvchi ModelForm orqali e'lon qo'shadi
- **Dashboard (`/my-items/`)** — o'z e'lonlarini ko'rish, statusni `taken` ga o'zgartirish, o'chirish
- **Autentifikatsiya** — Register, Login, Logout + shaxsiy profil sahifasi

## Modellar

- **Category** — `name`, `slug`
- **Item** — `title`, `description`, `category`, `owner`, `image`, `location_name`, `contact`, `status` (available/taken), `created_at`

## Ishga tushirish

```bash
# 1. Virtual muhit yaratish
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Linux/macOS

# 2. Bog'liqliklarni o'rnatish
pip install -r requirements.txt

# 3. Migratsiyalar
python manage.py migrate

# 4. Superuser yaratish
python manage.py createsuperuser

# 5. Ishga tushirish
python manage.py runserver
```

Keyin `http://127.0.0.1:8000/` ga o'ting.

## Namuna ma'lumotlar

```bash
python manage.py shell -c "from items.models import Category, Item; from django.contrib.auth.models import User; ..."
```

## Loyiha tuzilmasi

```
EcoShare/
├── manage.py
├── ecoshare/           # Django asosiy sozlamalari
├── apps/
│   ├── items/          # Buyumlar ilovasi (modellar, views, templates)
│   └── accounts/       # Autentifikatsiya ilovasi
├── templates/          # Global template (base.html)
├── static/             # CSS, JS, rasm fayllari
└── media/              # Yuklangan rasm fayllari
```