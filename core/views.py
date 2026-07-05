from decimal import Decimal

from django.shortcuts import redirect, render
from django.utils.text import slugify

from erp_modules.forms import EmployeeForm, InvoiceForm, LeadForm, MetaCampaignForm, ProductForm, ProjectForm, VendorForm
from erp_modules.models import Employee, Invoice, Lead, MetaCampaign, Product, Project, Vendor


MODULE_DETAILS = {
    'overview': {
        'title': 'Dashboard Overview',
        'subtitle': 'Executive summary with KPI cards, trends, approvals, and stock alerts.',
        'highlights': ['Top statistics cards', 'Sales and revenue charts', 'Pending approvals', 'Low stock alerts'],
        'table_actions': ['Search', 'Filters', 'Sorting', 'Pagination', 'Export CSV', 'Export Excel', 'Print', 'Bulk Actions'],
        'modals': ['Create Modal', 'Edit Modal', 'Delete Confirmation', 'View Details Modal'],
    },
    'analytics': {
        'title': 'Analytics',
        'subtitle': 'Deep business analysis for sales, finance, and people performance.',
        'highlights': ['Revenue analytics', 'Employee growth', 'Purchase analytics', 'Sales trend analysis'],
        'table_actions': ['Search', 'Filters', 'Sorting', 'Pagination', 'Export CSV', 'Export Excel', 'Print'],
        'modals': ['View Details Modal', 'Export Report Modal'],
    },
    'reports': {
        'title': 'Reports',
        'subtitle': 'Operational and leadership reporting for the entire ERP platform.',
        'highlights': ['Profit and loss', 'Balance sheet', 'Inventory reports', 'HR productivity reports'],
        'table_actions': ['Search', 'Filters', 'Sorting', 'Pagination', 'Export CSV', 'Export Excel', 'Print'],
        'modals': ['Schedule Report Modal', 'View Details Modal'],
    },
    'company-profile': {
        'title': 'Company Profile',
        'subtitle': 'Manage organization identity, branches, policies, and tax information.',
        'highlights': ['Organization identity', 'Branch structure', 'Tax and policy settings', 'Document management'],
        'table_actions': ['Search', 'Filters', 'Sorting', 'Pagination', 'Export CSV', 'Export Excel', 'Print'],
        'modals': ['Create Modal', 'Edit Modal', 'Delete Confirmation'],
    },
    'employees': {
        'title': 'Employees',
        'subtitle': 'Core workforce records for onboarding, performance, and payroll.',
        'highlights': ['Employee directory', 'Role assignment', 'Payroll linkage', 'Document upload'],
        'table_actions': ['Search', 'Filters', 'Sorting', 'Pagination', 'Export CSV', 'Export Excel', 'Print', 'Bulk Actions'],
        'modals': ['Create Modal', 'Edit Modal', 'Delete Confirmation', 'View Details Modal'],
    },
    'attendance': {
        'title': 'Attendance',
        'subtitle': 'Track check-ins, shifts, attendance summaries, and absence history.',
        'highlights': ['Daily presence tracking', 'Shift management', 'Attendance summary', 'Exception reports'],
        'table_actions': ['Search', 'Filters', 'Sorting', 'Pagination', 'Export CSV', 'Export Excel', 'Print'],
        'modals': ['Create Modal', 'Edit Modal', 'View Details Modal'],
    },
    'leads': {
        'title': 'Leads',
        'subtitle': 'Capture and qualify opportunities across the sales lifecycle.',
        'highlights': ['Lead capture', 'Follow-up scheduling', 'Sales pipeline view', 'Assignment rules'],
        'table_actions': ['Search', 'Filters', 'Sorting', 'Pagination', 'Export CSV', 'Export Excel', 'Print', 'Bulk Actions'],
        'modals': ['Create Modal', 'Edit Modal', 'Delete Confirmation', 'View Details Modal'],
    },
    'vendors': {
        'title': 'Vendors',
        'subtitle': 'Vendor profiles, approvals, payments, and supplier performance.',
        'highlights': ['Vendor directory', 'Purchase approvals', 'Payments tracking', 'Performance insights'],
        'table_actions': ['Search', 'Filters', 'Sorting', 'Pagination', 'Export CSV', 'Export Excel', 'Print', 'Bulk Actions'],
        'modals': ['Create Modal', 'Edit Modal', 'Delete Confirmation', 'View Details Modal'],
    },
    'products': {
        'title': 'Products',
        'subtitle': 'Inventory catalog, categories, stock movement, and reorder intelligence.',
        'highlights': ['Product master data', 'Stock levels', 'Barcode management', 'Reorder alerts'],
        'table_actions': ['Search', 'Filters', 'Sorting', 'Pagination', 'Export CSV', 'Export Excel', 'Print', 'Bulk Actions'],
        'modals': ['Create Modal', 'Edit Modal', 'Delete Confirmation', 'View Details Modal'],
    },
    'invoices': {
        'title': 'Invoices',
        'subtitle': 'Billing and receivable workflow for customers and sales orders.',
        'highlights': ['Invoice generation', 'Payment tracking', 'Tax handling', 'Outstanding balances'],
        'table_actions': ['Search', 'Filters', 'Sorting', 'Pagination', 'Export CSV', 'Export Excel', 'Print'],
        'modals': ['Create Modal', 'Edit Modal', 'View Details Modal'],
    },
    'projects': {
        'title': 'Projects',
        'subtitle': 'Delivery planning, status tracking, team assignments, and timelines.',
        'highlights': ['Project planning', 'Task assignment', 'Progress tracking', 'Timeline monitoring'],
        'table_actions': ['Search', 'Filters', 'Sorting', 'Pagination', 'Export CSV', 'Export Excel', 'Print', 'Bulk Actions'],
        'modals': ['Create Modal', 'Edit Modal', 'Delete Confirmation', 'View Details Modal'],
    },
    'user-management': {
        'title': 'User Management',
        'subtitle': 'Admin controls for users, roles, permissions, and access governance.',
        'highlights': ['User administration', 'Role assignment', 'Permission mapping', 'Audit readiness'],
        'table_actions': ['Search', 'Filters', 'Sorting', 'Pagination', 'Export CSV', 'Export Excel', 'Print', 'Bulk Actions'],
        'modals': ['Create Modal', 'Edit Modal', 'Delete Confirmation', 'View Details Modal'],
    },
    'manage-organizations': {
        'title': 'Manage Organizations',
        'subtitle': 'Super admin controls for organizations, subscription plans, billing, and monitoring.',
        'highlights': ['Organization management', 'Subscription controls', 'Billing and limits', 'System monitoring'],
        'table_actions': ['Search', 'Filters', 'Sorting', 'Pagination', 'Export CSV', 'Export Excel', 'Print', 'Bulk Actions'],
        'modals': ['Create Modal', 'Edit Modal', 'Delete Confirmation', 'View Details Modal'],
    },
}


def dashboard_view(request):
    recent_leads = Lead.objects.select_related('owner').order_by('-created_at')[:5]
    recent_campaigns = MetaCampaign.objects.order_by('-created_at')[:5]
    employee_count = Employee.objects.count()
    lead_count = Lead.objects.count()

    if request.method == 'POST':
        form = MetaCampaignForm(request.POST)
        if form.is_valid():
            campaign = form.save(commit=False)
            campaign.status = 'running'
            campaign.response_summary = (
                f"Simulated Meta ad delivery is live for {campaign.audience}. "
                f"Expected response: {max(8, int(campaign.budget / 20))} leads this week."
            )
            campaign.save()

            Lead.objects.create(
                full_name=f"{campaign.name} Prospect",
                email=f"{slugify(campaign.name)}@meta.local",
                company=f"Meta {campaign.name}",
                source='social',
                stage='new',
                notes=f"Meta campaign response from {campaign.audience}.",
            )

    form = MetaCampaignForm()
    return render(request, 'dashboard.html', {
        'active_page': 'dashboard',
        'employee_count': employee_count,
        'lead_count': lead_count,
        'recent_leads': recent_leads,
        'recent_campaigns': recent_campaigns,
        'campaign_form': form,
    })


def crm_view(request):
    return render(request, 'crm.html', {'active_page': 'crm'})


def finance_view(request):
    return render(request, 'finance.html', {'active_page': 'finance'})


def hr_view(request):
    return render(request, 'hr.html', {'active_page': 'hr'})


def projects_view(request):
    return render(request, 'projects.html', {'active_page': 'projects'})


def reports_view(request):
    return render(request, 'reports.html', {'active_page': 'reports'})


def module_page_view(request, module_slug):
    module = MODULE_DETAILS.get(module_slug, MODULE_DETAILS['overview'])

    if request.method == 'POST':
        if module_slug == 'employees':
            form = EmployeeForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('module_page', module_slug)
        elif module_slug == 'leads':
            form = LeadForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('module_page', module_slug)
        elif module_slug == 'vendors':
            form = VendorForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('module_page', module_slug)
        elif module_slug == 'products':
            form = ProductForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('module_page', module_slug)
        elif module_slug == 'invoices':
            form = InvoiceForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('module_page', module_slug)
        elif module_slug == 'projects':
            form = ProjectForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('module_page', module_slug)

    delete_id = request.GET.get('delete')
    if delete_id and module_slug == 'employees':
        Employee.objects.filter(pk=delete_id).delete()
        return redirect('module_page', module_slug)
    if delete_id and module_slug == 'leads':
        Lead.objects.filter(pk=delete_id).delete()
        return redirect('module_page', module_slug)
    if delete_id and module_slug == 'vendors':
        Vendor.objects.filter(pk=delete_id).delete()
        return redirect('module_page', module_slug)
    if delete_id and module_slug == 'products':
        Product.objects.filter(pk=delete_id).delete()
        return redirect('module_page', module_slug)
    if delete_id and module_slug == 'invoices':
        Invoice.objects.filter(pk=delete_id).delete()
        return redirect('module_page', module_slug)
    if delete_id and module_slug == 'projects':
        Project.objects.filter(pk=delete_id).delete()
        return redirect('module_page', module_slug)

    employees = Employee.objects.all() if module_slug == 'employees' else []
    leads = Lead.objects.select_related('owner').all() if module_slug == 'leads' else []
    vendors = Vendor.objects.all() if module_slug == 'vendors' else []
    products = Product.objects.all() if module_slug == 'products' else []
    invoices = Invoice.objects.all() if module_slug == 'invoices' else []
    projects = Project.objects.all() if module_slug == 'projects' else []
    employee_form = EmployeeForm() if module_slug == 'employees' else None
    lead_form = LeadForm() if module_slug == 'leads' else None
    vendor_form = VendorForm() if module_slug == 'vendors' else None
    product_form = ProductForm() if module_slug == 'products' else None
    invoice_form = InvoiceForm() if module_slug == 'invoices' else None
    project_form = ProjectForm() if module_slug == 'projects' else None

    return render(request, 'module_page.html', {
        'active_page': module_slug,
        'module': module,
        'module_slug': module_slug,
        'employees': employees,
        'leads': leads,
        'vendors': vendors,
        'products': products,
        'invoices': invoices,
        'projects': projects,
        'employee_form': employee_form,
        'lead_form': lead_form,
        'vendor_form': vendor_form,
        'product_form': product_form,
        'invoice_form': invoice_form,
        'project_form': project_form,
    })
