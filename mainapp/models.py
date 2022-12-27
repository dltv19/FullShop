from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    # https://127.0.0.1:8000/mainapp/category_detail/spirts
    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class Product(models.Model):
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='products/')
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')
    features = models.ManyToManyField('specs.ProductFeature', blank=True, null=True, related_name='features_for_product')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})

    def get_features(self):
        return {f.feature.fearure_name: ' '.join([f.value, f.feature.unit or '']) for f in self.features.all()}


class CartProduct(models.Model):
    user = models.ForeignKey('Customer', on_delete=models.CASCADE, verbose_name='Покупатель')
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, related_name='related_products', verbose_name='Корзина')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена')
    qty = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Продукт {self.product.title} (для корзины)"

    def save(self, *args, **kwargs):
        self.final_price = self.qty * self.product.price
        super().save(*args, **kwargs)


class Cart(models.Model):
    owner = models.ForeignKey('Customer', on_delete=models.CASCADE, verbose_name='Пользователь', null=True, blank=True)
    products = models.ManyToManyField(CartProduct, blank=True, null=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name='Общая цена')
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.owner)


class Customer(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Номер телефона', blank=True, null=True)
    address = models.CharField(max_length=255, verbose_name='Адрес', blank=True, null=True)
    order = models.ManyToManyField('Order', verbose_name='Заказы покупателя', related_name='related_order')

    def __str__(self):
        return f"Покупатель: {self.user.first_name}, {self.user.last_name}"


class Order(models.Model):
    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'ready'
    STATUS_COMPLETED = 'completed'

    BUYING_TYPE_SELF = 'self'
    BUYING_TYPE_DELIVERY = 'delivery'

    STATUS_CHOICES = (
        (STATUS_NEW, "Новый заказ"),
        (STATUS_IN_PROGRESS, "Заказ в обработке"),
        (STATUS_READY, "Заказ готов"),
        (STATUS_COMPLETED, "Заказ выполнен")
    )

    BUYING_TYPE_CHOICES = (
        (BUYING_TYPE_SELF, 'Самовызов'),
        (BUYING_TYPE_DELIVERY, 'Доставка')
    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='related_orders', verbose_name='Покупатель')
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    phone = models.CharField(max_length=12, verbose_name='Телефон')
    cart = models.ForeignKey(Cart, verbose_name='Корзина', on_delete=models.CASCADE, blank=True, null=True)
    address = models.CharField(max_length=1024, verbose_name='Адрес', null=True, blank=True)
    status = models.CharField(
        max_length=100,
        verbose_name='Статус заказа',
        choices=STATUS_CHOICES,
        default=STATUS_NEW
    )
    buying_type = models.CharField(max_length=100, verbose_name='Тип заказа', choices=BUYING_TYPE_CHOICES, default=BUYING_TYPE_SELF)
    comment = models.TextField(verbose_name='Комментарий к заказу')
    created_at = models.DateTimeField(auto_now=True, verbose_name='Дата создания заказа')
    order_date = models.DateTimeField(verbose_name='Дата получения заказа', default=timezone.now())

    def __str__(self):
        return str(self.customer.user)