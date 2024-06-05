# Münzen-Projekt
Das Ziel vom Projekt wird es eine Website zu erstellen, die den Lehrern dabei behilflich sein kann die Statistiken vom Münzwurf zu erklären.
[Zur Website](https://muenzen.tyfn.de)
<hr>

# Inhaltsverzeichnis

<ol>
    <li style="list-style: none">
        <h2><a href="#project-description">Projekt beschreibung</a></h2>
        <ol>
            <li><a href="#description">Beschreibung</a></li>
            <li><a href="#requirements">Anforderungen</a></li>
        </ol>
    </li>
    <li style="list-style: none">
        <h2><a href="#set-up">Set Up</a></h2>
        <ol>
            <li><a href="#docker">Docker</a></li>
            <li><a href="">Lokal</a></li>
            <li><a href="">Makefile</a></li>
        </ol>
    </li>
    <li style="list-style: none">
        <h2><a href="">Planung</a></h2>
        <ol>
            <li><a href="">Techstack</a></li>
            <li><a href="">Diagramme</a></li>
            <li><a href="">Struktur</a></li>
        </ol>
    </li>
</ol>

<hr>
<h1 id="project-description">Projekt beschreibung</h1>
<h2 id="description">Beschreibung</h2>
Die Web-Applikation soll Schülern einen besseren Einblick in die Statistik eines
Münzwurfes verschaffen. Durch das Interaktive wählen und Schätzen der nächsten Münze,
wird eine Statistik, aus den gewählten Schätzungen der Schüler erstellt und visuell dargestellt.
Diese Daten werden dann auf folgende Metriken untersucht:

- Anzahl an Kopf und Zahl
- Mittelwert an Kopf und Zahl pro Wurf
- Anzahl an aufeinander folgende Würfe
- etc.

<h2 id="requirements">Anforderungen</h2>
Unsere Website soll folgende Anforderungen vom Kunden mindestens erfüllen:

- [x] Schüler/innen können interaktiv Münzen werfen (8-, 10-, 20-Mal, ...).
- [x] Der Code soll Flexibel gehalten werden, damit andere Teams in Zukunft daran weiter arbeiten können.
- [x] Die Statistiken von den Münzwürfen sollen analysiert.
  - [x] Anzahl an geworfenen Kopf und Zahl
  - [x] Mittelwert an Kopf und Zahl
  - [x] Maximal aufeinander folgende Würfe
- [ ] Der Prozess soll interessant und spaßig gestaltet werden.
- [ ] Die Webseite soll auf einer URL erreichbar sein.

<hr>
<h1 id="set-up">Set Up</h1>
<h2 id="docker">Docker</h2>
Wir haben eine Docker-compose erstellt, welches eine das Frontend und Backend mit Nginx aufsetzt.
Es ist möglich eine Entwicklungsumgebung aufzusetzen, indem Sie in der Commandline diesen Befehl eingeben:

```
docker-compose -f docker-compose.yml -p muenzen up -d
```






