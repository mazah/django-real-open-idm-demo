from django.shortcuts import render
from django.urls import reverse
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from djangorealidm.models import Grant
from river.models import State
from django.template import loader
from django.contrib.auth.decorators import login_required
import csv


@login_required(login_url='/admin/login/')
def approve_ticket(request, grant_id, next_state_id=None):
    ticket = get_object_or_404(Grant, pk=grant_id)
    next_state = get_object_or_404(State, pk=next_state_id)

    try:
        ticket.river.status.approve(as_user=request.user, next_state=next_state)
        return redirect(reverse('admin:djangorealidm_grant_changelist'))
    except Exception as e:
        return HttpResponse(e.message)


@login_required(login_url='/admin/login/')
def reports(request):
    grant_list = Grant.objects.all()
    template = loader.get_template('djangorealidm/reports.html')
    grants = []
    for grant in grant_list:
        approver = None
        last_approved = None
        try:
            approver = grant.status_transition_approvals.filter(status='approved').order_by('-id')[0].transactioner.username
            last_approved = grant.status_transition_approvals.filter(status='approved').order_by('-id')[0].transaction_date
        except:
            pass
        grants.append({
            'approver': approver,
            'last_approved': last_approved,
            'grant': grant
        })

    context = {
        'grant_list': grants,
    }
    if request.GET.get("csv"):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

        writer = csv.writer(response)
        writer.writerow(['username', 'group', 'status', 'last_approval', 'transaction_date'])
        for grant in grant_list:
            try:
                approval = grant.status_transition_approvals.filter(status='approved').order_by('-id')[0]
                approval_username = approval.transactioner.username
                last_approved = approval.transaction_date
            except:
                approval_username = None
                last_approved = None
            writer.writerow([grant.user.username, grant.group.name, grant.status.slug, approval_username, last_approved])

        return response
    else:
        return HttpResponse(template.render(context, request))

