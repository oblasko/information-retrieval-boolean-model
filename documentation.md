# BI-VWM Dokumentácia ku semestrálne projektu - boolovský model
Blaško Oliver (blaskoli)

## Popis projektu
Cieľom tejto práce bolo implementovať teoretický boolovský model domény získavania informácií  (information retrieval). Jeho úlohou je pre zadaný boolovský dotaz, vyhladať vyhovujúce dokumenty v statickej kolekcii textov. Dotaz je tvorený boolovským výrazom, ktorý sa skladá z termov (slov) spojených logickými spojkami AND, OR, NOT. Boolovský model vracia dokumenty vyhovujúce tomuto dotazu, poprípade informuje o tom že žiadny dokument dotazu nevyhovuje alebo, že zadaný dotaz nebol validný.

## Riešenie
### Dataset
V prvom rade bolo potrebné vytvoriť kolekciu dokumentov v ktorej bude užívateľ vyhladávať. Rozhodol som sa použiť NLTK Gutenberg corpus, ktorý obsahuje 18 textov - známych literálnych diel z elektronického archívu Project Gutenberg.

### Predzpracovanie
Následne bolo potrebné túto kolekciu predpripraviť. Ako prvé sme zo všetkých textov vytvorili slovník slov (všetky rôzne slová, ktoré sa v daných textoch nachádzajú, každé max. 1x). Zo slovníka boli odstránené tzv. stop words - nevýznámové slová (v texte sa nachádzajú s vysokou frekvenciou ako napríklad spojky, predložky) pomocou balíčka `nltk.corpus`. Po odstránení stopwords sme na významových slovách pomocou balíčka `nltk.stem` aplikovali proces stematizácie a teda nájdenie koreňa slova čím sa opať znížil počet významových slov, kedže týmto procesom sa podobné slová zredukujú len na spoločný koreň.

### Invertovaný index
Po príprave dát sme vytvorili vyhľadaváciu štruktúru - invertovaný index. Invertovaný index je kompaktná reprezentácia term-by-document matice (kde na i-tom riadku v j-tom stĺpci je 1 práve vtedy ak je term i obsiahnutý v dokumente j). Invertovaný index je štruktúra, ktorá pre každý term ukladá vzostupne usporiadaný list, ktorý obsahuje identifkátory všetkých dokumentov v ktorých sa daný term nachádza. Pre implementáciu sme použili 2 Python slovníky, kde v prvom sú namapované termy (kľúče slovníka) ku spojovému zoznamu identifikátorov (vlastná implementácia) a v druhom sú namapované identifikátory (kľúče slovníka) ku názvom daných dokumentov(súborov). Konkrétnu implementáciu možno vidieť v balíčku `information_retrieval`.

### Sekvenčný prechod
Pre porovnanie sme implementovali aj triviálny sekvenčný prechod kolekciou, ktorý hľadá daný výraz prechodom cez všetky texty kolekcie word-by-word. Implementáciu možno pozorovať v balíčku `evaluator`, metóda `sequence_find`.

### Spracovanie boolovského dotazu
Pre ovorenie validity boolovského dotazu sme použili knihovňu `PyEDA`,  konkrétne balíčku pre operácie s boolovskou algebrou: `pyeda.boolalg.expr`. Na parsovanie a vyhodnotenie sme použili vlastnú implementáciu, ktorá si najprv usporiada boolovské operácie podľa priority a následne daný výraz reťazovo vyhodnotí. Výstupom tohto spracovania je buď prázdny list (žiadny vyhovujúci dokument) alebo list identifikátorov dokumentov, pre ktoré daný výraz platí. V poslednom rade sa ešte identifikátory zamenia za názvy dokumentov pre užívateľa. Poznámka: termy obishanuté v dotaze boli pred vyhodnotením taktiež stemmatizované. Konkrétnu implementáciu a testy možno vidieť v balíčku `evaluator`.

### Aplikácia
Pre implementáciu GUI sme sa rozhodli použiť klient-server webovú aplikáciu, kde bude mať užívateľ možnosť pohodlne zadať daný boolovský dotaz a aplikácia mu vráti tabuľku vyhovujúcich dokumentov ako aj linky na raw formát daných dokumentov (pre kontrolu). Aplikácia taktiež bude vedieť skontrolovať validitu dotazu a prípadne informovať užívateľa o nevalidnom dotaze alebo v prípade, že pre daný dotaz nebol nájdeny žiadny vyhovujúci dokument.

#### Back-end 
Kedže logika aplikácie bola napísaná v Pythone, pre backend sme sa rozhodoli použiť Python webový framework Flask. Server s použitím balíčkov popsaných vyšie pre daný request vyhodnotí validitu dotazu a vracia buď informáciu že daný dotaz nebol validný alebo tabuľku výsledkov. Konkrétnu implementáciu možno vidieť v balíčku `api`.

#### Front-end
Pre klient časť sme sa rozhodli použit javascriptový framework [ReactJs](https://reactjs.org/). Klient má na starosti prijatie dotazu od uživateľa, zaslanie requestu na server a následné zobrazenie odpovede (výsledkov) v prehliadači. Pre jednoduché nastavenie front-end pipeline sme použili [create-react-app](https://github.com/facebook/create-react-app). V poslednom rade bola pre krajšiu štylizáciu použitá knihovňa [react-bootstrap]([react-bootstrap](https://react-bootstrap.github.io/))




## Prehľad použitých technológií
#### Back-end 
- Python 3.7.4
- [NLTK](https://www.nltk.org/)
  - `nltk.corpus` pre vytvorenie korpusu, odstránenie stopwords
  - `nltk.stem` pre stematizáciu
- [PyEda](https://pypi.org/project/pyeda/) - validácia dotazu
- [Flask](https://flask.palletsprojects.com/en/2.0.x/) - API

#### Front-end
- [ReactJs](https://reactjs.org/) - front-end framework
- [create-react-app](https://github.com/facebook/create-react-app) - konfigurácia 
- [react-bootstrap]([react-bootstrap](https://react-bootstrap.github.io/)) - štylizácia

## Inštalačná príručka
### Základné požiadavky
- Python 3
- [nodeJS](https://nodejs.org/en/)

### Inštalácia

## Output example

## Experimenty
Pre otestovanie a porovnanie rýhlosti indexu sme sa rozhodli porovnať čas odozvy indexu voči trivialnému sekvenčnému prechodu pre zadaný dotaz. 

| Dotaz      | Index | Sekvenčný prechod     |
| :---        |    :----:   |          ---: |
| horse     | 0.27 ms     | 8.25 ms   |
| NOT horse   | 0.35 ms       | 7.89 ms      |
| death and love  | 0.39 ms       | 8.25 ms      |
| murder OR god OR shakespear   | 0.49 ms       | 67.93 ms      |
| (Goddard AND god) OR NOT Exeunt  | 0.51 ms       | 83.99 ms      |
| (Goddard AND god) AND NOT Exeunt AND (death AND love)   | 0.68 ms       | 95.94 ms      |

Ako môžme vidieť v tabuľke vyššie invertovaný index je viacnásobne rychlejší ako triviálny prechod. Zaujimavé taktiež je to, že pri rastúcej náročnosti dotazu oba spôsoby prehladávania rastú, ale pri indexe nárast času odozvy nie je až taký výrazný ako pri triviálnom prechode.
## Discussion

## Conclusion

