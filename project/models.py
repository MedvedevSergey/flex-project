import json
import os
import unicodedata as ud
import re

from django.db import models
from transliterate import translit

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


def check_unacceptable_symbols(string):
    processed_str = re.match("^[A-Za-z0-9_-]*$", string)
    if processed_str is None:
        raise ValueError("Строка должна содержать только символы кириллицы, латиницы, дефис или нижнее подчеркивание")


def transliteration_and_validation(string):
    new_str = translit(string, 'ru', reversed=True)
    check_unacceptable_symbols(new_str)
    return new_str


with open(os.path.join(os.path.dirname(__file__), "dynamic.json"), "r", encoding="utf-8") as f:
    models_struct = json.loads(f.read())
    for obj in models_struct:
        model_fields = {}
        for field in obj["fields"]:
            attrs = field["attrs"]
            if field["type"] == "foreignkey":
                attrs["on_delete"] = additional_foreignkey_attributes[attrs["on_delete"]]

            field_name = transliteration_and_validation(field["name"])
            model_fields.update({field_name: allowed_type_field[field["type"]](**attrs)})

            model_name = transliteration_and_validation(obj["model"])

        model = type(
            model_name,
            (models.Model,),
            {
                **model_fields,
                "__module__": "project.models",
                '__str__': lambda self: f'{self.id}'
            }
        )
