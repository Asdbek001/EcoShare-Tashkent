from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(attrs={"placeholder": _("sizning@email.uz")}),
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": _("Foydalanuvchi nomi")}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        field_classes = (
            "w-full rounded-xl bg-white/5 border border-white/10 px-4 py-3 "
            "text-white placeholder-white/30 outline-none transition-all duration-300 "
            "focus:border-emerald-400/60 focus:ring-2 focus:ring-emerald-400/20"
        )
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", field_classes)

    def clean_email(self):
        email = self.cleaned_data.get("email").lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_("Bu email allaqachon ro'yxatdan o'tgan."))
        return email