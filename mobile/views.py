from django.shortcuts import render
from django.shortcuts import redirect
import re

MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)


def mobile(request):
    context = {}
    if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
        return redirect('now')
    else:
        return render(request, 'mobile/mobile.html', context)
