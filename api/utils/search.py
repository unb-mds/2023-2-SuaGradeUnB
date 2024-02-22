from django.contrib.admin import ModelAdmin, site
from django.db.models.query import QuerySet
from django.db.models import Model
from rest_framework.request import Request
from unidecode import unidecode
from typing import Any, Type

class SearchTool:
    """
    Search for models by given model fields and a search string.
    """
    def __init__(self, model: Type[Model]) -> None:
        self.model = model
    
    def filter_by_search_result(self, request: Request, search_str: str, search_fields: list[str]) -> QuerySet[Any]:
        unicode_search_str = unidecode(search_str).casefold()
        model_handler = ModelAdmin(self.model, site)
        model_handler.search_fields = search_fields
        
        values = self.model.objects.all()

        values, _ = model_handler.get_search_results(
            request, values, unicode_search_str)

        return values
    