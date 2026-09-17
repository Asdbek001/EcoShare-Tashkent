from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField("Nomi", max_length=100, unique=True)
    slug = models.SlugField("Slug", max_length=120, unique=True)

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Item(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = "available", "Bepul"
        TAKEN = "taken", "Topshirilgan"

    title = models.CharField("Nomi", max_length=200)
    description = models.TextField("Tavsif")
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="items",
        verbose_name="Kategoriya",
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="Egasi",
    )
    image = models.ImageField(
        "Rasm",
        upload_to="items/%Y/%m/%d/",
        blank=True,
        null=True,
        help_text="Ixtiyoriy — rasm qo'shilmagan bo'lsa placeholder ko'rsatiladi.",
    )
    location_name = models.CharField("Manzil", max_length=200)
    contact = models.CharField(
        "Bog'lanish (Telegram / telefon)",
        max_length=255,
        help_text="Masalan: @username yoki +998901234567",
    )
    status = models.CharField(
        "Holat",
        max_length=20,
        choices=Status.choices,
        default=Status.AVAILABLE,
    )
    created_at = models.DateTimeField("Yaratilgan vaqt", auto_now_add=True)

    class Meta:
        verbose_name = "Buyum"
        verbose_name_plural = "Buyumlar"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("items:item_detail", kwargs={"pk": self.pk})

    @property
    def contact_url(self):
        contact = self.contact.strip()
        if contact.startswith(("http://", "https://")):
            return contact
        if contact.startswith("@"):
            return f"https://t.me/{contact.lstrip('@')}"
        if contact.startswith(("+", "998", "9")):
            digits = "".join(ch for ch in contact if ch.isdigit())
            return f"tel:+{digits}"
        return contact

    @property
    def is_available(self):
        return self.status == self.Status.AVAILABLE