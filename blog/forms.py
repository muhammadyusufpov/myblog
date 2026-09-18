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
                    "data-editor": "markdown",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        original_format = Post.FORMAT_MARKDOWN
        if self.instance.pk:
            original_format = self.instance.content_format or Post.FORMAT_MARKDOWN
        self.fields["content"].widget.attrs["data-original-format"] = original_format
