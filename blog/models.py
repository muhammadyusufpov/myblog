from django.db import models

from .markdown_utils import render_post_html, to_plain_text


class Post(models.Model):
    FORMAT_HTML = "html"
    FORMAT_MARKDOWN = "markdown"
    FORMAT_CHOICES = [
        (FORMAT_HTML, "HTML"),
        (FORMAT_MARKDOWN, "Markdown"),
    ]

    category = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    content = models.TextField()
    content_format = models.CharField(
        max_length=10,
        choices=FORMAT_CHOICES,
        default=FORMAT_MARKDOWN,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def rendered_html(self):
        return render_post_html(self.content, self.content_format)

    @property
    def plain_text(self):
        return to_plain_text(self.content, self.content_format)

    @property
    def is_markdown(self):
        return self.content_format == self.FORMAT_MARKDOWN
