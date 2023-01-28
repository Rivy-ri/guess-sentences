from random import randint
from Interface_package.Interface_Hadanka import InterfaceHadanka
import multiprocessing


class Hadanka(InterfaceHadanka):
    result=None #slouzi k zjisteni vysledku
    stop=False #slouzi k zastaveni processu
    def __init__(self,veta:str):
        """
        vytvori objekt s vlastnostma
        _origin: puvodni veta
        _unit: vycistena veta od nezadanych znaku
        words_in_unit: pole slov co veta obsahuje
        _array_of_guessed_words: pole uhodnutych slov pred generovane s prazdnzma stringaman

        :param veta:
        """
        if len(veta)>0 and len(Hadanka._clean_sentence(veta))>0:
            self._origin =veta
            self._unit=Hadanka._clean_sentence(veta)
            self.words_in_unit=self._unit.split(' ')
            self._array_of_guessed_words=multiprocessing.Queue(self.pocet_slov())
            self.guessed_sentence=[" "]*len(self.words_in_unit)
        else:
            raise ValueError("empty sentence")


    def pocet_slov(self):
        """
        Vraci pocet slov ve vete

        :return: int
        """
        return len(self.words_in_unit)

    def hadej_slovo(self, slovo: str):
        """
        Metoda hleda slovo podle vygenerovaneho
        cisla ktere se prevede na pismeno prohledava vybrane slovo
        a nasledne pokud najde jeddnu shodu tak posle
        slovo do metody _match_in_word()

        :param slovo: slovo ktere metoda hada
        :return:  bool
        """
        print(f"the program started to guess the word: {slovo}")
        slovo=slovo.lower()
        already_guessed_latters = []
        guessed_word = list(slovo.lower())
        right_guessed_latters = ["null"] * len(guessed_word)
        while Hadanka._Array_ToString(right_guessed_latters,False)!=slovo:
            number=Hadanka.Generate_number(already_guessed_latters)
            if isinstance(number,int):
                latter=chr(number)
                already_guessed_latters.append(number)
                for i in range(len(guessed_word)):
                    if guessed_word[i]==latter:
                        result=self._match_in_word(latter,len(guessed_word),right_guessed_latters,guessed_word,slovo)
                        if result==True or Hadanka._Array_ToString(right_guessed_latters,False)==slovo:
                            print(f"State of guessed words: {self.Write_All_from_Que()}")
                            return True
                            break


                    else:
                        continue

            else:
                print("Out of range")
                break
                return False

    def hadej_vetu(self, veta: str):
        """
        Metoda hada vetu tak ze rozdelenou veti naslova
        priradi jednotlivim processum ktere je pak hadaj
        kdyz se vsechny processy dohadaji slova
        tak zkontroluje zda pos serazeni slov jsou schodna s
        upravenou verzi vety

        :param veta: kterou hadame
        :return: bool
        """
        my_process = []
        for i in range(len(self.words_in_unit)):
            p = multiprocessing.Process(target=self.hadej_slovo, args=(self.words_in_unit[i],))
            p.start()
            my_process.append(p)
        for p in my_process:
            if Hadanka.stop==False:
             p.join()
            else:
                self.result==False
            continue


        if self.Que_ToString() == self._unit:
            lock=multiprocessing.Lock()
            lock.acquire()
            print("Uhodnuto")
            lock.release()
            self.result=True
        elif Hadanka.stop==True:
            for p in my_process:
                p.terminate()
            self.result=False
        else:
            self.result=False





    def _match_in_word(self,latter:str,lenght:int,right_guessed_latters:[],guessed_word:[],slovo):
        """
        Dukladne prohleda slovo a najde vsechny schody s latter a pokud se pote po prevodu na
        string right_guessed_latters rovnaji se slovem rovnou provede iteraci


        :param latter: pismeno ktere je hledane ve slove
        :param lenght: delka slova
        :param right_guessed_latters: spravne uhodnuta pismena
        :param guessed_word: hadane slovo ve forme pole, uzivane k prepisovani
        :param slovo: slovo ktere se pouziva pro porovnani
        :return: bool
        """
        try:
            for i in range(lenght):
                _index=guessed_word.index(latter)
                guessed_word[_index]="#"
                right_guessed_latters[_index]=latter
                if self._Array_ToString(right_guessed_latters,False)==slovo:
                    lock = multiprocessing.Lock()
                    nalezene_slovo=self._Array_ToString(right_guessed_latters,False)
                    self._array_of_guessed_words.put(nalezene_slovo)

                    return True
                else:
                    return False
        except ValueError:
            if slovo==Hadanka._Array_ToString(right_guessed_latters,False):
                self._array_of_guessed_words.put(Hadanka._Array_ToString(right_guessed_latters,False))
                return True
            else:
                return False






    @staticmethod
    def _clean_sentence(sentence:str):
        """
        Vycisti vetu od nezadanych pismen, znaku, mezer
         a celou vetu prevede na mala pismena

        :param sentence: Veta kterou chcem vycistit
        :return: string
        """
        sentence = sentence.lower()
        marks=[",","?","!",".","@","#","$","%","^","&","*","<",">",":",";","{","}","'","=","+","-"]
        diacritics=[("ě","e"),("š","s"),("č","c"),("ř","r"),("ž","z"),("ý","y"),("á","a"),("í","i"),("é","e"),("ú","u"),("ů","u"),("ó","o"),("ň,n")]
        numbers=["0","1","2","3","4","5","6","7","8","9"]
        for i in range(len(marks)):
            sentence=sentence.replace(marks[i],"")
        for i in range(len(diacritics)):
            sentence=sentence.replace(diacritics[i][0],diacritics[i][1])
        for i in range(len(numbers)):
            sentence=sentence.replace(numbers[i],"")
        cleaned=sentence.strip()

        return str(cleaned)

    @staticmethod
    def Generate_number(exept:[]):
        """
        Generuje nahodna cisla v rozsahu malich pismen Asci tabulky
        :param exept: ValueError
        :return: int
        """
        returned=False
        while returned==False:
            #97-122 mala
            number=randint(97,122)
            try:
                exept.index(number)
                continue
            except ValueError:
                if len(exept)<=25:
                    return number
                    break
                else:
                    return "all latter have been used"

    @staticmethod
    def _Array_ToString(pole:[],space:bool):
        """
        Prevadi pole na string

        :param pole: ktere chceme prevest
        :param space: jestli chcem prvky dohromady v jednom slove nebo oddelene jako vetu
        :return: string
        """
        if space==False:
            string=""
            return (string.join(pole))
        else:
            string=" "
            return (string.join(pole))

    def Write_All_from_Que(self):
        """
        z dat v multiprocesove Queue udela pole
        :return: array
        """
        lock =multiprocessing.Lock()
        lock.acquire()
        array=[]
        size=self._array_of_guessed_words.qsize()
        for i in range(size):
         array.append(self._array_of_guessed_words.get())
         self._array_of_guessed_words.put(array[i])
        return array
        lock.release()

    def Que_ToString(self):
        """
        Pretvori multiprocesingovou Queue do pole, seradi podle poradi ve ve vete a
        a vrati organizovanou vetu

        :return: string
        """
        array_unordered=self.Write_All_from_Que()
        for i in range(len(array_unordered)):
            self._Que_deep_seach(array_unordered[i], len(self.guessed_sentence))

        return self._Array_ToString(self.guessed_sentence,True)

    def _Que_deep_seach(self, slovo, lenght):
        """
        Je soucasti Que_ToString ma za ukol najit pozice vsech
         mist kde se slovo nachazi podle indexu v slov vety a nasledne jej prepise
         aby jej nenalezlo znovu

         #poz. metody jsou rozdelene protoze by v nich jinak byl chaos

        :param slovo: hledane slovo v poli
        :param lenght: delka vety
        :return: void
        """
        try:
            for i in range(lenght):
                index = self.words_in_unit.index(slovo)
                self.words_in_unit[index]="#"
                lock=multiprocessing.Lock()
                lock.acquire()
                self.guessed_sentence[index] = slovo
                lock.release()

        except ValueError:
            return















