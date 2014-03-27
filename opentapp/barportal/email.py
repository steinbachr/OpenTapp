from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from barwatch import helpers as h

class DrinkUpEmail():
    def __init__(self, tpl_file, subject, to_emails, context={}):
        self.tpl_file = tpl_file
        self.subject = subject
        self.to_emails = to_emails
        self.from_email = h.parse_config_file().get('app_email')
        self.context = context
            
    def send(self):
        rendered_html = render_to_string('emails/html/%s.html' % self.tpl_file, self.context)
        rendered_text = render_to_string('emails/text/%s.txt' % self.tpl_file, self.context)
        
        message = EmailMultiAlternatives(self.subject, rendered_text, self.from_email, self.to_emails)
        message.attach_alternative(rendered_html, "text/html")
        message.send()                
        
