from django.http import HttpResponse
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_POST
from django.shortcuts import redirect, render
from .models import Flower, Prices
from .utils.pdf import generateInvoice
from django.conf import settings
import uuid
import json

def homePage(req):
    return render(request=req, template_name="index.html",context={"flowers": Flower.objects.all()})

def search(req):
    try:
        flowers = Flower.objects.all()
        flowers_json = []
        name = req.GET.get("name","").strip()   
        print(name)
        if name:
            flowers = flowers.filter(name__icontains=name)       
        for flower in flowers:
            image_url = flower.image.url
            price = (
                Prices.objects.filter(name__name=flower.name)
                .order_by("-date")  # Order by the latest date
                .first()  # Get the first result or None
            )
            price_value = price.price if price else 0
            flowers_json.append({
                "name": flower.name,
                "price": price_value,
                "imageURL": image_url
            })
        return JsonResponse(flowers_json, safe=False)
    except Exception as e:
        return JsonResponse({'error': e})

@csrf_protect
def login_user(req):
    try:
        if req.method == "GET":
            return render(req, 'login.html')
        elif req.method == "POST":
            username = req.POST.get("username")
            password = req.POST.get("password")

            user = authenticate(req,username=username,password=password)

            if user is not None:
                login(req, user=user)
                return redirect('default')
            else:
                return render(req, 'login.html', context={'error': "Invalid Credentials"})
    except Exception as e:
        return JsonResponse({'error': e})

@csrf_protect
@require_POST
def logout_user(req):
    try:
        logout(req)
        return redirect(default)
    except Exception as e:
        return JsonResponse({'error': e})
    
@require_POST
def invoiceQuery(req):
    try:
        data = json.loads(req.body)  # Parse JSON from POST body
        flowers_map = data.get("flowers", {})
        numberOfBouquets = data.get("numberOfBouquets", 1)
        labor_cost = data.get("laborCost", 25)
        material_cost = data.get("materialCost", 5)

        if not flowers_map:
            return JsonResponse({"error": "No flowers specified"}, status=400)

        invoice = {"flowers": {}, "labor": {}, "material": {}}
        for name, quantity in flowers_map.items():
            price_entry = Prices.objects.filter(name__name=name).latest("date")
            invoice["flowers"][name] = {
                "price": price_entry.price,
                "quantity": quantity,
                "subtotal": price_entry.price * quantity,
            }
        invoice["labor"]["numberOfBouquets"] = numberOfBouquets
        invoice["labor"]["cost"] = labor_cost
        invoice["labor"]["subtotal"] = labor_cost * numberOfBouquets

        invoice["material"]["numberOfBouquets"] = numberOfBouquets
        invoice["material"]["cost"] = material_cost
        invoice["material"]["subtotal"] = material_cost * numberOfBouquets

        invoice_pdf = generateInvoice(invoice)
        response = HttpResponse(invoice_pdf, content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="invoice.pdf"'
        return response
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@login_required(login_url='/login/')
def updatePrice(req):
    try:
        name = req.POST.get("flowers")
        price = req.POST.get("flowerPrice")
        if not name and not price:
            return JsonResponse({"error": "Name or Price Field Missing"}, status=400)

        Prices.objects.create(name=Flower.objects.get(name=name), price=price,date=timezone.now())
        return JsonResponse({"message": "Success"})
    except Exception as e:
        return JsonResponse({"error": e}, status=500)

@login_required(login_url='/login/')
def addFlower(req):
    try:
        name = req.POST.get("name")
        type = req.POST.get("type")
        image = req.FILES.get("image")
        price = req.POST.get("flowerPrice")
        if not name or not type:
            return JsonResponse({"error": "Name or Price Field Missing"}, status=400)
        if image is None:
            flower = Flower.objects.create( name=name, type=type)
        else:
            flower = Flower.objects.create(name=name, type=type, image=image)
        if price:
            Prices.objects.create(name=flower, price=price,date=timezone.now())
        return JsonResponse({"message": "New Flower Added"}, status=200)
    except Exception as e:
        return JsonResponse({"error": e}, status=500)
