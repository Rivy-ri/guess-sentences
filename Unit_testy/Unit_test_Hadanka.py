import unittest
import Interface_package.Interface_Hadanka
from Hadana_vec import Hadanka


class MyTestCase(unittest.TestCase):

    def test_Hv_pocet_slov(self):
        """
        Test pocitani slov ve vete
        :return:
        """
        instance_1=Hadanka("Lorem ipsum dolor sit amet consectetur adipisicing elit")
        instance_2=Hadanka("Skakal pes pres oves")
        instance_3=Hadanka("Mr. Doctor Man questions his hands, lost his mind but he's clinically fine, but he found a way to cope, needle in his throat.")
        self.assertEqual(instance_1.pocet_slov(),8)
        self.assertEqual(instance_2.pocet_slov(),4)
        self.assertEqual(instance_3.pocet_slov(),24)

    def test_Hv_clean_sentence(self):
        """
        Test cisteni vety od nezadanych znaku
        :return:
        """
        instance_1 = "Lorem ipsum do85lor, sit."
        instance_2 = "Skákal peš? pres oves   "

        instance_1c="lorem ipsum dolor sit"
        instance_2c="skakal pes pres oves"

        self.assertEqual(Hadanka._clean_sentence(instance_1),instance_1c)
        self.assertEqual(Hadanka._clean_sentence(instance_2),instance_2c)


    def test_Hv_create_small_sentence(self):
        """
        Test tvorby vety bez obsahu
        :return:
        """
        with self.assertRaises(ValueError):
            instance1=Hadanka("")
            instance2=Hadanka("      ")

    def test_Hv_hadej_slovo(self):
        """
        Test hadani slova
        :return:
        """
        instance1=Hadanka("pes")
        self.assertEqual(instance1.hadej_slovo(instance1.words_in_unit[0]),True)
        self.assertEqual(instance1.Que_ToString(),"pes")


    def test_Hv_Array_ToString(self):
        """
        Test metody co prepisuje pole na string
        :return:
        """
        self.assertEqual(Hadanka._Array_ToString(["Skakal","pes","pres","oves"],False),"Skakalpespresoves")
        self.assertEqual(Hadanka._Array_ToString(["Skakal","pes","pres","oves"],True),"Skakal pes pres oves")

    def test_Hv_Generate_number(self):
        """
        Test generovani cisel ktera se pouzivaj na generovani pismen
        :return:
        """
        array = [97, 99, 98, 100]
        number1=Hadanka.Generate_number(array)
        number2 = Hadanka.Generate_number(array)
        number3 = Hadanka.Generate_number(array)
        number4 = Hadanka.Generate_number(array)
        for i in array:
         self.assertNotEqual(number1,i)
         self.assertNotEqual(number2, i)
         self.assertNotEqual(number3, i)
         self.assertNotEqual(number4, i)

    def test_Hv_Write_all_from_Que(self):
        """
        Vypsani vseho z multiprocesingove queue
        :return:
        """
        instance1 = Hadanka("Nothing is as cautiously cuddly as a pet porcupine.")
        instance1.hadej_vetu(instance1._unit)
        self.assertNotEqual(instance1.words_in_unit,instance1.Write_All_from_Que())

    def test_Hv_Que_to_string(self):
        """
        Test vypsani Queue do stringu
        :return:
        """
        instance1 = Hadanka("Nothing is as cautiously cuddly as a pet porcupine.")
        instance1.hadej_vetu(instance1._unit)
        self.assertEqual(instance1.Que_ToString(),instance1._unit)

    def test_Hv_implement_interfaces(self):
        """
        Test zda Trida Hadanka implementuje interface
        :return:
        """
        instance1=Hadanka("abraka dabra")
        self.assertIsInstance(instance1,Interface_package.Interface_Hadanka.InterfaceHadanka)



if __name__ == '__main__':
    unittest.main()
