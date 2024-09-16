from django import template 
import logging  

logger = logging.getLogger(__name__)   

register = template.Library()  

@register.filter  
def add_class(field, css_class):  
    """  
    Adds a CSS class to a form field.  
    Usage: {{ form.field|add_class:"form-control" }}  
    """  
    return field.as_widget(attrs={"class": css_class})  