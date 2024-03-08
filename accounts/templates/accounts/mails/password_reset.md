Hallo {{ user.first_name }},

du hast kürzlich einen Link zum Zurücksetzen deines Passworts angefordert.

[Neues Passwort festlegen]({{ action_url }})

Falls du das Zurücksetzen deines Passworts nicht angefordert hast, kannst du
diese E-Mail getrost ignorieren.

Solltest du Bedenken in Bezug auf die Sicherheit deines Kontos haben, kannst du
dich an die Organisatoren der diesjährigen Fachschaftentagung Maschinenbau
wenden.

[Support kontaktieren](mailto:{{ the_congress.support_email }})

Viele Grüße  
{{ the_congress.support_team }}

{% include "fatama/mails/signature.md" %}
