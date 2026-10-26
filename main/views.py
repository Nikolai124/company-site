import time

from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import LeadForm
from .models import Faq, Review, Service
from .telegram import notify_new_lead

# Не чаще одной заявки в минуту с одной сессии
LEAD_COOLDOWN_SECONDS = 60


def index(request):
    if request.method == "POST":
        form = LeadForm(request.POST)
        if form.is_valid():
            last_sent = request.session.get("last_lead_at", 0)
            if form.is_spam():
                pass  # делаем вид, что всё ок, но ничего не сохраняем
            elif time.time() - last_sent < LEAD_COOLDOWN_SECONDS:
                messages.warning(request, "Вы уже отправили заявку. Мы скоро перезвоним!")
                return redirect("/#contact")
            else:
                lead = form.save()
                request.session["last_lead_at"] = time.time()
                notify_new_lead(lead)
            messages.success(request, "Спасибо! Перезвоним в течение 15 минут в рабочее время.")
            # Редирект после POST, чтобы F5 не отправлял форму повторно
            return redirect("/#contact")
    else:
        form = LeadForm()

    context = {
        "services": Service.objects.filter(is_active=True),
        "reviews": Review.objects.filter(is_published=True)[:3],
        "faqs": Faq.objects.all(),
        "form": form,
    }
    return render(request, "main/index.html", context)


def privacy(request):
    return render(request, "main/privacy.html")


def consent(request):
    return render(request, "main/consent.html")
