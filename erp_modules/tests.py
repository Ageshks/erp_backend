from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from erp_modules.models import Customer, Employee, Inventory, Lead, Order, Product, Report


class ModuleCrudTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(email='module@example.com', password='StrongPass123!')
        self.client.force_authenticate(self.user)

    def test_employee_crud_flow(self):
        create_url = reverse('erp_modules:employee-list-create')
        response = self.client.post(create_url, {
            'name': 'Ava',
            'email': 'ava@example.com',
            'department': 'Engineering',
            'position': 'Developer',
            'status': 'active',
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        employee = Employee.objects.get(email='ava@example.com')
        detail_url = reverse('erp_modules:employee-detail', kwargs={'pk': employee.pk})
        patch_response = self.client.patch(detail_url, {'position': 'Lead Developer'})
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)
        self.assertEqual(Employee.objects.get(pk=employee.pk).position, 'Lead Developer')
        delete_response = self.client.delete(detail_url)
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)

    def test_lead_crud_flow(self):
        create_url = reverse('erp_modules:lead-list-create')
        response = self.client.post(create_url, {
            'full_name': 'Mina Patel',
            'email': 'mina@example.com',
            'company': 'Northwind',
            'source': 'social',
            'stage': 'new',
            'notes': 'Interested in enterprise plan',
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        lead = Lead.objects.get(email='mina@example.com')
        detail_url = reverse('erp_modules:lead-detail', kwargs={'pk': lead.pk})
        patch_response = self.client.patch(detail_url, {'stage': 'qualified'})
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)
        self.assertEqual(Lead.objects.get(pk=lead.pk).stage, 'qualified')
        delete_response = self.client.delete(detail_url)
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)

    def test_dashboard_uses_database_records(self):
        Product.objects.create(name='Widget', sku='W-1', price='10.00', stock=3)
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'Widget')

    def test_product_order_inventory_and_report_crud(self):
        customer_response = self.client.post(reverse('erp_modules:customer-list-create'), {
            'name': 'Tester', 'email': 'customer@example.com', 'status': 'active',
        })
        self.assertEqual(customer_response.status_code, status.HTTP_201_CREATED)
        customer = Customer.objects.get(email='customer@example.com')

        product_response = self.client.post(reverse('erp_modules:product-list-create'), {
            'name': 'Widget', 'sku': 'W-1', 'price': '10.00', 'stock': 0, 'status': 'out_of_stock',
        })
        self.assertEqual(product_response.status_code, status.HTTP_201_CREATED)
        product = Product.objects.get(sku='W-1')

        inventory_response = self.client.post(reverse('erp_modules:inventory-list-create'), {
            'product': product.pk, 'quantity': 12, 'reorder_level': 3, 'location': 'A1',
        })
        self.assertEqual(inventory_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.get(pk=product.pk).stock, 12)

        order_response = self.client.post(reverse('erp_modules:order-list-create'), {
            'order_number': 'ORD-1', 'customer': customer.pk, 'product': product.pk, 'quantity': 2,
        })
        self.assertEqual(order_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.get(order_number='ORD-1').total_amount, 20)
        self.assertEqual(Order.objects.get(order_number='ORD-1').customer_name, 'Tester')

        report_response = self.client.post(reverse('erp_modules:report-list-create'), {
            'title': 'Stock report', 'report_type': 'inventory', 'status': 'ready',
        })
        self.assertEqual(report_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Report.objects.get().created_by, self.user)

    def test_module_search_and_inline_edit(self):
        employee = Employee.objects.create(
            name='Ava Carter',
            email='ava.search@example.com',
            department='Sales',
            position='Manager',
            status='active',
        )
        Employee.objects.create(
            name='Mina Patel',
            email='mina@example.com',
            department='HR',
            position='Lead',
            status='inactive',
        )

        response = self.client.get(reverse('module_page', kwargs={'module_slug': 'employees'}), {'q': 'ava', 'status': 'active'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'Ava Carter')
        self.assertNotContains(response, 'Mina Patel')

        update_response = self.client.post(reverse('module_page', kwargs={'module_slug': 'employees'}), {
            'record_id': employee.pk,
            'name': 'Ava Carter',
            'email': 'ava.search@example.com',
            'department': 'Operations',
            'position': 'Director',
            'status': 'active',
        })
        self.assertEqual(update_response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(Employee.objects.get(pk=employee.pk).department, 'Operations')
