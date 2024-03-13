Hallo {{ recipient }},

dein Vorschlag für das Seminar **{{ workshop.title }}** wurde
{{ workshop.get_state_display|lower }}.

[Seminare anzeigen]({{ action_url }})

Viele Grüße  
{{ the_congress.support_team }}

{% include "fatama/mails/signature.md" %}
