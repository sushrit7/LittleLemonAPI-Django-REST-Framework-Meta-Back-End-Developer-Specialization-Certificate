from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=255, db_index=True)

    def __str__(self) -> str:
        return self.title
    
class MenuItem(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, db_index=True)
    featured = models.BooleanField(db_index=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.title

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, blank=True)

    class Meta:
        unique_together = ( 'menuitem', 'user')

    def __str__(self) -> str:
        return self.menuitem.title
    
    def save(self, *args, **kwargs):
        # Automatically populate unit price and price based on MenuItem
        menu_item = self.menuitem
        self.unit_price = menu_item.price
        self.price = menu_item.price * self.quantity

        super().save(*args, **kwargs)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_crew = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='delivery_crew', null=True)
    status = models.BooleanField(db_index=True, default=0)
    total = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    date = models.DateTimeField(db_index=True, blank=True, null=True)

    def __str__(self) -> str:
        return str(self.user)
    
    def calculate_total(self):
        order_items = self.orderitem_set.all()
        total = sum(item.price for item in order_items)
        return total

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        unique_together = ('order', 'menuitem')

    def __str__(self) -> str:
        return str(self.menuitem)

