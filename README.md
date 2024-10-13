Эмулятор Оптимизированной Оболочки для UNIX-подобных ОС

Описание

Данный проект представляет собой эмулятор командной оболочки UNIX-подобных ОС. Эмулятор работает в режиме CLI (командная строка) и позволяет пользователям взаимодействовать с виртуальной файловой системой, представленной в виде файла формата tar. Основная цель этого проекта — обеспечить максимально близкий опыт работы с оболочкой UNIX.

Функциональные возможности

Эмулятор поддерживает базовые команды:

- ls: отображение списка файлов и директорий.
- cd: смена текущей директории.
- exit: выход из эмулятора.
- date: отображение текущей даты и времени.
- touch: создание нового файла или обновление времени последнего доступа к существующему.

Запуск

Эмулятор запускается из реальной командной строки и принимает следующие аргументы:

- -h, --hostname: Имя компьютера для отображения в приглашении к вводу.
- -vfs, --vfs-path: Путь к архиву виртуальной файловой системы (файл формата tar).
- -s, --script: Путь к стартовому скрипту, который будет выполнен при запуске эмулятора.
