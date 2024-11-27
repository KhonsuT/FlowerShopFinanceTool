from django.http import HttpResponse
from django.http import JsonResponse
from .models import Flower, Prices
from .utilities.pdf import generateInvoice
import uuid
import json


def default(req):
    return JsonResponse({"flowers": Flower.objects.all()})


def search(req):
    name = req.GET.get("name")
    flowers = Flower.objects.all()
    if name:
        flowers = flowers.filter(name__icontains=name)
    return JsonResponse({"flowers": flowers})


def invoiceQuery(req):
    ## Map of flowers
    ## key: name of flower, value: quantity
    flowers_map = req.GET.get("flowers")
    if not flowers_map:
        return JsonResponse({"errors":"Missing list of flowers"}, status=400)
    try:
        flowers_map = json.loads(flowers_map)
        invoice = {}
        for name, quantity in enumerate(flowers_map):
            invoice[name] = Prices.objects.filter(name=name).latest() * quantity
        invoice_pdf = generateInvoice(invoice)
        response = HttpResponse(invoice_pdf, content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="invoice.pdf"'
        return response
    except Exception as e:
        return JsonResponse({"error": e}, status=500)


def addPrice(req):
    try:
        name = req.POST.get("name")
        price = req.POST.get("price")

        if not name and not price:
            return JsonResponse({"error": "Name or Price Field Missing"}, status=400)

        Prices.objects.create(name=name, price=price)
        return JsonResponse.status_code("200")
    except Exception as e:
        return JsonResponse({"error": e}, status=500)


def removePrice(req):
    try:
        name = req.DELETE.get("name")
        date = req.DELETE.get("date")
        if not name and not date:
            return JsonResponse({"error": "Name or Price Field Missing"}, status=400)
        Prices.filter(name=name, date=date).delete()
        return JsonResponse.status_code(200)
    except Exception as e:
        return JsonResponse({"error": e}, status=500)


def addFlower(req):
    try:
        name = req.POST.get("name")
        type = req.POST.get("type")
        if not name and not type:
            return JsonResponse({"error": "Name or Price Field Missing"}, status=400)
        Flower.objects.create(id=uuid.uuid4(), name=name, type=type)
        return JsonResponse.status_code(200)
    except Exception as e:
        return JsonResponse({"error": e}, status=500)
