from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .markdown_utils import render_markdown, to_plain_text
from .models import Post


class MarkdownRenderingTests(TestCase):
    def test_renders_headings_emphasis_lists_and_links(self):
        html = render_markdown(
            "# Title\n\nThis is **bold** and *italic*.\n\n- one\n- two\n\n[site](https://example.com)"
        )
        self.assertIn("<h1", html)
        self.assertIn("Title", html)
        self.assertIn("<strong>bold</strong>", html)
        self.assertIn("<em>italic</em>", html)
        self.assertIn("<li>one</li>", html)
        self.assertIn('href="https://example.com"', html)

    def test_renders_fenced_code_and_tables(self):
        html = render_markdown(
            "```python\nprint('hi')\n```\n\n"
            "| col |\n| --- |\n| val |"
        )
        self.assertIn("<pre>", html)
        self.assertIn("print", html)
        self.assertIn("<table>", html)
        self.assertIn("<td>val</td>", html)

    def test_renders_blockquotes_and_images(self):
        html = render_markdown('> quoted\n\n![alt text](/static/images/my_photo.jpg)')
        self.assertIn("<blockquote>", html)
        self.assertIn("<img", html)
        self.assertIn('alt="alt text"', html)

    def test_renders_strikethrough_and_task_lists(self):
        html = render_markdown("~~old~~\n\n- [ ] todo\n- [x] done")
        self.assertIn("<del>old</del>", html)
        self.assertIn('<input type="checkbox" disabled>', html)
        self.assertIn('<input type="checkbox" disabled checked>', html)


class PostContentTests(TestCase):
    def test_new_posts_default_to_markdown(self):
        post = Post.objects.create(category="Tech", title="New", content="# Hello")
        self.assertEqual(post.content_format, Post.FORMAT_MARKDOWN)

    def test_markdown_post_renders_html_on_detail(self):
        post = Post.objects.create(
            category="Tech",
            title="Markdown post",
            content="## Heading\n\nA **bold** word.",
            content_format=Post.FORMAT_MARKDOWN,
        )
        response = self.client.get(reverse("post_detail", args=[post.pk]))
        self.assertContains(response, "<h2")
        self.assertContains(response, "Heading")
        self.assertContains(response, "<strong>bold</strong>")

    def test_html_posts_render_unchanged(self):
        post = Post.objects.create(
            category="Tech",
            title="Legacy post",
            content="<p>Hello <strong>world</strong></p>",
            content_format=Post.FORMAT_HTML,
        )
        response = self.client.get(reverse("post_detail", args=[post.pk]))
        self.assertContains(response, "<p>Hello <strong>world</strong></p>", html=False)

    def test_list_excerpt_strips_markdown_syntax(self):
        Post.objects.create(
            category="Tech",
            title="Excerpt post",
            content="# Hello\n\nSome **text** here.",
            content_format=Post.FORMAT_MARKDOWN,
        )
        response = self.client.get(reverse("blog_list"))
        self.assertContains(response, "text")
        self.assertNotContains(response, "**text**")
        self.assertNotContains(response, "# Hello")

    def test_plain_text_for_html_posts(self):
        text = to_plain_text("<p>Hello <strong>world</strong></p>", Post.FORMAT_HTML)
        self.assertEqual(text, "Hello world")


class PostAuthoringTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_superuser("admin", "admin@example.com", "pass")
        self.client.force_login(self.user)

    def test_create_post_saves_markdown(self):
        response = self.client.post(
            reverse("create_post"),
            {
                "category": "Tech",
                "title": "Fresh article",
                "content": "# Intro\n\nHello **there**.",
            },
        )
        self.assertEqual(response.status_code, 302)
        post = Post.objects.get(title="Fresh article")
        self.assertEqual(post.content_format, Post.FORMAT_MARKDOWN)
        self.assertEqual(post.content, "# Intro\n\nHello **there**.")

    def test_edit_keeps_html_format(self):
        post = Post.objects.create(
            category="Tech",
            title="Old article",
            content="<p>Original</p>",
            content_format=Post.FORMAT_HTML,
        )
        response = self.client.post(
            reverse("edit_post", args=[post.pk]),
            {
                "category": "Tech",
                "title": "Old article",
                "content": "<p>Updated</p>",
            },
        )
        self.assertEqual(response.status_code, 302)
        post.refresh_from_db()
        self.assertEqual(post.content_format, Post.FORMAT_HTML)
        self.assertEqual(post.content, "<p>Updated</p>")

    def test_write_page_loads_markdown_editor(self):
        response = self.client.get(reverse("create_post"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "easymde")
        self.assertContains(response, 'data-editor="markdown"')
        self.assertNotContains(response, "ckeditor")
