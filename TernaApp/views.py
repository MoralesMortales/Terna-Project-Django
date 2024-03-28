from django.shortcuts import render
from django.views.generic import TemplateView
from django.conf import settings
from django.core.mail import send_mail
# Create your views here.


class BasePage(TemplateView):
    template_name = "base.html"



class FormularioEmail(TemplateView):
    template_name = "formularioContacto.html"

def contactar(request):
    if request.method == "POST":
        asunto = request.POST["reason_email"]
        mensaje = request.POST["theMessage"] + "/ Email: " + request.POST["theEmail"]
        email_de = settings.EMAIL_HOST_USER
        email_para = ["pancitosdelhorno@gmail.com"]
        send_mail(asunto, mensaje, email_de, email_para ,fail_silently=False)
        return render(request, "contactadoExitosamente.html")
    return render(request, "formularioContacto.html")
    