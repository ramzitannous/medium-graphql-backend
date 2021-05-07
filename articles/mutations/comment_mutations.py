from articles.models import Article, Comment
from articles.types import (CommentCreateInputType, CommentDeleteInputType,
                            CommentNode)
from core.mutations import AppResolverInfo, BaseMutation
from graphene import Field, ObjectType
from graphql import GraphQLError
from graphql_jwt.decorators import login_required
from graphql_relay import from_global_id

####################################
#    Comments Mutations
####################################


class CreateCommentMutation(BaseMutation):
    comment = Field(CommentNode)

    Input = CommentCreateInputType

    @classmethod
    @login_required
    def mutate_and_get_payload(
        cls, root, info: AppResolverInfo, article_slug: str, body: str
    ) -> "CreateCommentMutation":
        article = Article.objects.get(slug=article_slug)
        comment = Comment(body=body, author=info.context.user, article=article)
        comment.save()
        article.comments.add(comment)
        return CreateCommentMutation(comment=comment, success=True)


class DeleteCommentMutation(BaseMutation):
    Input = CommentDeleteInputType

    @classmethod
    @login_required
    def mutate_and_get_payload(
        cls, root, info: AppResolverInfo, comment_id: str
    ) -> "DeleteCommentMutation":
        _, comment_id = from_global_id(comment_id)
        comment = Comment.objects.select_related("author").get(id=comment_id)
        if not comment.author == info.context.user:
            raise GraphQLError("only the comment author can delete it")
        comment.delete()
        return DeleteCommentMutation(success=True)


class CommentsMutations(ObjectType):
    add_comment = CreateCommentMutation.Field(
        description="add a new comment to an article"
    )
    delete_comment = DeleteCommentMutation.Field(
        description="delete a comment by its id"
    )
