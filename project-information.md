
# Münzen Werfen

## Beschreibung

Die Web-Applikation soll Schülern einen besseren Einblick in die Statistik eines
Münzwurfes verschaffen. Durch das Interaktive wählen und Schätzen der nächsten Münze,
wird eine Statistik, aus den gewählten Schätzungen der Schüler erstellt und visuell dargestellt.

## User-Kriterien
Um die Ziele klarer zu definieren, wird niedergeschrieben welche Interaktionen 
der User mit unserer Web-Applikation machen soll.

Der User soll ...
- ... durch einen Text aufgeklärt werden, was seine/ihre Aufgabe ist
- ... in der Lage sein, zwischen einen Münzwurf von 8 und 10 auszusuchen
- ... zwischen Kopf oder Zahl aussuchen können
- ... sehen können, welche Entscheidungen er vorher getroffen hat.
- ... am Ende der Entscheidungen diese an den Server schicken können.
- ... die Statistiken von dem Münzwurf der anderen Schüler sehen sollen.

![User-flow Diagramm](/Docs/Userflow-diagram.svg)
Der Benutzer hat einen gradlinigen Ablauf.

# Backend Dataflow
Durch den kleinen Umfang der Applikation wird eine schnelle und minimale API benötigt. 
Diese API muss keine User-Authentifizierung durchführen und nur in der lage sein, ein 
POST request der Daten anzunehmen und ein GET für Request der Statistik zu verarbeiten.

Der Hauptfokus der Applikation soll die Verarbeitung der gesammelten Daten sein, weshalb
mathematische Funktionen vom Vorteil sind. Unsere Auswahl für die Technologien wird Python mit folgenden Modulen sein.

## Python
Python ist eines der meist benutzen Programmiersprachen laut einer 
[Stackoverflow Survey 2023](https://survey.stackoverflow.co/2023/#technology-most-popular-technologies).
Die Ruhr-Universität-Bochum bietet eine große Auswahl an Modulen an, in welchen die Studenten 
diese Programmiersprache erlernen und einsetzen, um Daten zu verarbeiten, wodurch die Einarbeitung in Python 
schneller möglich ist.

Zudem ist Python auch eine bekannte Sprache, die in vielen Fällen für das Backend development von Web-Applikationen 
benutzt wird. 

## Fast-API
[Fast-API](https://fastapi.tiangolo.com) ist ein lightweight Web Framework für Rest-API Development. Es ist bekannt für die
antwort geschwindigkeit der APIs, welches so schnell ist wie NodeJS oder GO. Dabei ist die Einarbeitung Zeit
und Development Zeit für kleine Projekte sehr schnell, weshalb es für unser Projekt sehr geeignet ist, da unser
Projekt aus 2 API schnittstellen besteht und nicht weiter skalieren muss.

## SQL Lite
Durch die Verwendung von SQL-Alchemy und einer relationalen Datenbank (SQL Lite) werden die gesammelten Daten gespeichert.
Obwohl es eine Relationale Datenbank ist, werden keine Relationen Existieren. 

# Frontend UI
Es wird eine Single Page Applikation erstellt, welches die Kriterien vom User-flow Diagramm erfüllen soll. 
Ein Mockup liegt bereits in Figma vor.

## User-flow diagramm
![Sequenz](/Docs/Frontend%20Sequenz%20Diagramm.png)

## Design Mockups

Das Design sollte ein Papier gefühl liefern und relativ minimal sein, damit sich die Schüler darauf fokussieren können

### Hero Sektion

![Here-section](/Docs/design/hero_section.png)

### About-us Sektion

![About-us-section](/Docs/design/about_us_section.png)

### Münzwurf Sektion

![münzwurf-1-section](/Docs/design/Münzwurf-1.png)
![münzwurf-2-section](/Docs/design/Münzwurf-2.png)
![münzwurf-3-section](/Docs/design/Münzwurf-3.png)






