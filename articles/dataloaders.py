from articles.models import Article, FavoriteArticles
from django.db.models import Count, Exists, OuterRef
from promise.dataloader import DataLoader, Promise
from users.models import User


class ArticleFavoriteDataLoader(DataLoader):
    def batch_load_fn(self, article_users: list[tuple[User, Article]]):
        """preload article favorites to avoid N+1 problem"""
        user, _ = article_users[0]
        article_ids = [article.id for _, article in article_users]
        favorites = (
            Article.objects.filter(id__in=article_ids)
            .annotate(
                favorited=Exists(
                    FavoriteArticles.objects.filter(
                        user=user, article_id=OuterRef("pk")
                    )
                ),
                favorites_count=Count(
                    "favorites",
                ),
            )
            .values("favorited", "favorites_count")
        )
        return Promise.resolve(favorites)
