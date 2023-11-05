import email
import smtplib
from django.core.mail import send_mail
from rung.models import Order

def send_email(to_email, subject, body):
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
    smtp.login("srivatsas0503@gmail.com", "iffw mnvb cfbz fgvh")

    smtp.send_message(msg)
    smtp.quit()

    print("Email sent successfully!")

def schedule_order_email(order_id):
    """Schedules an email to be sent with order details at the specified time.

    Args:
        order_id: The ID of the Order instance for which to send an email.
    """
    try:
        order = Order.objects.get(id=order_id)  # Retrieve the order by ID
    except Order.DoesNotExist:
        # Handle the case where the order with the given ID doesn't exist
        return

    to_email = "vatsasundar0503@gmail.com"
    subject = "Order Details"

    # Construct the email body based on the database information
    body = f"Lieferung Bestätigte Uhrzeit {order.delivery_time}\n\n"
    body += f"{order.person_name}\n{order.address}\n{order.postal_code} {order.city}\n"
    body += f"Tel. :{order.phone_number}\n\n"

    # Assuming that 'cart' is a related field on the Order model, use .all() to retrieve the items
    body += "Suppen\n"
    for item in order.cart.all():
        body += f"{item.quantity}x {item.product.name} {item.total_price} CHF\n"
        if item.customization:
            body += f"- {item.customization}\n"
    body += f"\nGesamt {order.total_price} CHF\n\n"

    # Additional information
    body += f"V{order.order_date}\n\nWichtig:\n\nBestellung ist bezahlt online\n\nPayment Online\n\n"
    body += "Dies ist keine Rechnung"

    send_email(to_email, subject, body)
    order.mail_sent = True
    order.save()
