from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def roles(request):
    return render(request, 'accounts/roles.html')


@login_required
def audit_logs(request):
    return render(request, 'accounts/audit-logs.html')


@login_required
def settings(request):
    return render(request, 'accounts/settings.html')
