from django import template

register = template.Library()


@register.filter
def format_date(value):
    """Sana: '17-sentabr, 2026' ko'rinishida chiqaradi."""
    months_uz = {
        1: "yanvar", 2: "fevral", 3: "mart", 4: "aprel",
        5: "may", 6: "iyun", 7: "iyul", 8: "avgust",
        9: "sentabr", 10: "oktabr", 11: "noyabr", 12: "dekabr",
    }
    return f"{value.day}-{months_uz[value.month]}, {value.year}"