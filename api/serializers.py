from rest_framework import serializers
from .models import Genre, Book, Comment

class GenreSerializer(serializers.ModelSerializer):
    books = serializers.StringRelatedField(source="book_set", many=True, read_only=True)
    books_count = serializers.SerializerMethodField()

    class Meta:
        model = Genre
        exclude = ["updated"]
        read_only_fields = ["id", "created"]
        extra_kwargs = {
            "name": {"min_length": 2, "trim_whitespace": True}
        }

    def get_books_count(self, obj):
        return obj.book_set.count()


class GenreBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        exclude = ["updated", "genre"]


class GenreDetailSerializer(serializers.ModelSerializer):
    books = GenreBookSerializer(source="book_set", many=True, read_only=True)
    books_count = serializers.SerializerMethodField()

    class Meta:
        model = Genre
        exclude = ["updated"]
        read_only_fields = ["id", "created"]

    def get_books_count(self, obj):
        return obj.book_set.count()


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        exclude = ["updated"]
        read_only_fields = ["id", "created"]
        extra_kwargs = {
            "price": {"min_value": 0},
            "published_year": {"min_value": 0, "max_value": 2100},
            "description": {"required": False},
            "genre": {"required": True, "allow_null": False}
        }


class BookDetailSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Book
        exclude = ["updated"]

    def get_comments_count(self, obj):
        return obj.comment_set.count()


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.StringRelatedField(source="user", read_only=True)

    class Meta:
        model = Comment
        exclude = ["updated"]
        read_only_fields = ["id", "user", "created"]
        extra_kwargs = {
            "text": {"min_length": 2, "max_length": 1000}
        }
