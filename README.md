# In-Matica
Opdracht: Collectionneur

# Studenten:
Carlos Tjoe Nij 	  	12394467
Matthijs Zwemmer 	12074829
Tim Schouten 		12329142

# Samenvatting
Wij gaan een site maken waarbij je je volledige bibliotheek van games kan opslaan en sorteren zodat je een beter overzicht krijgt wat je allemaal aan games bezit en wat je nog niet en wel al gespeeld hebt. Wat onze web applicatie uniek maakt is dat de gebruiker kan uitsorteren wat hij/zij al gespeeld heeft en wat nog niet binnen zijn eigen collectie. Dit geeft de gebruiker veel inzicht in zijn bibliotheek, want tegenwoordig zijn er veel verschillende distributieplatformen die allemaal niet goed samenwerken en de gebruiker geen overzicht meer houd.

# Screenshot
https://drive.google.com/open?id=1PE0XpjZBI_ig9Iva6yK5tweieilO_ETK

# Features
* Toegang tot een database(kunnen zoeken op games).
* De mogelijkheid om games op te zoeken.
* De mogelijkheid om een profiel aan te maken en in te loggen.
* De mogelijkheid om games op te slaan op je profiel.
* De mogelijkheid om games te sturen naar mensen als tips.
* De mogelijkheid om games uit te sorteren op 5 categorieën(currently playing, on hold, dropped, completed, wishlist)
* De mogelijkheid om je wachtwoord, username en email te veranderen.
* De mogelijkheid om games een cijfer te geven.
* De mogelijkheid om in de tabellen te sorteren op rating, op alfabetische volgorde en op datum/ tijdstip van toevoeging.
* De mogelijkheid om je account te verwijderen
* De mogelijkheid om andere mensen hun profiel te bekijken.
* De mogelijkheid om de status en persoonlijke rating van games te veranderen die je al in je bibliotheek staan

# Taakverdeling
Wij hebben het grootste gedeelte samen gedaan, waarbij iedereen wel aan alle delen van de site heeft gewerkt. Grofweg heeft Tim het meeste gedaan aan de css, Matthijs aan helpers.py en Carlos het meest aan application.py. De rest van de formatting ging in gezamenlijk overleg.

# Onderdelen
In onze repository vind je in de hoofdmap WebprogIK nog twee andere mappen;
	1. Static/: hierin staan alle visuele aspecten zoals de css file 				en alle afbeeldingen die zijn gebruikt in de website.
	2. templates/: hierin staan alle html files die zich bevinden in 			de website. 

Naast deze mappen staan er nog een aantal losse files in onze hoofdmap:

	1. Application.py: hierin staat alle code die nodig is voor het functioneren van de website. Alle POST en GET items zijn hier te vinden en de manier waarop alle html files aan elkaar zijn gelinkt.

	2. Helpers.py: hierin staan alle onderdelen die te maken hebben met de database. Met deze map worden alle links gelegd tussen de website en alle op te halen informatie uit de database met alle gebruikersinfo. Ook staat hier de functie in waarmee je toegang hebt tot de database met alle games waarop onze website gebaseerd is.

	3. Games.db: dit is de database met alle gebruikersinformatie in SQL format. Hierin bevinden zich ook de variërende informatie die een gebruiker kan aanpassen zoals de persoonlijke rating per game.
