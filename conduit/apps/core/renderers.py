import json

from rest_framework.renderers import JSONRenderer


class ConduitJSONRenderer(JSONRenderer):
    charset = 'utf-8'
    object_label = 'object'

    def render(self, data, media_type=None, renderer_context=None):

        errors = data.get('error', None)

        if errors is not None:
            # As mentioned above, we will let the default JSONRenderer handle
            # rendering errors.
            return super(ConduitJSONRenderer, self).render(data)

        # Finally, we can render our data under the "user" namespace.
        return json.dumps({
            self.object_label: data
        })