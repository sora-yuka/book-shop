from django.core.mail import send_mail

    
def send_confirmation_email(email, code):
    
    # Функция отправляющая сообщение с кодом.
    
    full_link = f"http://localhost:8000/account/activate/{code}"
    send_mail(
        "Активация пользователя",
        f"Вас приветствует книжный магазин 'books-shop.kg', пройдите по этой ссылке {full_link} чтобы подтвердить ваш аккаунт.",
        "sabyrkulov.nurmuhammed@gmail.com",
        [email]
    )