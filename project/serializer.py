from django.apps import apps
from rest_framework.serializers import ModelSerializer

app_models = apps.get_app_config('project').get_models()

serializers = {}
for app_model in app_models:
    class Meta:
        model = app_model
        fields = '__all__'

    attrs = {'__module__': app_model.__module__, 'Meta': Meta}
    serializer_name = f"{app_model.__name__}Serializer"
    serializers.update({
        serializer_name: type(
            serializer_name,
            (ModelSerializer, ),
            attrs
        )
    })

