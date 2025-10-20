from django.test import TestCase

import django.db
import pytest

from .models import User, Tag, Post, PostComment, PostLike

@pytest.mark.django_db
class FooTest(TestCase):
    def test_posting(self):
        bob = User.objects.create(email="bob@blog.hexlet.io")
        alice = User.objects.create(email="alice@blog.hexlet.io")
        assert User.objects.count() == 2

        bobs_intro = Post.objects.create(
        title="Hello, World!",
        body="Hi there, I'm Bob!",
        creator=bob,
        )
        assert Post.objects.count() == 1

        intro = Tag.objects.create(title="Introduction")
        bobs_intro.tags.add(intro)
        
        assert intro.post_set.count() == 1
        
        hello_from_alice = PostComment.objects.create(
        body="Hi, Bob!",
        creator=alice,
        post=bobs_intro,
        )
        
        bobs_response = PostComment.objects.create(
        body="Nice to meet you, Alice!",
        creator=bob,
        post=bobs_intro,
        response_to=hello_from_alice,
        )
        
        assert bobs_intro.postcomment_set.count() == 2
        assert bobs_response.response_to.post_id == bobs_response.post_id
        PostLike.objects.create(
        post=bobs_intro,
        creator=alice,
        )
        with django.db.transaction.atomic():
        # each post can be liked by particular user only once
            with pytest.raises(django.db.utils.IntegrityError):
                PostLike.objects.create(
                post=bobs_intro,
                creator=alice,
                )
        assert bobs_intro.postlike_set.count() == 1

    