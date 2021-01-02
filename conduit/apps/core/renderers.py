import json

from rest_framework.renderers import JSONRenderer
from rest_framework.utils.serializer_helpers import ReturnList


class ConduitJSONRenderer(JSONRenderer):
    charset = 'utf-8'
    object_label = 'object'
    object_label_plural = 'objects'

    # When it retrieve all data, JSONRenderer return ReturnList
    # If data is instance of ReturnList -> render it 
    # Then return the rendered data
    # slug -> data is ReturnDict 
    # all -> data is ReturnList
    def render(self, data, media_type=None, renderer_context=None):
        if isinstance(data, ReturnList):
            _data = json.loads(
                super(ConduitJSONRenderer, self).render(data).decode('utf-8')
            )

            return json.dumps({
                self.object_label_plural: _data
            })
        else:
            errors = data.get('error', None)
            if errors is not None:
                # As mentioned above, we will let the default JSONRenderer handle
                # rendering errors.
                return super(ConduitJSONRenderer, self).render(data)

            # Finally, we can render our data under the "user" namespace.
            return json.dumps({
                self.object_label: data
            })

    # json.dumps
    # json -> strings
    # json.loads 
    # string -> json

    # Serialize
    # Python obj -> bytes
    # Deserialize
    # bytes -> Python obj

    # JSONParser
    # JSON -> DRF Dictionary
    # JSONRenderer
    # DRF Dictionary -> JSON 
