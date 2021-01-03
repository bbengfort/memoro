# Generated by Django 3.1.3 on 2021-01-03 14:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('diary', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstapaperAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('account_id', models.IntegerField(blank=True, default=None, help_text='The Instapaper user_id field (should not change)', null=True)),
                ('username', models.CharField(blank=True, default=None, help_text='The Instapaper username field (may change)', max_length=255, null=True)),
                ('subscription_is_active', models.BooleanField(blank=True, default=None, help_text='If the account is using Instapaper Premium or not', null=True)),
                ('oauth_token', models.CharField(blank=True, default=None, editable=False, help_text='Cached xAuth token from authentication', max_length=75, null=True)),
                ('oauth_token_secret', models.CharField(blank=True, default=None, editable=False, help_text='Cached xAuth secret from authentication', max_length=75, null=True)),
                ('user', models.OneToOneField(help_text='The memoro user associated with the instapaper account', on_delete=django.db.models.deletion.CASCADE, related_name='instapaper_account', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Instapaper Account',
                'verbose_name_plural': 'Instapaper Accounts',
                'db_table': 'instapaper_accounts',
                'ordering': ('-modified',),
                'get_latest_by': 'modified',
            },
        ),
        migrations.CreateModel(
            name='ArticleCounts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('read', models.PositiveSmallIntegerField(blank=True, default=None, help_text='The number of articles read today', null=True)),
                ('unread', models.PositiveSmallIntegerField(blank=True, default=None, help_text='The number of articles to read today', null=True)),
                ('archived', models.PositiveSmallIntegerField(blank=True, default=None, help_text='The number of articles archived, year to date', null=True)),
                ('starred', models.PositiveSmallIntegerField(blank=True, default=None, help_text='The number of articles starred, year to date', null=True)),
                ('memo', models.OneToOneField(help_text='The reading list counts for the specified day', on_delete=django.db.models.deletion.CASCADE, related_name='article_counts', to='diary.memo')),
            ],
            options={
                'verbose_name': 'Reading List Count',
                'verbose_name_plural': 'Reading List Counts',
                'db_table': 'article_counts',
                'ordering': ('-memo__date',),
                'get_latest_by': 'memo__date',
            },
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('url', models.URLField(blank=True, default=None, help_text="The source of the article (will be empty if private source isn't)", max_length=500, null=True)),
                ('title', models.CharField(blank=True, default=None, help_text='The title of the article', max_length=512, null=True)),
                ('description', models.CharField(blank=True, default=None, help_text='A brief description or summary of the article', max_length=2000, null=True)),
                ('hash', models.CharField(blank=True, default=None, help_text='The Instapaper metadata hash for change detection', max_length=60, null=True)),
                ('progress', models.FloatField(blank=True, default=None, help_text='The percentage of the article read so far between 0 and 1', null=True)),
                ('progress_timestamp', models.DateTimeField(blank=True, default=None, help_text='The timestamp the progress was updated on', null=True)),
                ('bookmark_id', models.IntegerField(blank=True, default=None, help_text='The Instapaper bookmark id', null=True)),
                ('private_source', models.CharField(blank=True, default=None, help_text='The Instapaper private source (if stored, no URL is stored)', max_length=255, null=True)),
                ('time', models.DateTimeField(blank=True, default=None, help_text='Instapaper time field, likely when it was created or added', null=True)),
                ('starred', models.BooleanField(default=False, help_text='If the article has been starred in Instapaper')),
                ('folder', models.CharField(blank=True, default='unread', help_text='The Instapaper folder id, unread, starred, or archive', max_length=128)),
                ('deleted', models.BooleanField(default=False, help_text='If the article was deleted in Instapaper')),
                ('account', models.ForeignKey(help_text='The Instapaper account that fetched the article/bookmark', on_delete=django.db.models.deletion.PROTECT, related_name='bookmarks', to='reading.instapaperaccount')),
                ('memo', models.ForeignKey(blank=True, help_text='The memo the article is associated with, usually the day read', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='articles', to='diary.memo')),
            ],
            options={
                'verbose_name': 'Web Article',
                'verbose_name_plural': 'Web Articles',
                'db_table': 'web_articles',
                'ordering': ('-progress_timestamp',),
                'get_latest_by': 'progress_timestamp',
                'unique_together': {('url', 'private_source')},
            },
        ),
    ]
