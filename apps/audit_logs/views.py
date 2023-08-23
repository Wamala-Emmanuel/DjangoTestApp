from django.shortcuts import render
from .models import AuditLog
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required

# Create your views here.
def audit_logs(request):
    audit_logs = AuditLog.objects.all().order_by('-created')

    page = request.GET.get('page', 1)
    query = request.GET.get("q")
    
    if query:
        audit_logs = AuditLog.objects.all().order_by('-created')

    paginator = Paginator(audit_logs, 20)
    
    try:
        audit_logs = paginator.page(page)
    except PageNotAnInteger:
        audit_logs = paginator.page(1)
    except EmptyPage:
        audit_logs = paginator.page(paginator.num_pages)

    context = {
        'audit_logs': audit_logs,
        'sidebar': 'audit_logs'
    }
    
    return render(request, 'audit_logs/audit_logs.html', context)