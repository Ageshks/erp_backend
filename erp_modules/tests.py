from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from erp_modules.models import Employee, Lead


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

    def test_dashboard_meta_campaign_flow(self):
        response = self.client.post(reverse('dashboard'), {
            'name': 'Spring Launch',
            'objective': 'LEAD_GENERATION',
            'audience': 'SMB Owners',
            'budget': '150',
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Lead.objects.filter(company__icontains='Meta').exists())

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
