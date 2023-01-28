from Interface_package.Interface_Hra import Interface_Hra
from Hadana_vec import Hadanka
import time
import threading

class Hra_Hadanka(Interface_Hra):

    def __init__(self):
        """
        Konstruktor
        """
        self._timeout = 10
        self._max_lenght_of_word = 10


    @property
    def timeout(self):
        """
        Getter timoutu
        :return: _timeout
        """
        return self._timeout

    @timeout.setter
    def timeout(self,val):
        """
        Nastavuje novej cas na uhadnuti
        :param val: novej cas
        :return: void
        """
        if isinstance(val,float)==True:
            self._timeout=val
        else:
            raise ValueError("Inserted value is not number")

    @property
    def max_lenght_of_word(self):
        """
        Getter maximalni delky slova
        :return: _max_lenght_of_word
        """
        return self._max_lenght_of_word

    @max_lenght_of_word.setter
    def max_lenght_of_word(self,val):
        """
        Setter maximalni delky slova
        :param val: nova maximalni delka
        :return: void
        """
        if isinstance(val,int)==True:
            self._max_lenght_of_word=val
        else:
            raise ValueError("Inserted value is not number")

    def hraj(self, hadanka: Hadanka):
        """
        Metoda vyuziva vlakna a snazi se uhodnout vetu
        za limitovany cas

        :param hadanka: hadanka kterou ma metoda vyresit
        :return: True kdyz uhone False kdyz nestihne
        """
        START = time.perf_counter()
        start_for_method = True
        t = threading.Thread(target=hadanka.hadej_vetu, args=(hadanka._unit,))
        t.start()
        while True:
            END = time.perf_counter()
            end_time = END - START
            if END - START > self._timeout or hadanka.result == False:
                Hadanka.stop=True
                print(f"Timeout")

                return False
            elif hadanka.result == True and start_for_method == True:
                print(f"find sentence took {end_time:.6f}s and remaind {self.timeout - end_time:.6}s")
                t.join()
                return True
            continue


    def Zacit_hru(self):
        """
        Metoda slouzi jako main meny hry odkud se hra spusti
         nebo muzem zmenit parametry hry v nastaveni
        :return: void
        """
        play=True
        while play==True:
            choice=input(f"Welcome in guessig game\n now setting is timeout={self.timeout} and max lenght is={self.max_lenght_of_word} select: \n 1 to START \n 2 SETTING \n 3 EXIT ")
            if choice=="1":
                sentence=input("Wrote sentence I have to guess condition:\nnumbers as word and no diacritics it will be removed and sentence in english pls \n")
                if self._Check_lenght_of_words(sentence.split(" "))==0:
                    try:
                     Puszzl=Hadanka(sentence)
                    except ValueError as ex:
                        print(ex)
                        continue
                    print(f"\nOriginal sentence:{Puszzl._origin} \nCleaned sentence:{Puszzl._unit}")
                    result=self.hraj(Puszzl)
                    if result==True:
                        print(f"I have won, final sentance is:\n {Puszzl.Que_ToString()}")
                        continue
                    elif result==False:
                        print(f"You have won, i only guessed:\n {Puszzl.Que_ToString()}")
                        continue
                else:
                    print(f"Words are way too long.. max lenght of word is {self._max_lenght_of_word} or way too long sentence")

            elif choice=="2":
                self._Setting()
                continue
            elif choice=="3":
                break
            else:
                print("sutch opinion doesnt exist")
                continue




    def _Setting(self):
        """
        Jde o Nastaveni hry, lze zde nastavit:
         timeou:kolik casu ma hra na uhodnuti
         max_lenght:jake nejdelsi slovo lze zadat
        :return: void
        """
        timeout =float(input("How mutch time do you wana give me to guess?"))
        self.timeout=timeout
        max_lenght = int(input("Max lenght of one word"))
        self.max_lenght_of_word=max_lenght


    def _Check_lenght_of_words(self,list:[]):
        """
        Kontrola delky slov ve vete
        :param list:
        :return:
        """
        longer_words=0
        if len(list)>15:
            longer_words=longer_words+1
            return longer_words
        for word in list:
            if len(word)>self._max_lenght_of_word:
                longer_words=longer_words+1
            else:
                continue
        return longer_words
















