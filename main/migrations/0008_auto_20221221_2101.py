# Generated by Django 3.2.14 on 2022-12-21 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_cartproduct_price_id_product_product_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='id',
        ),
        migrations.RemoveField(
            model_name='product',
            name='type',
        ),
        migrations.AddField(
            model_name='product',
            name='cat',
            field=models.CharField(choices=[('B', 'Books'), ('S', 'Services'), ('E', 'Electronics'), ('M', 'Merch')], default='M', max_length=2),
        ),
        migrations.AddField(
            model_name='product',
            name='external_product_id',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='image_name',
            field=models.CharField(blank=True, default='', max_length=250),
        ),
        migrations.AddField(
            model_name='product',
            name='mode',
            field=models.CharField(choices=[('P', 'payment'), ('S', 'subscription')], default='P', max_length=1),
        ),
        migrations.AddField(
            model_name='product',
            name='page',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AddField(
            model_name='product',
            name='tax_code',
            field=models.CharField(choices=[('txcd_99999999', 'Goods'), ('txcd_20030000', 'Services'), ('txcd_10701100', 'Hosting'), ('txcd_34021000', 'Phones'), ('txcd_35010000', 'Books')], default='txcd_99999999', max_length=20),
        ),
        migrations.AlterField(
            model_name='cartproduct',
            name='price',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, upload_to='data_here'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
