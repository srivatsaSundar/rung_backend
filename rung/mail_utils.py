import email
import smtplib
import json
from django.core.mail import send_mail

def send_email(to_email,cc_email, subject, body):
    """Sends an email to the specified recipient using the email library.

    Args:
        to_email: The email address of the recipient.
        subject: The subject line of the email.
        body: The body of the email.
    """
    msg = email.message.EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["To"] = to_email
    msg["Cc"] = cc_email

    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    smtp = smtplib.SMTP(smtp_server, smtp_port)
    smtp.starttls()

    # Replace the following with your Gmail username and password.
    smtp.login("mrrungorders@gmail.com", "augt wgxa pagx vhat")

    smtp.send_message(msg)
    smtp.quit()

    print("Email sent successfully!")

def schedule_order_email(order):
    """Schedules an email to be sent with order details at the specified time.

    Args:
        order: The Order instance for which to send an email.
    """
    # to_email =["yuti-m@hotmail.com", "Y.mahendran@gmail.com"]
    to_email=["vatsasundar0503@gmail.com"]
    cc_email=order.email

    subject = "Order Details from Mr Rung"
    body = ""
    # Construct the email body based on the database information
    body += f"**Order ID:** {order.id}\n\n"
    body += f"Order Details\n\n"
    body += f"Lieferung Bestätigte Uhrzeit {order.delivery_date} {order.delivery_time.strftime('%H:%M')}\n\n"
    body += "Lieferadresse\n"
    body += f"{order.person_name}\n{order.address}\n{order.postal_code} {order.city}\n"
    body += f"Tel. : {order.phone_number}\n\n"

    # Add order items
    body += "Gerichte\n"
    cart_str = order.cart
    cart = json.loads(cart_str)
    print(cart)
    for item in cart:
        item_name = item["item_name"]
        quantity = item["quantity"]
        cost = item["cost"]
        item_line = f"{quantity}x {item_name}\t{cost:.2f} CHF\n"
        body += item_line

    # Add total price
    body += f"\n**Gesamt: {order.total_price} CHF**\n\n"
    # Additional information

    body += f"Order Date: {order.order_date}\n\n"
    body += f"Wichtig:\n\n"
    body += f"Dies ist keine Rechnung"

    send_email(to_email,cc_email, subject, body)
    order.mail_sent = True
    order.save()

def send_contact_email(to_email, subject, body):
    """Sends an email to the specified recipient using the email library.

    Args:
        to_email: The email address of the recipient.
        subject: The subject line of the email.
        body: The body of the email.
    """
    msg = email.message.EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["To"] = to_email

    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    smtp = smtplib.SMTP(smtp_server, smtp_port)
    smtp.starttls()

    # Replace the following with your Gmail username and password.
    smtp.login("mrrungorders@gmail.com", "augt wgxa pagx vhat")

    smtp.send_message(msg)
    smtp.quit()

    print("Email sent successfully!")

def schedule_contact_email(contact):
    """Schedules an email to be sent with contact details of user with message at the specified time.

    Args:
        message: The Message instance for which to send an email.
    """
    to_email =["yuti-m@hotmail.com", "Y.mahendran@gmail.com"]

    subject = "Contact submitted to Mr Rung"
    body = ""
    body += f"Contact Details\n\n"
    body += f"**Name : ** {contact.name}\n\n"
    body += f"**Email : ** {contact.email}\n\n"
    body += f"**Message : ** {contact.message}\n\n"
    body += f"Tel. : {contact.phone_number}\n\n"

    send_contact_email(to_email, subject, body)

