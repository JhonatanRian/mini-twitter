# Generated by Django 4.1.1 on 2022-10-03 21:12

from django.db import migrations, models
import django.db.models.deletion
import stdimage.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('update', models.DateField(auto_now=True)),
                ('text', models.CharField(max_length=355)),
                ('archive', models.FileField(blank=True, upload_to='publications')),
            ],
            options={
                'verbose_name': 'publication',
                'verbose_name_plural': 'publications',
            },
        ),
        migrations.CreateModel(
            name='TypeReaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('update', models.DateField(auto_now=True)),
                ('name', models.CharField(max_length=10)),
                ('image', stdimage.models.StdImageField(force_min_size=False, upload_to='reactions', variations={}, verbose_name='imagem')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('publication_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='publications.publication')),
            ],
            options={
                'verbose_name': 'comment',
                'verbose_name_plural': 'comments',
            },
            bases=('publications.publication',),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('publication_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='publications.publication')),
                ('visible', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('publications.publication',),
        ),
        migrations.CreateModel(
            name='Reaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('update', models.DateField(auto_now=True)),
                ('type_reaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='type_reaction', to='publications.typereaction')),
                ('comment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reaction', to='publications.comment')),
                ('post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reaction', to='publications.post')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]