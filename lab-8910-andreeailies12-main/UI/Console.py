import datetime
import time

from Service.cardClientService import CardClientService
from Service.filmService import FilmService
from Service.rezervareService import RezervareService
from Service.undoRedoService import UndoRedoService


class Consola:
    def __init__(self, filmService: FilmService,
                 cardClientService: CardClientService,
                 rezervareService: RezervareService,
                 undoRedoService: UndoRedoService):

        self.__filmService = filmService
        self.__cardClientService = cardClientService
        self.__rezervareService = rezervareService
        self.__undoRedoService = undoRedoService

    def run_menu(self):
        while True:
            print("1. CRUD  filme")
            print("2. CRUD  card client")
            print("3. CRUD  rezervare")
            print("4. Sa se genereze random n filme/carduri clienti")
            print("5. Afișarea filmelor ordonate descrescător "
                  "după numărul de rezervări")
            print("6. Afișarea cardurilor client ordonate "
                  "descrescător după numărul de puncte de pe card.")
            print("7. Afișarea tuturor rezervărilor dintr-un interval"
                  " de ore dat, indiferent de zi.")
            print("8. Ștergerea tuturor rezervărilor"
                  " dintr-un anumit interval de zile.")
            print("9. Incrementarea cu o valoare dată a punctelor de pe toate "
                  "cardurile a căror zi de naștere"
                  " se află într-un interval dat.")
            print("u. Undo")
            print("r. Redo")
            print("x. Iesire")
            optiune = input("Dati optiunea: ")

            if optiune == "1":
                self.run_crud_film_menu()
            elif optiune == "2":
                self.run_crud_card_client_menu()
            elif optiune == "3":
                self.run_crud_rezervare_menu()
            elif optiune == "4":
                self.generare()
            elif optiune == "5":
                self.afiseaza(self.__rezervareService.filme_desc_nr_rezervari()
                              )
            elif optiune == "6":
                self.ui_ordoneaza_card_client()
            elif optiune == "7":
                self.ui_afisare_rezervari_ore()
            elif optiune == "8":
                self.ui_stergere_rezervari()
            elif optiune == "9":
                self.ui_incrementarea_cardurilor()
            elif optiune == "u":
                self.__undoRedoService.undo()
            elif optiune == "r":
                self.__undoRedoService.redo()

            elif optiune == "x":
                break
            else:
                print("Optiune gresita! Reincercati!")

    def afiseaza(self, entitati):
        for entitate in entitati:
            print(entitate)

    def run_crud_film_menu(self):
        while True:
            print("1. Adauga film")
            print("2. Sterge film")
            print("3. Modifica film")
            print("4. Cautare filme full text")
            print("a. Afiseaza toate filmele")
            print("x. Iesire")
            optiune = input("Dati optiunea: ")

            if optiune == "1":
                self.ui_adauga_film()
            elif optiune == "2":
                self.ui_sterge_film()
            elif optiune == "3":
                self.ui_modifica_film()
            elif optiune == "4":
                a = input("Dati un parametru dupa care"
                          " sa fie realizata cautarea filmelor: ")
                self.ui_cautare_full_text_filme(a)
            elif optiune == "a":
                self.show_all_film()
            elif optiune == "x":
                break
            else:
                print("Optiune gresita! Reincercati!")

    def ui_adauga_film(self):
        try:
            id_film = input("Dati id ul filmului: ")
            titlu = input("Dati titlul filmului: ")
            an_aparitie = int(input("Dati anul aparitiei filmului: "))
            pret_bilet = float(input("Dati pretul biletului pentru film."
                                     "Acesta trebuie sa fie un nr pozitiv: "))
            in_program = input("Dati confirmarea daca "
                               "filmul este in program(da sau nu): ")

            self.__filmService.adauga(id_film,
                                      titlu,
                                      an_aparitie,
                                      pret_bilet,
                                      in_program)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def ui_sterge_film(self):
        try:
            id_film = input("Dati id ul filmului de sters: ")

            self.__filmService.sterge(id_film)
            self.__rezervareService.stergere_film(id_film)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def ui_modifica_film(self):
        try:
            id_film = input("Dati id ul filmului de modificat: ")
            titlu = input("Dati noul titlu al filmului : ")
            an_aparitie = int(input("Dati noul an al aparitiei filmului: "))
            pret_bilet = float(input("Dati noul pret al biletului pentru film."
                               " Acesta trebuie sa fie un numar pozitiv: "))
            in_program = input("Dati noua confirmare daca "
                               "filmul este in program(da sau nu): ")

            self.__filmService.modifica(id_film,
                                        titlu,
                                        an_aparitie,
                                        pret_bilet,
                                        in_program)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def show_all_film(self):
        for film in self.__filmService.get_all():
            print(film)

    def run_crud_card_client_menu(self):
        while True:
            print("1. Adauga card")
            print("2. Sterge card")
            print("3. Modifica card")
            print("4. Cautare clienti full text")
            print("a. Afiseaza toate cardurile")
            print("x. Iesire")
            optiune = input("Dati optiunea: ")

            if optiune == "1":
                self.ui_adauga_card()
            elif optiune == "2":
                self.ui_sterge_card()
            elif optiune == "3":
                self.ui_modifica_card()
            elif optiune == "4":
                a = input("Dati un parametru dupa care "
                          "sa fie realizata cautarea cardurilor de clienti: ")
                self.ui_cautare_full_text_clienti(a)
            elif optiune == "a":
                self.show_all_card()
            elif optiune == "x":
                break
            else:
                print("Optiune gresita! Reincercati!")

    def ui_adauga_card(self):
        try:
            id_card = input("Dati id ul cardului: ")
            nume = input("Dati numele detinatorului cardului: ")
            prenume = input("Dati prenumele datinatorului cardului: ")
            CNP = input("Dati CNP detinatorului cardului: ")
            data_nasterii = input("Dati data nasterii a"
                                  " detinatorului de card: ")
            data_inregistrarii = input("Dati data inregistrarii: ")
            puncte_acumulate = float(input("Dati punctele acumulate: "))

            self.__cardClientService.adauga(id_card,
                                            nume,
                                            prenume,
                                            CNP,
                                            data_nasterii,
                                            data_inregistrarii,
                                            puncte_acumulate)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def ui_sterge_card(self):
        try:
            id_card = input("Dati id ul cardului de sters: ")

            self.__cardClientService.sterge(id_card)
            self.__rezervareService.stergere_card(id_card)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def ui_modifica_card(self):
        try:
            id_card = input("Dati id ul cardului de modificat: ")
            nume = input("Dati noul nume al detinatorului: ")
            prenume = input("Dati noul prenumele al datinatorului: ")
            CNP = input("Dati noul CNP al detinatorului: ")
            data_nasterii = input("Dati noua data de nastere: ")
            data_inregistrarii = input("Dati noua data a inregistrarii: ")
            puncte_acumulate = float(input("Dati noile puncte acumulate: "))

            self.__cardClientService.modifica(id_card,
                                              nume,
                                              prenume,
                                              CNP,
                                              data_nasterii,
                                              data_inregistrarii,
                                              puncte_acumulate)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def show_all_card(self):
        for card in self.__cardClientService.get_all():
            print(card)

    def run_crud_rezervare_menu(self):
        while True:
            print("1. Adauga rezervarea")
            print("2. Sterge rezervarea")
            print("3. Modifica rezervarea")
            print("4. Afișarea tuturor rezervărilor"
                  " dintr-un interval de ore dat, indifererent de zi")
            print("a. Afiseaza toate rezervarile")
            print("x. Iesire")
            optiune = input("Dati optiunea: ")

            if optiune == "1":
                self.ui_adauga_rezervare()
            elif optiune == "2":
                self.ui_sterge_rezervare()
            elif optiune == "3":
                self.ui_modifica_rezervare()
            elif optiune == "4":
                try:
                    start = input("Dati prima ora: ")
                    end = input("Dati ora de sfarsit: ")
                    self.afiseaza(self.__rezervareService.dupa_ora(start, end))
                except Exception as e:
                    print(e)
            elif optiune == "a":
                self.show_all_rezervare()
            elif optiune == "x":
                break
            else:
                print("Optiune gresita! Reincercati!")

    def ui_adauga_rezervare(self):
        try:
            id_rezervare = input("Dati id ul rezervarii: ")
            id_film = input("Dati id ul filmului: ")
            id_card = input("Dati id ul cardului: ")
            data = input("Dati data rezervarii: ")
            ora = input("Dati ora rezervarii: ")

            self.__rezervareService.adauga(id_rezervare,
                                           id_film,
                                           id_card,
                                           data,
                                           ora)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def ui_sterge_rezervare(self):
        try:
            id_rezervare = input("Dati id ul rezervarii de sters: ")

            self.__rezervareService.sterge(id_rezervare)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def ui_modifica_rezervare(self):
        try:
            id_rezervare = input("Dati noul id al rezervarii: ")
            id_film = input("Dati noul id al filmului: ")
            id_card = input("Dati noul id al cardului: ")
            data = input("Dati noua data a rezervarii: ")
            ora = input("Dati noua ora a rezervarii: ")

            self.__rezervareService.modifica(id_rezervare,
                                             id_film,
                                             id_card,
                                             data,
                                             ora)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def show_all_rezervare(self):
        for rezervare in self.__rezervareService.get_all():
            print(rezervare)

    def ui_cautare_full_text_filme(self, a):
        try:
            for i in self.__filmService.cautare_full_text_filme(a):
                print(i)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def ui_cautare_full_text_clienti(self, a):
        try:
            for i in self.__cardClientService.cautare_full_text_clienti(a):
                print(i)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def generare(self):
        while True:
            print("1. Sa se genereze n filme")
            print("2. Sa se genereze n carduri clienti")
            print("af. Afisare filme")
            print("ac. Afisare carduri clienti")
            print("x. Iesire")

            optiune = input("Dati optiunea: ")
            if optiune == "1":
                n = int(input("Dati numarul de filme de generat: "))
                self.__filmService.filme_generate(n)
            elif optiune == "2":
                n = int(input("Dati numarul de carduri de generat: "))
                self.__cardClientService.carduri_generate(n)
            elif optiune == "x":
                break
            elif optiune == "af":
                self.show_all_filme()
            elif optiune == "ac":
                self.show_all_clienti()
            else:
                print("Optiune gresita! Reincercati!")

    def show_all_filme(self):
        for filme in self.__filmService.get_all():
            print(filme)

    def show_all_clienti(self):
        for clienti in self.__cardClientService.get_all():
            print(clienti)

    def ui_ordoneaza_card_client(self):
        for cardClient in self.__cardClientService.card_puncte():
            print(cardClient)

    def ui_afisare_rezervari_ore(self):
        try:
            ora_start = input("Dati ora de inceput: ")
            ora_final = input("Dati ora de final: ")
            for rezervare in self.__rezervareService.afisare_rezervari_ore(
                    ora_start, ora_final):
                print(rezervare)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def ui_incrementarea_cardurilor(self):
        try:
            data_1 = input('Dati data de inceput:')
            data_2 = input('Dati data de final:')
            val = int(input('Dati valoarea:'))
            self.__cardClientService.incrementarea_cardurilor(
                data_1, data_2, val)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def ui_stergere_rezervari(self):
        try:
            data_1 = input('Dati data de inceput:')
            data_2 = input('Dati data de final:')
            self.__rezervareService.stergere_rezervari(
                data_1, data_2)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)
