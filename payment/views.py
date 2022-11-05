from django.shortcuts import render

# Create your views here.
import braintree
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from orders.models import Order
from django.contrib.auth.decorators import login_required
from .tasks import payment_completed
from django.views.decorators.csrf import csrf_exempt
# instantiate Braintree payment gateway
gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)


@login_required
def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    total_cost = order.get_total_cost()
    if request.method == 'POST':
        # retrieve nonce
        
        nonce = request.POST.get('payment_method_nonce', None)
        # print("nonce",nonce)
        # create and submit transaction
        result = gateway.transaction.sale({
        'amount': f'{total_cost:.2f}',
        'payment_method_nonce': nonce,
        'options': {
        'submit_for_settlement': True
        }
        })
        order.user = request.user
        if result.is_success:
            # mark the order as paid
            order.paid = True
            
            # store the unique transaction id
            order.braintree_id = result.transaction.id
            order.save()
            # launch asynchronous task
            # print('+++++',order.id)
            payment_completed(order.id)
            # payment_completed.delay(order.id)
            return redirect('payment:done')
        else:
            return redirect('payment:canceled')
    else:
        # generate token
        
        client_token = gateway.client_token.generate()
        return render(request,
            'payment/process.html',{
            'order': order,
            'client_token': client_token
            })


def payment_done(request):
    return render(request, 'payment/done.html')

def payment_canceled(request):
    return render(request, 'payment/done.html')


from django.http import JsonResponse
@csrf_exempt
def get_nonce(request):
    
    nonce = request.GET.get('nonce', None)
    print(nonce)
    data = {
        'u': nonce
    }
    return JsonResponse(data)