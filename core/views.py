from django.db.models import Sum
from django.shortcuts import redirect, render

from erp_modules.forms import CustomerForm, EmployeeForm, InventoryForm, InvoiceForm, LeadForm, MetaCampaignForm, OrderForm, ProductForm, ProjectForm, ReportForm, VendorForm
from erp_modules.models import Customer, Employee, Inventory, Invoice, Lead, MetaCampaign, Order, Product, Project, Report, Vendor


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
    'customers': {
        'title': 'Customers',
        'subtitle': 'Manage customer contact details, companies, addresses, and status.',
        'highlights': ['Customer directory', 'Contact details', 'Order history', 'Status tracking'],
        'table_actions': ['Search', 'Filters'],
        'modals': ['Create', 'Delete'],
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
    'orders': {
        'title': 'Orders',
        'subtitle': 'Create and track customer orders from placement through completion.',
        'highlights': ['Order entry', 'Product selection', 'Status tracking', 'Order totals'],
        'table_actions': ['Search', 'Filters'],
        'modals': ['Create', 'Delete'],
    },
    'inventory': {
        'title': 'Inventory',
        'subtitle': 'Manage product quantities, storage locations, and reorder levels.',
        'highlights': ['Stock quantities', 'Locations', 'Reorder levels', 'Stock status'],
        'table_actions': ['Search', 'Filters'],
        'modals': ['Create', 'Delete'],
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
    employee_count = Employee.objects.count()
    lead_count = Lead.objects.count()
    customer_count = Customer.objects.count()
    product_count = Product.objects.count()
    order_count = Order.objects.count()
    pending_order_count = Order.objects.filter(status__in=['pending', 'processing']).count()
    inventory_units = Inventory.objects.aggregate(total=Sum('quantity'))['total'] or 0

    return render(request, 'dashboard.html', {
        'active_page': 'dashboard',
        'employee_count': employee_count,
        'lead_count': lead_count,
        'customer_count': customer_count,
        'product_count': product_count,
        'order_count': order_count,
        'pending_order_count': pending_order_count,
        'inventory_units': inventory_units,
        'recent_orders': Order.objects.select_related('product')[:5],
        'recent_products': Product.objects.all()[:5],
        'recent_leads': recent_leads,
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
    return redirect('module_page', 'reports')


def module_page_view(request, module_slug):
    module = MODULE_DETAILS.get(module_slug, MODULE_DETAILS['overview'])
    q = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status', '').strip()

    if request.method == 'POST':
        record_id = request.POST.get('record_id')
        if record_id and module_slug == 'employees':
            employee = Employee.objects.filter(pk=record_id).first()
            if employee:
                form = EmployeeForm(request.POST, instance=employee)
                if form.is_valid():
                    form.save()
                    return redirect('module_page', module_slug)
        elif module_slug == 'employees':
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
        elif module_slug == 'customers':
            form = CustomerForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('module_page', module_slug)
        elif module_slug == 'orders':
            form = OrderForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('module_page', module_slug)
        elif module_slug == 'inventory':
            form = InventoryForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('module_page', module_slug)
        elif module_slug == 'reports':
            form = ReportForm(request.POST)
            if form.is_valid():
                report = form.save(commit=False)
                report.created_by = request.user if request.user.is_authenticated else None
                report.save()
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
    if delete_id and module_slug == 'customers':
        Customer.objects.filter(pk=delete_id).delete()
        return redirect('module_page', module_slug)
    if delete_id and module_slug == 'orders':
        Order.objects.filter(pk=delete_id).delete()
        return redirect('module_page', module_slug)
    if delete_id and module_slug == 'inventory':
        Inventory.objects.filter(pk=delete_id).delete()
        return redirect('module_page', module_slug)
    if delete_id and module_slug == 'reports':
        Report.objects.filter(pk=delete_id).delete()
        return redirect('module_page', module_slug)
    if delete_id and module_slug == 'invoices':
        Invoice.objects.filter(pk=delete_id).delete()
        return redirect('module_page', module_slug)
    if delete_id and module_slug == 'projects':
        Project.objects.filter(pk=delete_id).delete()
        return redirect('module_page', module_slug)

    employees = Employee.objects.all() if module_slug == 'employees' else []
    if module_slug == 'employees':
        employees = employees.filter(name__icontains=q) if q else employees
        if status_filter:
            employees = employees.filter(status=status_filter)

    leads = Lead.objects.select_related('owner').all() if module_slug == 'leads' else []
    if module_slug == 'leads':
        leads = leads.filter(full_name__icontains=q) if q else leads
        if status_filter:
            leads = leads.filter(stage=status_filter)

    vendors = Vendor.objects.all() if module_slug == 'vendors' else []
    if module_slug == 'vendors':
        vendors = vendors.filter(name__icontains=q) if q else vendors
        if status_filter:
            vendors = vendors.filter(status=status_filter)

    products = Product.objects.all() if module_slug == 'products' else []
    if module_slug == 'products':
        products = products.filter(name__icontains=q) if q else products
        if status_filter:
            products = products.filter(status=status_filter)

    customers = Customer.objects.all() if module_slug == 'customers' else []
    if module_slug == 'customers':
        customers = customers.filter(name__icontains=q) if q else customers
        if status_filter:
            customers = customers.filter(status=status_filter)

    orders = Order.objects.select_related('product').all() if module_slug == 'orders' else []
    if module_slug == 'orders':
        orders = orders.filter(order_number__icontains=q) if q else orders
        if status_filter:
            orders = orders.filter(status=status_filter)

    inventory = Inventory.objects.select_related('product').all() if module_slug == 'inventory' else []
    if module_slug == 'inventory' and q:
        inventory = inventory.filter(product__name__icontains=q)

    reports = Report.objects.select_related('created_by').all() if module_slug == 'reports' else []
    if module_slug == 'reports':
        reports = reports.filter(title__icontains=q) if q else reports
        if status_filter:
            reports = reports.filter(status=status_filter)

    invoices = Invoice.objects.all() if module_slug == 'invoices' else []
    if module_slug == 'invoices':
        invoices = invoices.filter(invoice_number__icontains=q) if q else invoices
        if status_filter:
            invoices = invoices.filter(status=status_filter)

    projects = Project.objects.all() if module_slug == 'projects' else []
    if module_slug == 'projects':
        projects = projects.filter(name__icontains=q) if q else projects
        if status_filter:
            projects = projects.filter(status=status_filter)
    employee_form = EmployeeForm() if module_slug == 'employees' else None
    lead_form = LeadForm() if module_slug == 'leads' else None
    vendor_form = VendorForm() if module_slug == 'vendors' else None
    product_form = ProductForm() if module_slug == 'products' else None
    customer_form = CustomerForm() if module_slug == 'customers' else None
    order_form = OrderForm() if module_slug == 'orders' else None
    inventory_form = InventoryForm() if module_slug == 'inventory' else None
    report_form = ReportForm() if module_slug == 'reports' else None
    invoice_form = InvoiceForm() if module_slug == 'invoices' else None
    project_form = ProjectForm() if module_slug == 'projects' else None

    return render(request, 'module_page.html', {
        'active_page': module_slug,
        'module': module,
        'module_slug': module_slug,
        'q': q,
        'status_filter': status_filter,
        'employees': employees,
        'leads': leads,
        'vendors': vendors,
        'products': products,
        'customers': customers,
        'orders': orders,
        'inventory': inventory,
        'reports': reports,
        'invoices': invoices,
        'projects': projects,
        'employee_form': employee_form,
        'lead_form': lead_form,
        'vendor_form': vendor_form,
        'product_form': product_form,
        'customer_form': customer_form,
        'order_form': order_form,
        'inventory_form': inventory_form,
        'report_form': report_form,
        'invoice_form': invoice_form,
        'project_form': project_form,
    })
