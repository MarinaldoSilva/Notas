from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

def form_email(user_email:str, titulo_nota:str):
    subject = f"Nova nota '${titulo_nota}' cadastrada com sucesso!"

    html_message = render_to_string(
        'email/form_email.html',
        {'user_email': user_email, 'titulo_nota': titulo_nota}
    )
    plain_message = f"A nota ${titulo_nota} foi criada"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]

    try:
        send_mail(
            subject,
            plain_message,
            from_email,
            recipient_list,
            fail_silently=False,
            html_message=html_message,
        )
        print(f"Enviado com sucesso!")
    except Exception as e:
        print(f"ERRO: Ao enviar e-mail para {user_email}: {e}")