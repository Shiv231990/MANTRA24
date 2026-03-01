from django.utils.text import slugify
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            while Category.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    category = models.ForeignKey(
        Category,
        related_name="subcategories",
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=200)
    slug = models.SlugField(blank=True)

    class Meta:
        verbose_name_plural = "Sub Categories"
        unique_together = ("category", "slug")

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            while SubCategory.objects.filter(category=self.category, slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.category.name} → {self.name}"


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        related_name="products",
        on_delete=models.CASCADE
    )

    subcategory = models.ForeignKey(
        SubCategory,
        related_name="products",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    name = models.CharField(max_length=255)

    slug = models.SlugField(unique=True, blank=True, null=True)

    description = models.TextField(blank=True)

    price = models.DecimalField(max_digits=10, decimal_places=2)

    image = models.ImageField(
        upload_to="products/",
        blank=True,
        null=True
    )

    available = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name