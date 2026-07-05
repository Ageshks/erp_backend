from django import forms

from erp_modules.models import Employee, Invoice, Lead, MetaCampaign, Product, Project, Vendor


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


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['invoice_number', 'customer_name', 'amount', 'status', 'due_date']


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'client', 'deadline', 'status', 'budget']
