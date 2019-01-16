# Technisch ontwerp

# Controllers;

De website begint op de Login-pagina ( def login( ) ). Hier krijgt de gebruiker de mogelijkheid om in te loggen op de website door het invoeren van de gebruikersnaam en het wachtwoord gekoppeld aan die gebruikersnaam. Er is een link onder de input van wachtwoord die een route geeft naar de register-pagina ( def register( ) ) en een link die redirect naar een pagina voor wachtwoord vergeten. Deze pagina geeft een POST-request zodra er een bestaande input gegeven is en redirect de gebruiker dan naar de homepage.

De pagina van wachtwoord vergeten ( def forgot( ), POST) krijg je een input te zien om een je gebruikersnaam in te vullen en je e-mail adres. Je krijgt dan een mail met een link naar een andere pagina ( def change( ), POST) waarin je je username moet invullen, een code die je toegestuurd krijgt, een nieuw wachtwoord en je nieuwe wachtwoord nog een keer ter controle.

Op de register-pagina kan de gebruiker een account aanmaken door een gebruikersnaam in te vullen, een wachtwoord in te vullen en dit wachtwoord nogmaals te herhalen in een confirm password-input. Ook moet er een e-mail adres ingevoerd worden. Zodra er een valide input gegeven is, redirect deze pagina via een POST-request de gebruiker naar de homepage. 

Op de homepagina(Dit is all games)erschijnt er een navigatiebar die meerdere links bevat;
All Games ( def allgames( ) , GET ) Op deze pagina krijgt de user al de games te zien die de gebruiker bezit. 

Completed games ( def completed( ), GET ) Op deze pagina krijgt de gebruikers de games te zien die de gebruiker uit heeft gespeeld. 
Currently playing ( def currently( ), GET ) Op deze pagina krijgt de gebruiker de games te zien waar de gebruiker mee bezig is ( niet op het moment zelf, gewoon de games die de gebruikers nog niet uit heeft gespeeld ). 
Games on hold ( def onhold( ), GET ) Op deze pagina krijgt de gebruiker de games te zien waar de gebruiker verder mee wilt gaan, maar even mee gestopt is. 
Dropped ( def dropped( ), GET ) Op deze pagina krijgt de gebruiker de games te zien die de gebruiker helemaal niet meer speelt. 
Wishlist ( def wishlist( ), GET ) Op deze pagina kan de gebruiker games toevoegen die de gebruiker nog wilt spelen, maar op het moment niet bezit.

Op elke pagina die niet de homepage is verschijnt er ook een link naar de homepage.
Op de homepage zelf ( def homepage( ) ) kan de gebruiker naar games zoeken uit de database, ens kan de gevonden game dan posten op een van de pagina’s uit de navigatiebar. De homepages is dus een POST ( voor het posten van de games op de gebruikers eigen account ) en een GET ( het ophalen van de games uit de database ) pagina.

Aan de rechterkant van de navigatiebar komt een knop met, met een klein dropdown menu waar de links naar user-settings ( def usersettings ( ), GET) komen te staan en een logout ( def logout( ), GET) knopt die redirect naar de login pagina. Hierin roepen we alle functie aan die de volgende opties mogelijk maken;
Het veranderen van:
	- De gebruikersnaam ( def changeuser( ), POST )
	- Het wachtwoord	( redirect naar def forgot( )
	- Het e-mailadres ( def changeemail( ), POST ) Ook is er de mogelijkheid om je account te verwijderen ( def delete( ), POST). 

# Models / helpers
Onze models voor de website zien er als volgt uit: https://drive.google.com/open?id=1LZcyfCxwPlxFBKRQibIETPpYN05O_lt3

In onze helpers.py moet in ieder geval staan:
	-  def login_required( ): Deze functie zorgt ervoor dat de gebruiker alleen bij de meeste delen van de website kan komen zodra de gebruiker is ingelogd.
	- def lookup(name): Deze functie kijkt of de game in de database staat. Deze functie returnt een lijst met dictionaries er in met alle waardes van de games. Dit zijn waardes als name, rating en andere.
	- def error(): deze functie returnt een error pagina als er iets fout gaat.
	
	- def checklogin(password, username): Deze functie checkt of de passwords en de username correct zijn. 
	Dit wordt in helpers.py gezet zodat we al onze opzoek verzoeken voor de database in een apparte file hebben.
	
	#Deze functie is nog niet zeker.
	-def makedatabaseuser(user_id): Deze functie maakt een nieuwe database waar de user al zijn games 
	in krijgt als een portfolio. Dit wordt individueel gedaan zodat de zoek snelheid van de user vergroot word.
	
	- def checkregister(username, password, repeat, email): Deze functie checkt of alles op de registreer 
	pagina goed is ingevuld.
	
	- def change(what, input, input_repeat): Deze functie checkt alle functies voor het veranderen van 
	gebruikers informatie
	
	- def forgotpassword(username, email): Verstruurd een automatische email waarin een code wordt gestuurd voor 
	de user zodat hij zijn wachtwoord kan resetten.
	
	-def changeforgotpassword(code, username, newpassword, repeatnewpassword): Deze functie kijkt of de code goed 
	ingevoerd is en zo of de passwords kloppen. Als de code fout is wordt er opnieuw een code aangemaakt en 
	mail verstuurd. (maximale mails moeten we nog even bekijken.)
