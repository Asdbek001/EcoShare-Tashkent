import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from items.models import Category

DEFAULT_CATEGORIES = [
    ("Kitoblar", "kitoblar"),
    ("Kiyim-kechak", "kiyim-kechak"),
    ("Maishiy texnika", "maishiy-texnika"),
    ("Bolalar buyumlari", "bolalar-buyumlari"),
    ("Mebel", "mebel"),
]


class Command(BaseCommand):
    help = "Boshlang'ich kategoriyalar va (sozlanganda) admin foydalanuvchini yaratadi."

    def handle(self, *args, **options):
        for name, slug in DEFAULT_CATEGORIES:
            Category.objects.get_or_create(slug=slug, defaults={"name": name})
        self.stdout.write(
            self.style.SUCCESS(f"Kategoriyalar tayyor: {Category.objects.count()} ta")
        )

        user_model = get_user_model()
        username = os.environ.get("ADMIN_USERNAME", "")
        password = os.environ.get("ADMIN_PASSWORD", "")
        email = os.environ.get("ADMIN_EMAIL", "")

        if username and password:
            admin, created = user_model.objects.get_or_create(
                username=username, defaults={"email": email or ""}
            )
            admin.email = email or admin.email
            admin.is_staff = True
            admin.is_superuser = True
            admin.set_password(password)
            admin.save()
            status = "yaratildi" if created else "yangilandi"
            self.stdout.write(self.style.SUCCESS(f"Admin: {username} ({status})"))
        else:
            self.stdout.write(self.style.WARNING("ADMIN_* env o'zgaruvchilari ko'rsatilmagan, admin o'tkazib yuborildi."))