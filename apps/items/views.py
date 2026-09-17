from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _

from .forms import ItemForm
from .models import Category, Item


def item_list(request):
    """Barcha bepul (available) e'lonlarni kategoriya va qidiruv bilan filterlaydi."""
    items = (
        Item.objects.filter(status=Item.Status.AVAILABLE)
        .select_related("owner", "category")
    )

    active_category = request.GET.get("category", "")
    query = request.GET.get("q", "").strip()

    if active_category:
        items = items.filter(category__slug=active_category)

    if query:
        items = items.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(location_name__icontains=query)
        )

    categories = (
        Category.objects.annotate(
            item_count=Count("items", filter=Q(items__status=Item.Status.AVAILABLE))
        )
        .filter(item_count__gt=0)
    )

    context = {
        "items": items,
        "categories": categories,
        "active_category": active_category,
        "query": query,
        "total_count": items.count(),
    }
    return render(request, "items/item_list.html", context)


def item_detail(request, pk):
    item = get_object_or_404(
        Item.objects.select_related("owner", "category"), pk=pk
    )
    related_items = (
        Item.objects.filter(category=item.category, status=Item.Status.AVAILABLE)
        .exclude(pk=item.pk)
        .select_related("owner")[:3]
    )
    context = {"item": item, "related_items": related_items}
    return render(request, "items/item_detail.html", context)


@login_required
def item_create(request):
    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.owner = request.user
            item.save()
            messages.success(request, _("E'lon muvaffaqiyatli joylandi!"))
            return redirect(item.get_absolute_url())
    else:
        form = ItemForm()
    return render(request, "items/item_create.html", {"form": form})


@login_required
def user_dashboard(request):
    items = Item.objects.filter(owner=request.user).select_related("category")
    available_count = items.filter(status=Item.Status.AVAILABLE).count()
    taken_count = items.filter(status=Item.Status.TAKEN).count()
    context = {
        "items": items,
        "available_count": available_count,
        "taken_count": taken_count,
    }
    return render(request, "items/user_dashboard.html", context)


@login_required
def toggle_item_status(request, pk):
    """E'lon egasiga statusni available <-> taken o'zgartirish imkonini beradi."""
    item = get_object_or_404(Item, pk=pk, owner=request.user)
    if request.method == "POST":
        if item.status == Item.Status.AVAILABLE:
            item.status = Item.Status.TAKEN
            messages.success(request, _("«%(title)s» topshirilgan deb belgilandi.") % {"title": item.title})
        else:
            item.status = Item.Status.AVAILABLE
            messages.success(request, _("«%(title)s» yana bepul holatiga qaytarildi.") % {"title": item.title})
        item.save(update_fields=["status"])
    return redirect("items:user_dashboard")


@login_required
def delete_item(request, pk):
    item = get_object_or_404(Item, pk=pk, owner=request.user)
    if request.method == "POST":
        title = item.title
        item.delete()
        messages.success(request, _("«%(title)s» e'loni o'chirildi.") % {"title": title})
    return redirect("items:user_dashboard")