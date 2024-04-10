from django import template
from django.utils.html import format_html
from markdown import markdown


register = template.Library()


@register.simple_tag
def render(content):
    """Render markdown content as valid html"""
    html_content = markdown(content)
    return format_html(html_content)


help_text = 'Verwende <a target="_blank" href="https://www.markdownguide.org/cheat-sheet/">Markdown</a> zur Formatierung.'
