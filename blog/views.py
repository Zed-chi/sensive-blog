from django.db.models.query import Prefetch
from django.shortcuts import render
from django.db.models import F, Q, Value, Count
from blog.models import Comment, Post, Tag


def serialize_post(post):
    return {
        "title": post.title,
        "teaser_text": post.text[:200],
        "author": post.author.username,
        "comments_amount": post.comments_count,
        "image_url": post.image.url if post.image else None,
        "published_at": post.published_at,
        "slug": post.slug,
        "tags": post.tags.all(),
        "first_tag_title": post.tags.all()[0].title,
    }


def serialize_tag(tag):
    return {
        "title": tag.title,
        "posts_with_tag": tag.posts.count(),
    }


def serialize_tag_optimized(tag):
    return {
        "title": tag.title,
        "posts_with_tag": tag.posts_with_tag,
    }


def index(request):
    posts = Post.objects.prefetch_related(
        "author", Prefetch("tags", queryset=Tag.objects.popular())
    )
    most_popular_posts = posts.popular()[:5].fetch_with_comments_count()
    most_fresh_posts = posts.order_by("-published_at")[
        :5
    ].fetch_with_comments_count()
    most_popular_tags = Tag.objects.popular()[:5]
    context = {
        "most_popular_posts": [
            serialize_post(post) for post in most_popular_posts
        ],
        "page_posts": [serialize_post(post) for post in most_fresh_posts],
        "popular_tags": most_popular_tags,
    }
    return render(request, "index.html", context)


def post_detail(request, slug):
    tags = Tag.objects.popular()
    posts = Post.objects.popular().prefetch_related("comments", "author")
    comments = Comment.objects.prefetch_related("author")
    post = posts.get(slug=slug)
    related_tags = tags.filter(
        posts__in=[
            post,
        ]
    )
    post_comments = comments.filter(post=post)

    serialized_post = {
        "title": post.title,
        "text": post.text,
        "author": post.author.username,
        "comments": post_comments,
        "likes_amount": post.likes_count,
        "image_url": post.image.url if post.image else None,
        "published_at": post.published_at,
        "slug": post.slug,
        "tags": related_tags,
    }

    most_popular_tags = tags.all()[:5]
    most_popular_posts = posts[:5].fetch_with_comments_count()

    context = {
        "post": serialized_post,
        "popular_tags": most_popular_tags,
        "most_popular_posts": most_popular_posts,
    }
    return render(request, "post-details.html", context)


def tag_filter(request, tag_title):
    tags = Tag.objects.popular()
    posts = Post.objects.prefetch_related(
        "author", Prefetch("tags", queryset=tags)
    )
    most_popular_tags = tags[:5]
    tag = tags.get(title=tag_title)
    related_posts = posts.filter(tags__in=(tag.id,))[
        :20
    ].fetch_with_comments_count()
    most_popular_posts = posts.popular()[:5].fetch_with_comments_count()

    context = {
        "tag": tag.title,
        "popular_tags": most_popular_tags,
        "posts": [serialize_post(post) for post in related_posts],
        "most_popular_posts": [
            serialize_post(post) for post in most_popular_posts
        ],
    }
    return render(request, "posts-list.html", context)


def contacts(request):
    # позже здесь будет код для статистики заходов на эту страницу
    # и для записи фидбека
    return render(request, "contacts.html", {})
