import json

from rest_framework.renderers import JSONRenderer


class ConduitJSONRenderer(JSONRenderer):
    charset = 'utf-8'
    object_label = 'object'
    pagination_object_label = 'objects'
    pagination_count_label = 'count'

    # When it retrieve all data, JSONRenderer return ReturnList
    # If data is instance of ReturnList -> render it 
    # Then return the rendered data
    # slug -> data is ReturnDict 
    # all -> data is ReturnList
    def render(self, data, media_type=None, renderer_context=None):
        
        if data.get('result', None) is not None:

            return json.dumps({
                self.pagination_object_label:data['result'],
                self.pagination_count_label:data['count']
            })
        elif data.get('error', None) is not None:
            # As mentioned above, we will let the default JSONRenderer handle
            # rendering errors.
            return super(ConduitJSONRenderer, self).render(data)

        else:
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
