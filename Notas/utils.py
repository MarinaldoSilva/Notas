from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

def form_email(email_destinatario:str, titulo_nota:str):
    
    subject = f"Nova nota '${titulo_nota}' cadastrada com sucesso!"
    #titulo do email

    msg_txt_pure = f"A nota '${titulo_nota}' foi criada"
    #msg console

    html_message = render_to_string(
        'email/form_email.html',
        {'user_email': email_destinatario, 'titulo_nota': titulo_nota}
    )

    from_email = settings.DEFAULT_FROM_EMAIL
    #email do remetente
    recipient_list = [email_destinatario]
    #lista de distinatários

    try:
        send_mail(
            subject,
            None,
            from_email,
            recipient_list,
            fail_silently=False,
            html_message=html_message,
        )
        print(f"Enviado com sucesso!")
        print(f"E-mail de criação de nota enviado para {email_destinatario} com título '{titulo_nota}'.")
    except Exception as e:
        print(f"ERRO: Ao enviar e-mail para {email_destinatario}: {e}")