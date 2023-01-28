import unittest

import Hadana_vec
import Hra_Hadanka
import Interface_package.Interface_Hra


class MyTestCase(unittest.TestCase):

    """
    Test zda tridy Hra_Hadanka implementuje
    """
    def test_HH_implement_interface(self):
        """
        Test zda trida Hra_Hadanka implementuje interface
        :return:
        """
        instance=Hra_Hadanka.Hra_Hadanka()
        self.assertIsInstance(instance,Interface_package.Interface_Hra.Interface_Hra)

    def test_HH_default_values(self):
        """
        test gettru tridy
        :return:
        """
        instance = Hra_Hadanka.Hra_Hadanka()
        self.assertEqual(instance.timeout,10)
        self.assertEqual(instance.max_lenght_of_word,10)

    def test_HH_default_setters(self):
        """
        Test Setteru tridy
        :return:
        """
        instance = Hra_Hadanka.Hra_Hadanka()
        instance.timeout=21.1
        instance.max_lenght_of_word=5
        self.assertEqual(instance.timeout,21.1)
        self.assertEqual(instance.max_lenght_of_word,5)
    def test_HH_stop_game(self):
        """
        Test zda se hra zastavi kdyz nestihne
        :return:
        """
        instance_1=Hra_Hadanka.Hra_Hadanka()
        instance_2=Hadana_vec.Hadanka("Nothing seemed out of place except the washing machine in the bar.")
        instance_1.timeout=0.005
        self.assertEqual(instance_1.hraj(instance_2),False)

if __name__ == '__main__':
    unittest.main()
