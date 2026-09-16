import re

import markdown
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from markdown.extensions import Extension
from markdown.inlinepatterns import SimpleTagInlineProcessor

TASK_ITEM_RE = re.compile(r"<li>\s*\[( |x|X)\]\s+")


class StrikethroughExtension(Extension):
    def extendMarkdown(self, md):
        md.inlinePatterns.register(
            SimpleTagInlineProcessor(r"()~~(.+?)~~", "del"),
            "strikethrough",
            175,
        )


def _apply_task_lists(html):
    def replace(match):
        checked = " checked" if match.group(1).lower() == "x" else ""
        return f'<li><input type="checkbox" disabled{checked}> '

    return TASK_ITEM_RE.sub(replace, html)


def render_markdown(text):
    if not text:
        return ""
    html = markdown.markdown(
        text,
        extensions=[
            "extra",
            "nl2br",
            "sane_lists",
            "smarty",
            "toc",
            StrikethroughExtension(),
        ],
        output_format="html5",
    )
    return _apply_task_lists(html)


def render_post_html(content, content_format):
    if not content:
        return ""
    if content_format == "markdown":
        return mark_safe(render_markdown(content))
    return mark_safe(content)


def to_plain_text(content, content_format):
    html = render_post_html(content, content_format)
    return strip_tags(str(html)).strip()
