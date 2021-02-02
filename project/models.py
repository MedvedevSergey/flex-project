import json
from django.db import models
import os


allowed_type_field = {
    "charfield": models.CharField,
    "foreignkey": models.ForeignKey,
    "integer": models.IntegerField,
    "m2m": models.ManyToManyField
}
additional_foreignkey_attributes = {
    "CASCADE": models.CASCADE,
    "SET_NULL": models.SET_NULL,
}

with open(os.path.join(os.path.dirname(__file__), "dynamic.json"), "r") as f:
    models_struct = json.loads(f.read())
    for obj in models_struct:
        model_fields = {}
        for field in obj["fields"]:
            attrs = field["attrs"]
            if field["type"] == "foreignkey":
                attrs["on_delete"] = additional_foreignkey_attributes[attrs["on_delete"]]
            model_fields.update({field["name"]: allowed_type_field[field["type"]](**attrs)})
        model = type(
            obj["model"],
            (models.Model,),
            {
                **model_fields,
                "__module__": "project.models",
                '__str__': lambda self: f'{self.id}'
            }
        )
