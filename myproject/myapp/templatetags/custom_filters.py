from django import template

# Create an instance of Library to register custom filters
register = template.Library()

@register.filter
def percentage_format(value):
    try:
        return f"{float(value):.2f}%"  # Format to 2 decimal places and append '%'
    except (ValueError, TypeError):
        return "N/A"  # Default value if input is invalid