from rest_framework import serializers
from .models import Tag

class TagRelatedField(serializers.RelatedField):

    def get_queryset(self):
        print("get_queryset")
        print(Tag.objects.all())
        return Tag.objects.all()

    def to_internal_value(self, data):
        print("to_internal_value data")
        print(data)
        tag, created = Tag.objects.get_or_create(tag=data, slug=data.lower())
        print("to_internal_value tag")
        print(tag)
        print("to_internal_value created")
        print(created)
        

        return tag
    
    # Return Tag Property ?
    def to_representation(self, value):
        print("to_internal_value value.tag")
        print(value.tag)
        return value.tag