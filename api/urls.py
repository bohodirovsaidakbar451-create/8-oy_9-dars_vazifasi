from rest_framework.routers import DefaultRouter

from .views import GenreViewSet, BookViewSet, CommentViewSet

router = DefaultRouter()
router.register('genres', GenreViewSet, basename='genre')
router.register('books', BookViewSet, basename='book')
router.register('comments', CommentViewSet, basename='comment')

urlpatterns = router.urls
