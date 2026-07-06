from django.db import models
from django.conf import settings


class Employee(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('onboarding', 'Onboarding'),
    ]

    name = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    department = models.CharField(max_length=80, blank=True)
    position = models.CharField(max_length=80, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Lead(models.Model):
    SOURCE_CHOICES = [
        ('organic', 'Organic'),
        ('paid', 'Paid'),
        ('referral', 'Referral'),
        ('social', 'Social'),
    ]
    STAGE_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('qualified', 'Qualified'),
        ('won', 'Won'),
        ('lost', 'Lost'),
    ]

    full_name = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=120, blank=True)
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='organic')
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES, default='new')
    notes = models.TextField(blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='owned_leads')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.full_name


class MetaCampaign(models.Model):
    OBJECTIVE_CHOICES = [
        ('LEAD_GENERATION', 'Lead Generation'),
        ('TRAFFIC', 'Traffic'),
        ('ENGAGEMENT', 'Engagement'),
    ]

    name = models.CharField(max_length=120)
    objective = models.CharField(max_length=30, choices=OBJECTIVE_CHOICES, default='LEAD_GENERATION')
    audience = models.CharField(max_length=120)
    budget = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, default='queued')
    response_summary = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Vendor(models.Model):
    STATUS_CHOICES = [('active', 'Active'), ('inactive', 'Inactive')]

    name = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=120, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Product(models.Model):
    STATUS_CHOICES = [('in_stock', 'In Stock'), ('low_stock', 'Low Stock'), ('out_of_stock', 'Out of Stock')]

    name = models.CharField(max_length=120)
    sku = models.CharField(max_length=50, unique=True)
    category = models.CharField(max_length=80, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_stock')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Customer(models.Model):
    STATUS_CHOICES = [('active', 'Active'), ('inactive', 'Inactive')]

    name = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=120, blank=True)
    address = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [('pending', 'Pending'), ('processing', 'Processing'), ('completed', 'Completed'), ('cancelled', 'Cancelled')]

    order_number = models.CharField(max_length=50, unique=True)
    customer_name = models.CharField(max_length=120)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='orders', null=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='orders')
    quantity = models.PositiveIntegerField(default=1)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if self.customer_id:
            self.customer_name = self.customer.name
        self.total_amount = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class Inventory(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='inventory')
    quantity = models.PositiveIntegerField(default=0)
    reorder_level = models.PositiveIntegerField(default=5)
    location = models.CharField(max_length=120, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['product__name']
        verbose_name_plural = 'inventory'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        status = 'out_of_stock' if self.quantity == 0 else ('low_stock' if self.quantity <= self.reorder_level else 'in_stock')
        Product.objects.filter(pk=self.product_id).update(stock=self.quantity, status=status)

    def __str__(self):
        return f'{self.product.name} inventory'


class Report(models.Model):
    TYPE_CHOICES = [('sales', 'Sales'), ('inventory', 'Inventory'), ('finance', 'Finance'), ('operations', 'Operations')]
    STATUS_CHOICES = [('draft', 'Draft'), ('ready', 'Ready'), ('archived', 'Archived')]

    title = models.CharField(max_length=160)
    report_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='reports')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Invoice(models.Model):
    STATUS_CHOICES = [('draft', 'Draft'), ('sent', 'Sent'), ('paid', 'Paid'), ('overdue', 'Overdue')]

    invoice_number = models.CharField(max_length=50, unique=True)
    customer_name = models.CharField(max_length=120)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.invoice_number


class Project(models.Model):
    STATUS_CHOICES = [('planning', 'Planning'), ('active', 'Active'), ('completed', 'Completed')]

    name = models.CharField(max_length=120)
    client = models.CharField(max_length=120, blank=True)
    deadline = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planning')
    budget = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name
