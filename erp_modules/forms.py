from django import forms

from erp_modules.models import Customer, Employee, Inventory, Invoice, Lead, MetaCampaign, Order, Product, Project, Report, Vendor


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'email', 'phone', 'department', 'position', 'status']


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['full_name', 'email', 'phone', 'company', 'source', 'stage', 'notes', 'owner']


class MetaCampaignForm(forms.ModelForm):
    class Meta:
        model = MetaCampaign
        fields = ['name', 'objective', 'audience', 'budget']


class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['name', 'email', 'phone', 'company', 'status']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'sku', 'category', 'price', 'stock', 'status']


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone', 'company', 'address', 'status']


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['order_number', 'customer', 'product', 'quantity', 'status']


class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['product', 'quantity', 'reorder_level', 'location']


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['title', 'report_type', 'status', 'notes']


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['invoice_number', 'customer_name', 'amount', 'status', 'due_date']


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'client', 'deadline', 'status', 'budget']
