import inspect
from rest_framework.viewsets import ModelViewSet
from django.apps import apps
from project import serializer

app_models = apps.get_app_config('project').get_models()
clsmembers = inspect.getmembers(serializer)

serializers_dict = [d for name, d in clsmembers if name == "serializers"][0]

viewset = {}
for model in app_models:
    viewset.update({
        f"{model.__name__}ViewSet": type(
            f"{model.__name__}ViewSet",
            (ModelViewSet, ),
            {
                "queryset": model.objects.all(),
                "__model_name__": model.__name__,
                "serializer_class": serializers_dict[f"{model.__name__}Serializer"]
             }
        )
        }
    )
