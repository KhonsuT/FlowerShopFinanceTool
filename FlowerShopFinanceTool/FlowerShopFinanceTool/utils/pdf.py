from django.template.loader import render_to_string
from weasyprint import HTML


def generateInvoice(invoice):
    flowers = invoice["flowers"]
    labor = invoice["labor"]
    material = invoice["material"]

    invoice = [
        {
            "index": index,
            "name": key,
            "price": val["price"],
            "quantity": val["quantity"],
            "subtotal": val["price"] * val["quantity"],
        }
        for index, (key, val) in enumerate(flowers.items())
    ]

    grandtotal = (
        sum(
            [
                val["quantity"] * val["price"]
                for index, (key, val) in enumerate(flowers.items())
            ]
        )
        + labor.get("subtotal", 0)
        + material.get("subtotal", 0)
    )

    return HTML(
        string=render_to_string(
            "invoice.html",
            context={
                "labor": labor,
                "material": material,
                "invoice": invoice,
                "grandtotal": grandtotal,
            },
        ),
        base_url="http://127.0.0.1:8000/",
    ).write_pdf()
