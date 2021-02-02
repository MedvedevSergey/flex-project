import inspect
from django.apps import apps
from project import views
from django.urls import path, include
from rest_framework_nested import routers

app_models = apps.get_app_config('project').get_models()
clsmembers = inspect.getmembers(views)


router = routers.SimpleRouter()
for cls_type, cls_l in clsmembers:
    if cls_type == "viewset":
        for i, cls in cls_l.items():
            router.register(f'{cls.__model_name__.lower()}', cls)


urlpatterns = [
    path("", include(router.urls))
]
