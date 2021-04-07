from django.shortcuts import render
from django.urls import reverse
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from djangorealidm.models import Grant
from river.models import State

def approve_ticket(request, grant_id, next_state_id=None):
    ticket = get_object_or_404(Grant, pk=grant_id)
    next_state = get_object_or_404(State, pk=next_state_id)

    try:
        ticket.river.status.approve(as_user=request.user, next_state=next_state)
        return redirect(reverse('admin:djangorealidm_grant_changelist'))
    except Exception as e:
        return HttpResponse(e.message)
