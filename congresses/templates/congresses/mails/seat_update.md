Hallo {{ recipient }},

die Teilnehmerplätze deines Gremiums **{{ attendance.council }}** für die
Anmeldung zur Tagung **{{ attendance.congress }}** wurden aktualisiert.

Dein Gremium hat nun insgesamt **{{ seats.total }}**
{% if seats.total == 1 %}Platz{% else %}Plätze{% endif %}. Du kannst davon noch
**{{ seats.free }}** {% if seats.free == 1 %}Platz{% else %}Plätze{% endif %}
zur Anmeldung weiterer Teilnehmer nutzen.
{% if seats.free > 0 %}
[Teilnehmer anmelden]({{ action_url }})
{% elif seats.total > 0 %}
[Teilnehmer anzeigen]({{ action_url }})
{% endif %}
Viele Grüße  
{{ the_congress.support_team }}

{% include "fatama/mails/signature.md" %}
