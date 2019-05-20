# Nazwa programu: CoordinatesTree v2.0 
# Jêzyk programowania: Python
# Autorzy: Sebastian Bogiel, Arkadiusz Walkowiak
# Uczelnia: Politechnika Poznañska
# Wydzia³: Elektryczny
# Kierunek: Automatyka i Robotyka, studia stacjonarne II stopnia
# Specjalizacja: Robotyka
# Przedmiot: Roboty autonomiczne (laboratorium)
# Prowadz¹cy: mgr Jan Wietrzykowski

# 1. Cel dzia³ania programu

Celem dzia³ania programu jest analiza drzewa zale¿noœci. Drzewo to zawieraja zale¿ne od siebie uk³ady wspó³rzêdnych.
Wynikiem dzia³ania programu jest lista uk³adów wspó³rzêdnych, których przekszta³cenie jest zale¿ne od g³ównego uk³adu wspó³rzêdnych o przekszta³ceniu jednostkowym.

# 2. Dane wejœciowe - opis

Program wymaga dostarczenia danych wejœciowych w postaci pliku .YAML. Ka¿dy rekord danych opisuje jeden uk³ad wspó³rzêdnych i zawiera nastêpuj¹ce pola:

	Name - nazwa uk³adu wspó³rzêdnych (string)
	Master - nazwa uk³adu nadrzêdnego dla danego uk³adu. Przez uk³ad nadrzêdny rozumie siê uk³ad o jeden stopieñ wy¿ej w strukturze drzewa.(string)
	Inverted - okreœla czy dane przekszta³cenie jest realizowane w kierunku od uk³adu nadrzêdnego do podrzêdnego (Inverted: 0) czy odwrotnie (Inverted: 1)
	Position - okreœla przesuniêcie uk³adu wzglêdem uk³adu nadrzêdnego. Sk³ada siê z trzech elementów - kolejno - przesuniêcia w osi X,Y i Z.
	Orientation - okreœla orientacjê uk³adu wzglêdem uk³adu nadrzêdnego. Wyra¿any jest w formie kwaternionu. Znaczenie kolejnych wartoœci nale¿y rozumieæ jako kolejno:
				skalar, obrót w osi X, Y i Z.

Z dok³adn¹ strukturê pliku danych wejœciowych mo¿na zapoznaæ siê po otwarciu pliku dane.yaml, który jest dostarczony do repozytorium.


# 3. Dane wejœciowe - wymagania

Dane w pliku wejœciowym wprowadzane s¹ w formie listy. Ka¿dy uk³ad jest traktowany jako element tej¿e listy. Nag³ówek ka¿dego uk³adu powinien mieæ formê: - LinkX:
gdzie X to kolejny numer uk³adu. Wa¿ne jest, aby numer ten by³ unikalny! 

Nale¿y tak¿e pamiêtaæ o tym, ¿e dany zestaw danych wejœciowych mo¿e mieæ tylko jeden g³ówny uk³ad wspó³rzêdnych. Uk³ad taki oznacza siê pozostawiaj¹c pole "Master" jako puste.
Wa¿n¹ rzecz¹ jest te¿ aby uk³ad g³ówny (bazowy) posiada³ translacjê w postaci wektora zerowego, oraz rotacjê w postaci kwaternionu 1 + 0i + 0j + 0k.


# 4. Uruchamianie programu

Program uruchamiany jest z wiersza poleceñ. Nale¿y go uruchomiæ, przejœæ do katalogu w którym znajduje siê pobrany program, a nastêpnie wywo³aæ program poleceniem w nastêpuj¹cej formie:

 CoordinatesTree.py "sciezka_pliku_zrodlowego.yaml" "sciezka_pliku_docelowego.yaml". 

Œcie¿ki do plików mog¹ zostaæ podane zarówno w postaci adresów wzglêdnych jak i bezwzglêdnych. Istotne jest jednak podanie rozszerzenia .yaml (opcjonalnie .YAML) na koñcu nazwy.

# 5. Repozytorium GitHub

Program mo¿na pobraæ z repozytorium GitHub pod adresem: https://github.com/arek1402/CoordinatesTree


