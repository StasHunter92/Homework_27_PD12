import json

from django.http import JsonResponse, Http404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView

from ads.models import Ad, Category


# ----------------------------------------------------------------------------------------------------------------------
# Start page (FBV)
def index(request):
    return JsonResponse({"status": "ok"}, status=200)


# ----------------------------------------------------------------------------------------------------------------------
# Ads page (CBV)
@method_decorator(csrf_exempt, name="dispatch")
class AdView(View):
    def get(self, request):
        ads = Ad.objects.all()
        response = []

        for ad in ads:
            response.append({
                "id": ad.id,
                "name": ad.name,
                "author": ad.author,
                "price": ad.price,
            })

        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False}, status=200)

    def post(self, request):
        ad_data = json.loads(request.body)

        ad = Ad.objects.create(
            name=ad_data.get("name"),
            author=ad_data.get("author"),
            price=ad_data.get("price"),
            description=ad_data.get("description"),
            address=ad_data.get("address"),
            is_published=ad_data.get("is_published")
        )

        response = {
            "id": ad.id,
            "name": ad.name,
            "author": ad.author,
            "price": ad.price,
            "description": ad.description,
            "address": ad.address,
            "is_published": ad.is_published,
        }

        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False}, status=201)


# ----------------------------------------------------------------------------------------------------------------------
# Single ad page (CBV)
@method_decorator(csrf_exempt, name="dispatch")
class AdDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs):
        try:
            ad = self.get_object()
        except Http404:
            return JsonResponse({"error": "Not found"}, status=404)

        response = {
            "id": ad.id,
            "name": ad.name,
            "author": ad.author,
            "price": ad.price,
            "description": ad.description,
            "address": ad.address,
            "is_published": ad.is_published,
        }
        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False}, status=200)


# ----------------------------------------------------------------------------------------------------------------------
# Categories page (CBV)
@method_decorator(csrf_exempt, name="dispatch")
class CategoryView(View):
    def get(self, request):
        categories = Category.objects.all()
        response = []

        for category in categories:
            response.append({
                "id": category.id,
                "name": category.name,
            })

        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False}, status=200)

    def post(self, request):
        category_data = json.loads(request.body)

        category = Category.objects.create(
            name=category_data.get("name")
        )

        response = {
            "id": category.id,
            "name": category.name,
        }

        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False}, status=201)


# ----------------------------------------------------------------------------------------------------------------------
# Single category page (CBV)
@method_decorator(csrf_exempt, name="dispatch")
class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        try:
            category = self.get_object()
        except Http404:
            return JsonResponse({"error": "Not found"}, status=404)

        response = {
            "id": category.id,
            "name": category.name,
        }
        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False}, status=200)
