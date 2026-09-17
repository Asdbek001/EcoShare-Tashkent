from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Item


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ["title", "description", "category", "image", "location_name", "contact"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": _("Masalan: Foydalanilgan romanlar...")}),
            "description": forms.Textarea(
                attrs={
                    "placeholder": _("Buyumning holati, nega berishga qaror qilganingiz va boshqa ma'lumotlar..."),
                    "rows": 5,
                }
            ),
            "location_name": forms.TextInput(attrs={"placeholder": _("Masalan: Chilonzor, 9-daha")}),
            "contact": forms.TextInput(
                attrs={"placeholder": _("Masalan: @telegram_username yoki +998901234567")}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].empty_label = _("Kategoriya tanlang")
        for name, field in self.fields.items():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs["class"] = (
                    "w-full rounded-xl bg-[#0f0f0f] border border-white/10 px-4 py-3 "
                    "text-white outline-none transition-all duration-300 "
                    "focus:border-emerald-400/60 focus:ring-2 focus:ring-emerald-400/20 [&>option]:bg-[#0f0f0f]"
                )
            else:
                field.widget.attrs.setdefault(
                    "class",
                    "w-full rounded-xl bg-white/5 border border-white/10 px-4 py-3 "
                    "text-white placeholder-white/30 outline-none transition-all duration-300 "
                    "focus:border-emerald-400/60 focus:ring-2 focus:ring-emerald-400/20",
                )