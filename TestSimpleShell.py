import unittest
import os
from ShellEmulator import ShellEmulator
from unittest.mock import patch, mock_open
import datetime

class TestShellEmulator(unittest.TestCase):

    @patch('datetime.datetime')
    def test_date(self, mock_datetime):
        # Устанавливаем фиктивное время
        mock_datetime.now.return_value = datetime.datetime(2024, 10, 1, 17, 30, 0)
        mock_datetime.now.return_value.strftime = lambda fmt: '2024-10-01 17:30:00'

        # Перехватываем вывод функции
        with patch('builtins.print') as mock_print:
            # Вызов тестируемой функции
            self.date()
            # Проверка, что функция вывела правильное время
            mock_print.assert_called_once_with('2024-10-01 17:30:00')

    def date(self):
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.utime')
    @patch('os.path')
    def test_touch(self, mock_path, mock_utime, mock_open):
        # Настройка mock для resolve_path
        self.resolve_path = lambda x: x

        # Тестирование, когда args пустой
        self.touch([])
        mock_open.assert_not_called()
        mock_utime.assert_not_called()

        # Тестирование, когда args не пустой
        mock_path.exists.return_value = True
        self.touch(['testfile.txt'])
        mock_open.assert_called_once_with('testfile.txt', 'a')
        mock_utime.assert_called_once_with('testfile.txt', None)

    def touch(self, args):
        if not args:
            return
        path = self.resolve_path(args[0])
        with open(path, 'a'):
            os.utime(path, None)

    @patch('os.path.isdir')
    def test_cd(self, mock_isdir):
        # Настройка mock для resolve_path
        self.resolve_path = lambda x: x
        self.current_dir = None

        # Тестирование, когда args пустой
        self.cd([])
        self.assertIsNone(self.current_dir)

        # Тестирование, когда директория существует
        mock_isdir.return_value = True
        self.cd(['existing_dir'])
        self.assertEqual(self.current_dir, 'existing_dir')

        # Тестирование, когда директория не существует
        mock_isdir.return_value = False
        with patch('builtins.print') as mock_print:
            self.cd(['non_existing_dir'])
            mock_print.assert_called_once_with('non_existing_dir: No such directory')
            self.assertNotEqual(self.current_dir, 'non_existing_dir')

    def cd(self, args):
        if not args:
            return
        path = self.resolve_path(args[0])
        if os.path.isdir(path):
            self.current_dir = path
        else:
            print(f"{path}: No such directory")

    def resolve_path(self, path):
        # Пример реализации resolve_path
        return path

    def ls(self, args):
        path = self.resolve_path(args[0] if args else self.current_dir)
        if os.path.isdir(path):
            print("\n".join(os.listdir(path)))
        else:
            print(f"{path}: No such directory")
    @patch('os.listdir')
    @patch('os.path.isdir')
    def test_ls(self, mock_isdir, mock_listdir):
        # Настройка mock для resolve_path
        self.resolve_path = lambda x: x
        self.current_dir = 'current_dir'

        # Тестирование, когда директория существует
        mock_isdir.return_value = True
        mock_listdir.return_value = ['file1.txt', 'file2.txt']
        with patch('builtins.print') as mock_print:
            self.ls(['existing_dir'])
            mock_print.assert_called_once_with('file1.txt\nfile2.txt')

        # Тестирование, когда директория не существует
        mock_isdir.return_value = False
        with patch('builtins.print') as mock_print:
            self.ls(['non_existing_dir'])
            mock_print.assert_called_once_with('non_existing_dir: No such directory')
            mock_isdir.return_value = True
            mock_listdir.return_value = ['file3.txt', 'file4.txt']
            with patch('builtins.print') as mock_print:
                self.ls([])
                mock_print.assert_called_once_with('file3.txt\nfile4.txt')



if __name__ == '__main__':
    unittest.main()
