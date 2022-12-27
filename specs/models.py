from django.db import models


class CategoryFeature(models.Model):
    category = models.ForeignKey('mainapp.Category',
                                 verbose_name='Категория',
                                 on_delete=models.CASCADE)
    feature_name = models.CharField(max_length=99,
                                    verbose_name='Имя ключа для категории')
    feature_filter_name = models.CharField(max_length=99, verbose_name='Имя для фильтрации')
    unit = models.CharField(verbose_name='Единица измерения', blank=True, null=True, max_length=44)

    class Meta:
        unique_together = ('category', 'feature_name', 'feature_filter_name', 'unit')

        def __str__(self):
            return f"{self.category.name} | {self.feature_name}"


class FeatureValidator(models.Model):
    category = models.ForeignKey('mainapp.Category', verbose_name='Категория', on_delete=models.CASCADE)
    feature_key = models.ForeignKey(CategoryFeature, verbose_name='Ключ характеристики', on_delete=models.CASCADE)
    valid_feature_value = models.CharField(max_length=123, verbose_name='Валидное значение')

    def __str__(self):
        return f"Товар {self.category} |"\
                f"Характеристика {self.feature_key} |"\
                f"Валидное значение {self.valid_feature_value}"


class ProductFeature(models.Model):
    product = models.ForeignKey('mainapp.Product', verbose_name='Товар', on_delete=models.CASCADE)
    feature = models.ForeignKey(CategoryFeature, verbose_name='Характеристика', on_delete=models.CASCADE)
    value = models.CharField(max_length=255, verbose_name='Значение')

    def __str__(self):
        return f"Товар {self.product} |"\
                f"Характеристика {self.feature.feature_name} |"\
                f"Значение {self.value}"

