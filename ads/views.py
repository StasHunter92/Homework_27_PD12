import json
from json import JSONDecodeError

from django.core.exceptions import ValidationError
from django.db.models import QuerySet
from django.http import JsonResponse, Http404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView

from ads.models import Ad, Category


# ----------------------------------------------------------------------------------------------------------------------
# Start page (FBV)
def index(request) -> JsonResponse:
    """
    Root view that returns a JSON response indicating success

    :param request: The incoming request object
    :return: JSON "OK" status
    """
    return JsonResponse({"status": "ok"}, status=200)


# ----------------------------------------------------------------------------------------------------------------------
# Ads page (CBV)
@method_decorator(csrf_exempt, name="dispatch")
class AdView(View):
    def get(self, request) -> JsonResponse:
        """
        Handle a GET request to the AdView. Returns a list of all Ad objects in the database as a JSON response

        :param request: The incoming request object
        :return: A JSON response with a list of dictionaries, where each dictionary represents an Ad object
        """
        ads: QuerySet[Ad] = Ad.objects.all()
        response: list[dict] | list = []

        for ad in ads:
            response.append({
                "id": ad.id,
                "name": ad.name,
                "author": ad.author,
                "price": ad.price,
            })

        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False}, status=200)

    def post(self, request) -> JsonResponse:
        """
        Handle a POST request to the AdView. Creates a new Ad object in the database

        :param request: The incoming request object
        :return: A JSON response with a dictionary representing the newly created Ad object
        """
        try:
            ad_data: dict = json.loads(request.body)
            ad: Ad = Ad.objects.create(
                name=ad_data.get("name"),
                author=ad_data.get("author"),
                price=ad_data.get("price"),
                description=ad_data.get("description"),
                address=ad_data.get("address"),
                is_published=ad_data.get("is_published")
            )
        except (JSONDecodeError, ValueError, ValidationError):
            return JsonResponse({"status": "Wrong data"}, status=400)

        response: dict = {
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
    model: Ad = Ad

    def get(self, request, *args, **kwargs) -> JsonResponse:
        """
        Retrieve a single Ad instance

        :param request: The incoming request object
        :return: JSON response with Ad data
        """
        try:
            ad: Ad = self.get_object()
        except Http404:
            return JsonResponse({"error": "Not found"}, status=404)

        response: dict = {
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
    def get(self, request) -> JsonResponse:
        """
        Handle a GET request to the CategoryView.
        Returns a list of all Category objects in the database as a JSON response

        :param request: The incoming request object
        :return: A JSON response with a list of dictionaries, where each dictionary represents a Category object
        """
        categories: QuerySet[Category] = Category.objects.all()
        response: list = []

        for category in categories:
            response.append({
                "id": category.id,
                "name": category.name,
            })

        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False}, status=200)

    def post(self, request) -> JsonResponse:
        """
        Handle a POST request to the CategoryView. Creates a new Category object in the database

        :param request: The incoming request object
        :return: A JSON response with a dictionary representing the newly created Category object
        """
        try:
            category_data: dict = json.loads(request.body)
            category: Category = Category.objects.create(
                name=category_data.get("name")
            )
        except (JSONDecodeError, ValueError, ValidationError):
            return JsonResponse({"status": "Wrong data"}, status=400)

        response: dict = {
            "id": category.id,
            "name": category.name,
        }

        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False}, status=201)


# ----------------------------------------------------------------------------------------------------------------------
# Single category page (CBV)
@method_decorator(csrf_exempt, name="dispatch")
class CategoryDetailView(DetailView):
    model: Category = Category

    def get(self, request, *args, **kwargs) -> JsonResponse:
        """
        Retrieve a single Category instance

        :param request: The incoming request object
        :return: JSON response with Category data
        """
        try:
            category: Category = self.get_object()
        except Http404:
            return JsonResponse({"error": "Not found"}, status=404)

        response: dict = {
            "id": category.id,
            "name": category.name,
        }
        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False}, status=200)
