from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(_("Nomi"), max_length=100, unique=True)
    slug = models.SlugField(_("Slug"), max_length=120, unique=True)

    class Meta:
        verbose_name = _("Kategoriya")
        verbose_name_plural = _("Kategoriyalar")
        ordering = ["name"]

    def __str__(self):
        return self.name


class Item(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = "available", _("Bepul berilmoqda")
        TAKEN = "taken", _("Topshirilgan")

    title = models.CharField(_("Nomi"), max_length=200)
    description = models.TextField(_("Tavsif"))
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="items",
        verbose_name=_("Kategoriya"),
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name=_("Egasi"),
    )
    image = models.ImageField(
        _("Rasm"),
        upload_to="items/%Y/%m/%d/",
        blank=True,
        null=True,
        help_text=_("Ixtiyoriy — rasm qo'shilmagan bo'lsa placeholder ko'rsatiladi."),
    )
    location_name = models.CharField(_("Manzil"), max_length=200)
    contact = models.CharField(
        _("Bog'lanish (Telegram / telefon)"),
        max_length=255,
        help_text=_("Masalan: @username yoki +998901234567"),
    )
    status = models.CharField(
        _("Holat"),
        max_length=20,
        choices=Status.choices,
        default=Status.AVAILABLE,
    )
    created_at = models.DateTimeField(_("Yaratilgan vaqt"), auto_now_add=True)

    class Meta:
        verbose_name = _("Buyum")
        verbose_name_plural = _("Buyumlar")
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