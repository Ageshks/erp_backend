from rest_framework import generics, permissions

from erp_modules.models import Customer, Employee, Inventory, Invoice, Lead, Order, Product, Project, Report, Vendor
from erp_modules.serializers import CustomerSerializer, EmployeeSerializer, InventorySerializer, InvoiceSerializer, LeadSerializer, OrderSerializer, ProductSerializer, ProjectSerializer, ReportSerializer, VendorSerializer


class EmployeeListCreateView(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]


class EmployeeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]


class LeadListCreateView(generics.ListCreateAPIView):
    queryset = Lead.objects.select_related('owner').all()
    serializer_class = LeadSerializer
    permission_classes = [permissions.IsAuthenticated]


class LeadDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lead.objects.select_related('owner').all()
    serializer_class = LeadSerializer
    permission_classes = [permissions.IsAuthenticated]


class VendorListCreateView(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [permissions.IsAuthenticated]


class VendorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]


class CustomerListCreateView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]


class CustomerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]


class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.select_related('customer', 'product').all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.select_related('customer', 'product').all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]


class InventoryListCreateView(generics.ListCreateAPIView):
    queryset = Inventory.objects.select_related('product').all()
    serializer_class = InventorySerializer
    permission_classes = [permissions.IsAuthenticated]


class InventoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Inventory.objects.select_related('product').all()
    serializer_class = InventorySerializer
    permission_classes = [permissions.IsAuthenticated]


class ReportListCreateView(generics.ListCreateAPIView):
    queryset = Report.objects.select_related('created_by').all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ReportDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Report.objects.select_related('created_by').all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]


class InvoiceListCreateView(generics.ListCreateAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]


class InvoiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProjectListCreateView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]
