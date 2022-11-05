from io import BytesIO
from celery.decorators import task
# import weasyprint
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from orders.models import Order
from django.core import mail

@task
def payment_completed(order_id):
    """
    Task to send an e-mail notification when an order is
    successfully created.
    """
    order = Order.objects.get(id=order_id)
    # create invoice e-mail
    subject = f'Buyzu - EE Invoice no. {order.id}'
    message = 'Please, find attached the invoice for your recent purchase.'
    # to = 'rovoda9368@isecv.com'
    to = order.email
    # email = EmailMessage(subject,
    #         message,
    #         settings.EMAIL_HOST_USER,
    #         [to])
#     print(message)
    # generate PDF
    html = render_to_string('orders/pdf.html', {'order': order})
    # pdf = render_to_pdf('orders/pdf.html', {'order': order})
    email = mail.EmailMultiAlternatives(
                subject=subject,
                body=message,
                from_email=settings.EMAIL_HOST_USER,
                to=[to],
                
            )
    email.attach_alternative(html, "text/html")
    # out = BytesIO()
    # stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')]
    # weasyprint.HTML(string=html).write_pdf(out,
    # stylesheets=stylesheets)
    # attach PDF file
    # email.attach(f'order_{order.id}.pdf',
    #             out.getvalue(),
    #             'application/pdf')
    # send e-mail
    email.send()
    # connection = mail.get_connection()
    # connection.send_messages([email])
        