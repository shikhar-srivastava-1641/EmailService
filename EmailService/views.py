from django.shortcuts import render


def email_sender(request):
    show_alert = request.GET.get('alert_visible', False)
    success = request.GET.get('success', False)
    return render(request, 'email.html', {"show_alert": show_alert, "success": success})
