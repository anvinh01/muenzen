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
        <h2><a href="#planning">Planung</a></h2>
        <ol>
            <li><a href="#tech-stack">Techstack</a></li>
            <li><a href="#diagramme">Diagramme</a></li>
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

<h2> User-Kriterien </h2>
Um die Ziele klarer zu definieren, wird niedergeschrieben welche Interaktionen 
der User mit unserer Web-Applikation machen soll.

Der User soll ...

- ... durch einen Text aufgeklärt werden, was seine/ihre Aufgabe ist
- ... in der Lage sein, zwischen einen Münzwurf von 8 und 10 auszusuchen
- ... zwischen Kopf oder Zahl aussuchen können
- ... sehen können, welche Entscheidungen er vorher getroffen hat.
- ... am Ende der Entscheidungen diese an den Server schicken können.
- ... die Statistiken von dem Münzwurf der anderen Schüler sehen sollen.

<h2 id="requirements">Anforderungen</h2>
Unsere Website soll folgende Anforderungen vom Kunden mindestens erfüllen:

- [x] Schüler/innen können interaktiv Münzen werfen (8-, 10-, 20-Mal, ...).
- [x] Der Code soll Flexibel gehalten werden, damit andere Teams in Zukunft daran weiter arbeiten können.
- [x] Die Statistiken von den Münzwürfen sollen analysiert.
  - [x] Anzahl an geworfenen Kopf und Zahl
  - [x] Mittelwert an Kopf und Zahl
  - [x] Maximal aufeinander folgende Würfe
- [ ] Der Prozess soll interessant und spaßig gestaltet werden.
- [x] Die Webseite soll auf einer URL erreichbar sein.

<hr>
<h1 id="set-up">Set Up</h1>
<h2 id="docker">Docker</h2>
Wir haben eine Docker-compose erstellt, welches eine das Frontend und Backend mit Nginx aufsetzt.
Es ist möglich eine Entwicklungsumgebung aufzusetzen, indem Sie in der Commandline diesen Befehl eingeben:

```
docker-compose -f docker-compose.yml -p muenzen up -d
```

<hr>
<h1 id="planning">Planung</h1>
<h2 id="tech-stack">Techstack</h2>

Durch den kleinen Umfang der Applikation wird eine schnelle und minimale API benötigt.
Diese API muss keine User-Authentifizierung durchführen und nur in der lage sein, ein
POST request der Daten anzunehmen und ein GET für Request der Statistik zu verarbeiten.

Der Hauptfokus der Applikation soll die Verarbeitung der gesammelten Daten sein, weshalb
mathematische Funktionen vom Vorteil sind. Unsere Auswahl für die Technologien wird Python mit folgenden Modulen sein.

<h3 id="python"> Python </h3>
Python ist eines der meist benutzen Programmiersprachen laut einer 
[Stackoverflow Survey 2023](https://survey.stackoverflow.co/2023/#technology-most-popular-technologies).
Die Ruhr-Universität-Bochum bietet eine große Auswahl an Modulen an, in welchen die Studenten 
diese Programmiersprache erlernen und einsetzen, um Daten zu verarbeiten, wodurch die Einarbeitung in Python 
schneller möglich ist.

Zudem ist Python auch eine bekannte Sprache, die in vielen Fällen für das Backend development von Web-Applikationen
benutzt wird.

<h3 id="fast-api"> Fast-API </h3>
[Fast-API](https://fastapi.tiangolo.com) ist ein lightweight Web Framework für Rest-API Development. Es ist bekannt für die
antwort geschwindigkeit der APIs, welches so schnell ist wie NodeJS oder GO. Dabei ist die Einarbeitung Zeit
und Development Zeit für kleine Projekte sehr schnell, weshalb es für unser Projekt sehr geeignet ist, da unser
Projekt aus 2 API schnittstellen besteht und nicht weiter skalieren muss.

<h3 id="sql-lite"> SQL Lite / SQL-Alchemy </h3>
Durch die Verwendung von SQL-Alchemy und einer relationalen Datenbank (SQL Lite) werden die gesammelten Daten gespeichert.
Obwohl es eine Relationale Datenbank ist, werden keine Relationen Existieren. 

<h3 id="pytest"> Pytest / Coverage.py </h3>
Zum testen haben wir Pytest benutzt, welches das Testen von FastAPI unterstützt. Zudem verwenden wir 
Coverage.py, um einzusehen wie viel Prozent unserer Anwendung wir bereits getestet haben.

<h2 id="diagramme"> Diagramme</h2>
Es wird eine Single Page Applikation erstellt, welches die Kriterien vom User-flow Diagramm erfüllen soll. 
Ein Mockup liegt bereits in Figma vor.

<h3 id="user-flow">User-flow diagramme</h3>
![Sequenz](/Docs/Frontend%20Sequenz%20Diagramm.png)
<h3 id="design">Design Mockups</h3>

Das Design sollte ein Papier gefühl liefern und relativ minimal sein, damit sich die Schüler darauf fokussieren können

<h4 id="design"> Hero Sektion</h4>

![Here-section](/Docs/design/hero_section.png)

<h4 id="design"> About-us Sektion</h4>

![About-us-section](/Docs/design/about_us_section.png)

<h4 id="design"> Münzwurf Sektion</h4>

![münzwurf-1-section](/Docs/design/Münzwurf-1.png)
![münzwurf-2-section](/Docs/design/Münzwurf-2.png)
![münzwurf-3-section](/Docs/design/Münzwurf-3.png)






