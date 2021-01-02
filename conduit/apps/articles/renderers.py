from conduit.apps.core.renderers import ConduitJSONRenderer

# Override object_label and object_label_plural 
class ArticleJSONRenderer(ConduitJSONRenderer):
    object_label = 'article'
    object_label_plural = 'articles'