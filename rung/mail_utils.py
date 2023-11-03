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

def format_cart(cart):
    # Initialize the HTML content for the cart
    cart_html = "<h3>Cart Details:</h3>"
    cart_html += "<table border='1'>"
    cart_html += "<tr><th>Item Name</th><th>Quantity</th><th>Cost</th></tr>"

    # Iterate through the items in the cart
    for item in cart:
        cart_html += "<tr>"
        cart_html += f"<td>{item['item_name']}</td>"
        cart_html += f"<td>{item['quantity']}</td>"
        cart_html += f"<td>${item['cost']}</td>"
        cart_html += "</tr>"

    cart_html += "</table>"

    return cart_html

def schedule_order_email(order):
    """Schedules an email to be sent with order details at the specified time.

    Args:
        order: The Order instance for which to send an email.
    """
    to_email = order.email
    subject = "Order Details"
    body = f"Order ID: {order.id}\n"
    body += f"Person Name: {order.person_name}\n"
    body += f"Company Name: {order.company_name}\n"
    body += f"Phone Number: {order.phone_number}\n"
    body += f"Address: {order.address}\n"
    body += f"Postal Code: {order.postal_code}\n"
    body += f"City: {order.city}\n"
    body += f"Coupon Code: {order.coupon_code}\n"
    body += f"Total Price: {order.total_price}\n"
    body += f"Delivery Option: {order.delivery_option}\n"
    body += f"Delivery Date: {order.delivery_date}\n"
    body += f"Delivery Time: {order.delivery_time}\n"
    body += f"Remarks: {order.remarks}\n"
    body += f"Order Date: {order.order_date}\n"
    body += cart_html 

    send_email(to_email, subject, body)
    order.mail_sent = True
    order.save()
