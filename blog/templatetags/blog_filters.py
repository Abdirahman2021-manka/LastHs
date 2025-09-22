from django import template
from django.utils.safestring import mark_safe
import re

register = template.Library()

@register.filter
def format_paragraphs(value):
    """
    Convert line breaks to proper HTML paragraphs.
    This filter handles both plain text and HTML content from CKEditor.
    """
    if not value:
        return value
    
    # If content already contains HTML tags, return as is
    if '<' in str(value) and '>' in str(value):
        return mark_safe(value)
    
    # Convert plain text with line breaks to HTML paragraphs
    # Split by double line breaks (paragraph breaks)
    paragraphs = re.split(r'\n\s*\n', str(value))
    
    # Process each paragraph
    formatted_paragraphs = []
    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if paragraph:
            # Convert single line breaks within paragraphs to <br> tags
            paragraph = paragraph.replace('\n', '<br>')
            formatted_paragraphs.append(f'<p>{paragraph}</p>')
    
    return mark_safe('\n'.join(formatted_paragraphs))

@register.filter
def linebreaks_to_br(value):
    """
    Convert line breaks to <br> tags while preserving existing HTML.
    """
    if not value:
        return value
    
    # If content already contains HTML tags, just convert line breaks to <br>
    if '<' in str(value) and '>' in str(value):
        # Convert line breaks to <br> tags, but be careful not to break existing HTML
        lines = str(value).split('\n')
        result = []
        for line in lines:
            line = line.strip()
            if line:
                result.append(line)
        return mark_safe('<br>'.join(result))
    
    # For plain text, convert line breaks to <br> tags
    return mark_safe(str(value).replace('\n', '<br>'))
