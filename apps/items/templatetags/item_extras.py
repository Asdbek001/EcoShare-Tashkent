from django import template
from django.utils.translation import gettext as _

register = template.Library()

_MONTH_IDS = {
    1: "yanvar",
    2: "fevral",
    3: "mart",
    4: "aprel",
    5: "may",
    6: "iyun",
    7: "iyul",
    8: "avgust",
    9: "sentabr",
    10: "oktabr",
    11: "noyabr",
    12: "dekabr",
}


@register.filter
def format_date(value):
    """Sana oy nomini har bir so'rovda faol tilga moslab chiqaradi: '17-sentabr, 2026'."""
    if value is None:
        return ""
    month = _(_MONTH_IDS.get(value.month, value.month))
    return f"{value.day}-{month}, {value.year}"