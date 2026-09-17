from django.urls import path

from . import views

app_name = "items"

urlpatterns = [
    path("", views.item_list, name="item_list"),
    path("item/<int:pk>/", views.item_detail, name="item_detail"),
    path("item/add/", views.item_create, name="item_create"),
    path("item/<int:pk>/toggle-status/", views.toggle_item_status, name="item_toggle_status"),
    path("item/<int:pk>/delete/", views.delete_item, name="item_delete"),
    path("my-items/", views.user_dashboard, name="user_dashboard"),
]