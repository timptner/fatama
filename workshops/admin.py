import markdown

from django.contrib import admin
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse_lazy

from workshops.models import Workshop


@admin.register(Workshop)
class WorkshopAdmin(admin.ModelAdmin):
    list_display = ["title", "author"]
    list_filter = ["state", "congress__year", "author"]

    def save_form(self, request, form, change):
        if change and "state" in form.changed_data:
            scheme = "https" if request.is_secure() else "http"
            host = request.get_host()
            path = reverse_lazy("workshops:workshop_list")
            url = f"{scheme}://{host}{path}"

            workshop = form.instance
            context = {
                "recipient": workshop.author.first_name,
                "workshop": workshop,
                "action_url": url,
            }

            subject = "Status deines Vorschlags aktualisiert"

            text_content = render_to_string(
                "workshops/mails/state_update.md", context, request
            )
            html_content = markdown.markdown(text_content)

            mail = EmailMultiAlternatives(
                subject, text_content, None, [workshop.author.email]
            )
            mail.attach_alternative(html_content, "text/html")

            mail.send()
        return super().save_form(request, form, change)
