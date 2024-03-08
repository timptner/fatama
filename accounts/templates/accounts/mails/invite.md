# Sei gegrüßt!

Du wurdest von {{ sender }} eingeladen, ein Konto für die
[FaTaMa {{ the_congress.year }}](https://www.fatama2024.de) zu erstellen.

[Konto erstellen]({{ action_url }})

Der Link kann zur **einmaligen** Registrierung verwendet werden und ist bis zum
{{ expired_at|date:"d.m.Y" }} um {{ expired_at|time:"H:i:s" }} Uhr
({{ expired_at|date:"T" }}) gültig.

Wenn du Fragen zur Registrierung hast, kannst du dich jederzeit an die
Organisatoren der diesjährigen Fachschaftentagung Maschinenbau wenden.

[Support kontaktieren](mailto:{{ the_congress.support_email }})

Viele Grüße  
{{ the_congress.support_team }}

{% include "fatama/mails/signature.md" %}
