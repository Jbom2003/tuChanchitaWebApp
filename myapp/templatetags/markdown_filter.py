from django import template
from django.utils.safestring import mark_safe
import markdown

register = template.Library()

@register.filter(name='markdown')
def markdown_filter(text):
    """Convierte texto Markdown a HTML"""
    if not text:
        return ""
    # Convertir Markdown a HTML
    html = markdown.markdown(text, extensions=['nl2br', 'fenced_code'])
    return mark_safe(html)

