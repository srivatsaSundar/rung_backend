import email
import smtplib
from django.core.mail import send_mail

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

def schedule_order_email(order):
    """Schedules an email to be sent with order details at the specified time.

    Args:
        order: The Order instance for which to send an email.
    """
    to_email = "Y.mahendran@gmail.com"
    subject = "Order Details"
    # body = ""
    # Construct the email body based on the database information
    body = f"**Order ID:** {order.id}\n\n"
    body += f"**Order Details**\n\n"
    body += f"**Lieferung Bestätigte Uhrzeit** {order.delivery_time}\n\n"
    body += f"{order.person_name}\n{order.address}\n{order.postal_code} {order.city}\n"
    body += f"Tel. : {order.phone_number}\n\n"

    # Add order items
    body += "**Gerichte**\n"
    # for item in order.cart:
    #     item_name = item["item_name"]
    #     quantity = item["quantity"]
    #     cost = item["cost"]
    #     body += f"Item Name: {item_name}, Quantity: {quantity}, Cost: {cost}\n"

    body += f"**Cart:** {order.cart}\n"
    body += f"\n**Gesamt {order.total_price} CHF**\n\n"
    
    # Assuming 'order.cart' is a list or queryset of items
    # for item in order.cart:
    #     print(item.item_name)
    #     body += f"{item.quantity}x {item.item_name} {item.cost} CHF\n"
    #     if item.customization:
    #         body += f"- {item.customization}\n"
    # Additional information

    body += f"**Order Date:** {order.order_date}\n\n"
    body += f"**Wichtig:**\n\n"
    body += f"Dies ist keine Rechnung"

    send_email(to_email, subject, body)
    order.mail_sent = True
    order.save()