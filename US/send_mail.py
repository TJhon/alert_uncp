import smtplib, os
from dotenv import load_dotenv

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

load_dotenv()


APP_PASSWORD = os.environ.get("APP_PASSWORD")
sender = os.environ.get("MAIL_SENDER")
receiver = os.environ.get("MAIL_RECEIVER")


def send_content(content):

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender, APP_PASSWORD)
    server.sendmail(sender, receiver, content)


def send_email(
    content,
    subject,
    sender_email=sender,
    sender_name="Jhon Kevin - Bot",
    receiver_email=receiver,
    app_password=APP_PASSWORD,
):
    # Configurar el mensaje
    msg = MIMEMultipart()
    msg["From"] = f"{sender_name} <{sender_email}>"
    msg["To"] = receiver_email
    msg["Subject"] = subject

    # Agregar el contenido del correo
    msg.attach(MIMEText(content, "plain"))

    # Configurar el servidor SMTP
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, app_password)

    # Enviar el correo electrónico
    server.sendmail(sender_email, receiver_email, msg.as_string())

    # Cerrar la conexión SMTP
    server.quit()


Header = "Contenido encontrado"


def pretty_content(content, url, page, relation, faculty):

    return f"""
    Econtrado: {content}
    URL: {url}
    Pagina: {page}
    Relación: {relation}
    Facultad: {faculty}
    """


print(APP_PASSWORD)
print(sender)
print(receiver)
# def join_content()
