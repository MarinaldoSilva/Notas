from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

ERROR_404 = "Anotação não localizada."
ERROR_PERMISSION_DENIED = "Você não tem permissão para editar este usuário."
ERROR_CREATE_OR_EMAIL = "Erro ao criar nota ou agendar e-mail."
KEY_ERROR = "error"
USER_LOCALIZATION = "Usuário não localizado"
RESULT_RESPONSE = "result"


def form_email(email_destinatario: str, titulo_nota: str) -> render_to_string:

    subject = "Nova nota cadastrada!"
    msg_txt_pure = f"A nota {titulo_nota} foi criada"
    html_message = render_to_string(
        "email/form_email.html",
        {"user_email": email_destinatario, "titulo_nota": titulo_nota},
    )

    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email_destinatario]

    try:
        send_mail(
            subject,
            msg_txt_pure,
            from_email,
            recipient_list,
            fail_silently=False,
            html_message=html_message,
        )
        print("Enviado com sucesso!")
        print(f"E-mail de criação de nota enviado para {email_destinatario} com título '{titulo_nota}'.")
    except Exception as e:
        print(f"{KEY_ERROR}: Ao enviar e-mail para {email_destinatario}: {e}")
