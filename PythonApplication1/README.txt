# Nazwa programu: CoordinatesTree v2.0 
# J�zyk programowania: Python
# Autorzy: Sebastian Bogiel, Arkadiusz Walkowiak
# Uczelnia: Politechnika Pozna�ska
# Wydzia�: Elektryczny
# Kierunek: Automatyka i Robotyka, studia stacjonarne II stopnia
# Specjalizacja: Robotyka
# Przedmiot: Roboty autonomiczne (laboratorium)
# Prowadz�cy: mgr Jan Wietrzykowski

# 1. Cel dzia�ania programu

Celem dzia�ania programu jest analiza drzewa zale�no�ci. Drzewo to zawieraja zale�ne od siebie uk�ady wsp�rz�dnych.
Wynikiem dzia�ania programu jest lista uk�ad�w wsp�rz�dnych, kt�rych przekszta�cenie jest zale�ne od g��wnego uk�adu wsp�rz�dnych o przekszta�ceniu jednostkowym.

# 2. Dane wej�ciowe - opis

Program wymaga dostarczenia danych wej�ciowych w postaci pliku .YAML. Ka�dy rekord danych opisuje jeden uk�ad wsp�rz�dnych i zawiera nast�puj�ce pola:

	Name - nazwa uk�adu wsp�rz�dnych (string)
	Master - nazwa uk�adu nadrz�dnego dla danego uk�adu. Przez uk�ad nadrz�dny rozumie si� uk�ad o jeden stopie� wy�ej w strukturze drzewa.(string)
	Inverted - okre�la czy dane przekszta�cenie jest realizowane w kierunku od uk�adu nadrz�dnego do podrz�dnego (Inverted: 0) czy odwrotnie (Inverted: 1)
	Position - okre�la przesuni�cie uk�adu wzgl�dem uk�adu nadrz�dnego. Sk�ada si� z trzech element�w - kolejno - przesuni�cia w osi X,Y i Z.
	Orientation - okre�la orientacj� uk�adu wzgl�dem uk�adu nadrz�dnego. Wyra�any jest w formie kwaternionu. Znaczenie kolejnych warto�ci nale�y rozumie� jako kolejno:
				skalar, obr�t w osi X, Y i Z.

Z dok�adn� struktur� pliku danych wej�ciowych mo�na zapozna� si� po otwarciu pliku dane.yaml, kt�ry jest dostarczony do repozytorium.


# 3. Dane wej�ciowe - wymagania

Dane w pliku wej�ciowym wprowadzane s� w formie listy. Ka�dy uk�ad jest traktowany jako element tej�e listy. Nag��wek ka�dego uk�adu powinien mie� form�: - LinkX:
gdzie X to kolejny numer uk�adu. Wa�ne jest, aby numer ten by� unikalny! 

Nale�y tak�e pami�ta� o tym, �e dany zestaw danych wej�ciowych mo�e mie� tylko jeden g��wny uk�ad wsp�rz�dnych. Uk�ad taki oznacza si� pozostawiaj�c pole "Master" jako puste.
Wa�n� rzecz� jest te� aby uk�ad g��wny (bazowy) posiada� translacj� w postaci wektora zerowego, oraz rotacj� w postaci kwaternionu 1 + 0i + 0j + 0k.


# 4. Uruchamianie programu

Program uruchamiany jest z wiersza polece�. Nale�y go uruchomi�, przej�� do katalogu w kt�rym znajduje si� pobrany program, a nast�pnie wywo�a� program poleceniem w nast�puj�cej formie:

 CoordinatesTree.py "sciezka_pliku_zrodlowego.yaml" "sciezka_pliku_docelowego.yaml". 

�cie�ki do plik�w mog� zosta� podane zar�wno w postaci adres�w wzgl�dnych jak i bezwzgl�dnych. Istotne jest jednak podanie rozszerzenia .yaml (opcjonalnie .YAML) na ko�cu nazwy.

# 5. Repozytorium GitHub

Program mo�na pobra� z repozytorium GitHub pod adresem: https://github.com/arek1402/CoordinatesTree


