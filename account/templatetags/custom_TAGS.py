
from django import template
from account.models import User
register = template.Library()



# THE NAME THAT APPEARS WHEN YOU LOG IN
@register.simple_tag(takes_context=True)
def staff_name(context):
    request =  context['request']
    full_name =  request.user.full_name
    title =  request.user.title
    return f"{title} {full_name.title()} "



