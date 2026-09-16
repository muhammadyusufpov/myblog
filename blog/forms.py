from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["category", "title", "content"]
        widgets = {
            "category": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. AI, Politics, Technology...",
                }
            ),
            "title": forms.TextInput(
                attrs={
                    "class": "form-control title-input",
                    "placeholder": "Title of your article...",
                }
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "form-control markdown-textarea",
                    "rows": 18,
                    "placeholder": "Write in Markdown...",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        is_html = bool(
            self.instance
            and self.instance.pk
            and self.instance.content_format == Post.FORMAT_HTML
        )
        editor = "html" if is_html else "markdown"
        self.fields["content"].widget.attrs["data-editor"] = editor
        if is_html:
            self.fields["content"].widget.attrs["class"] = "form-control html-textarea"
            self.fields["content"].widget.attrs["placeholder"] = "HTML content"
