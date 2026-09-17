from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.translation import gettext as _

from items.models import Item

from .forms import RegisterForm


def register(request):
    if request.user.is_authenticated:
        return redirect("items:item_list")
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, _("Xush kelibsiz, %(name)s!") % {"name": user.username})
            return redirect("items:item_list")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})


@login_required
def profile(request):
    items = Item.objects.filter(owner=request.user).select_related("category")
    context = {"items": items}
    return render(request, "accounts/profile.html", context)