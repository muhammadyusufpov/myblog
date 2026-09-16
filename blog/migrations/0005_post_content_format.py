from django.db import migrations, models


def mark_existing_posts_as_html(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    Post.objects.update(content_format="html")


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0004_alter_post_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="content_format",
            field=models.CharField(
                choices=[("html", "HTML"), ("markdown", "Markdown")],
                default="markdown",
                max_length=10,
            ),
        ),
        migrations.RunPython(mark_existing_posts_as_html, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="post",
            name="content",
            field=models.TextField(),
        ),
    ]
