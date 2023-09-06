from django.db import models
import os


def item_icon_image_path(instance, filename):
    # Extract the base name of the file (the filename without any directories)
    basename = os.path.basename(filename)
    return f'static/icon_images/{basename}'


class Item(models.Model):
    itemId = models.IntegerField(primary_key=True, verbose_name="Item ID")
    name = models.CharField(max_length=200, verbose_name="Item Name")
    icon = models.CharField(max_length=100, verbose_name="Icon Name")
    icon_image = models.ImageField(upload_to=item_icon_image_path, verbose_name="Icon Image")
    item_class = models.CharField(max_length=100, verbose_name="Class", blank=True, null=True)
    subclass = models.CharField(max_length=100, verbose_name="Subclass", blank=True, null=True)
    sellPrice = models.PositiveIntegerField(verbose_name="Sell Price", blank=True, null=True)
    quality = models.CharField(max_length=100, verbose_name="Quality", blank=True, null=True)
    itemLevel = models.PositiveIntegerField(verbose_name="Item Level", blank=True, null=True)
    requiredLevel = models.PositiveIntegerField(verbose_name="Required Level", blank=True, null=True)
    slot = models.CharField(max_length=50, verbose_name="Slot", blank=True, null=True)
    itemLink = models.TextField(verbose_name="Item Link", blank=True, null=True)
    vendorPrice = models.PositiveIntegerField(verbose_name="Vendor Price", blank=True, null=True)
    contentPhase = models.PositiveIntegerField(verbose_name="Content Phase", blank=True, null=True)
    uniqueName = models.SlugField(verbose_name="Unique Name", blank=True, null=True)

    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"

    def __str__(self):
        return self.name
