from django.shortcuts import render


PLACEHOLDER_PAGES = {
    'medicines': ('inventory/medicines.html', 'Medicines', 'Browse and manage the pharmacy medicine catalogue.'),
    'categories': ('inventory/categories.html', 'Categories', 'Group medicines into categories for easier browsing.'),
    'suppliers': ('inventory/suppliers.html', 'Suppliers', 'Keep supplier details and contact information in one place.'),
    'stocks': ('inventory/stocks.html', 'Stocks', 'Track stock levels and replenishments.'),
    'expiry_dates': ('inventory/expiry-dates.html', 'Expiry Dates', 'Monitor batch expiry dates and approaching expiries.'),
    'alerts': ('inventory/alerts.html', 'Alerts', 'Low stock, expired batch, and other system alerts.'),
}


def _placeholder(request, page):
    template, title, description = PLACEHOLDER_PAGES[page]
    return render(request, template, {'page_title': title, 'description': description})


def medicines(request):
    return _placeholder(request, 'medicines')


def categories(request):
    return _placeholder(request, 'categories')


def suppliers(request):
    return _placeholder(request, 'suppliers')


def stocks(request):
    return _placeholder(request, 'stocks')


def expiry_dates(request):
    return _placeholder(request, 'expiry_dates')


def alerts(request):
    return _placeholder(request, 'alerts')
