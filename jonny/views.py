from django.shortcuts import render
from .services.fetch_urls import end_to_end_url, refresh_customer, find_customer, get_customer_transactions
from django.http import JsonResponse
import random
# Create your views here.
def index(request):
    return render( request, "jonny.html")


def generate_url(request):
    id =random.randint(100, 200)
    if request.method == "POST":
        # Get the value of the input with name="username"
        req = int(request.POST.get('id') ) 

        if (req > 20 and req < 200): 
            id = int(req)

    app_token, customer_id, link = end_to_end_url(id)
    return render(request, 'bank_connect.html', context={'url':link, 'id': customer_id})


def timed_transaction(request):
    customer_id = request.GET.get('user-id')
    customer_id = '13212489182' #reassigned for testing
    if not customer_id:
        return JsonResponse({"error": "Missing 'user-id' parameter"}, status=400)
    try:
        customer_id = int(customer_id) + 250

    except ValueError:
        return JsonResponse({"error": "'user-id' must be a number"}, status=400)

    # Call your integrated Finicity service
    data = get_customer_transactions(customer_id)
    return render(request, 'transaction_list.html', context={"transactions":data})

def consolidate_customer(request):
    if request.method == "POST":
        # Get the value of the input with name="username"
        req = request.POST.get('selected-id')  # 

        print(request.POST.get('selected-id'))
        if req == None:
            return JsonResponse({'message': f"<div id='#placeholder'>Not Found</div>"})


        res = refresh_customer(req).get("transactions")
        print(res[1])
        return render(request, 'transaction_list.html', context={"transactions":res})