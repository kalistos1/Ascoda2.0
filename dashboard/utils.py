from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string, get_template




def send_email(receiver, subject, template_name, context, sender):
    msg_html = render_to_string(template_name, context)
    msg = EmailMessage(subject=subject, body=msg_html, from_email=sender, to=receiver)
    msg.content_subtype = "html"  # Main content is now text/html
    return msg.send()

