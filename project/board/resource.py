from import_export import resources

from board.models import Post


class PostResource(resources.ModelResource):
    class Meta:
        model = Post
        fields = ('author', 'title', 'content', 'created_at')
        export_order = fields
