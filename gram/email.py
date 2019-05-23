from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode


def send_activation_email(user, current_site, receiver):
    subject = 'Activate your account'

    message = render_to_string('registration/activate.html', {
        'user':user,
        'domain':current_site.domain,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        # 'token':account_activation_token.make_token(user),
    })

    email = EmailMessage(subject, message, to=[receiver])
    email.send()

def send_welcome_email(name,receiver):
    # Creating message subject and sender
    subject = 'Welcome to the Instagram'
    sender = 'shirley@moringaschool.com'

    #passing in the context vairables
    text_content = render_to_string('email/newsemail.txt',{"name": name})
    html_content = render_to_string('email/newsemail.html',{"name": name})

    msg = EmailMultiAlternatives(subject,text_content,sender,[receiver])
    msg.attach_alternative(html_content,'text/html')
    msg.send()