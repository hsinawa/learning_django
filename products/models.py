from django.db import models



class Product(models.Model): # Product model with all fields
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100) 
    stock_available = models.PositiveIntegerField()
    units_sold = models.PositiveIntegerField(default=0)
    customer_rating = models.FloatField(default=0.0)
    demand_forecast = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)  
    optimized_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name
    
    
    
class SampleTest(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name