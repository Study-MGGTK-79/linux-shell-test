# Задание 1. Навигация и работа с файлами

## Цель

Познакомиться с терминалом, путями, каталогами и базовыми командами для создания, просмотра, копирования, перемещения и удаления файлов.

## Подготовка

Все команды выполняйте внутри этой папки. Если вы случайно вышли из неё, вернитесь командой `cd` с абсолютным путём.

## Условия

1. Узнайте текущий каталог и выведите его содержимое, включая скрытые файлы.
2. Создайте структуру `project/{docs,src,backup}`.
3. В `docs` создайте файл `notes.txt` с тремя строками текста о Linux.
4. Создайте пустые файлы `src/main.sh` и `src/config.conf`.
5. Выведите содержимое `notes.txt` несколькими способами: `cat`, `less` или `more`, `head`, `tail`.
6. Скопируйте `notes.txt` в `backup/notes-copy.txt`, а `config.conf` переименуйте в `config.local`.
7. Добавьте в `notes.txt` ещё одну строку, сравните оригинал и копию с помощью `diff`.
8. Найдите все файлы проекта командой `find` и удалите только копию `backup/notes-copy.txt`.

## Что должно получиться

В конце должны существовать каталоги `project/docs`, `project/src`, `project/backup`, файл `project/docs/notes.txt`, а также `project/src/main.sh` и `project/src/config.local`. Копии `notes-copy.txt` быть не должно.

## Решение

```bash
# 1. Текущий каталог и скрытые файлы
pwd
ls -la

# 2. Создание вложенных каталогов
mkdir -p project/{docs,src,backup}

# 3. Создание текстового файла. Оператор > записывает текст заново.
printf '%s\n' \
  'Linux — свободная операционная система.' \
  'Терминал позволяет управлять системой командами.' \
  'Команды можно объединять в сценарии.' > project/docs/notes.txt

# 4. Создание пустых файлов
touch project/src/main.sh project/src/config.conf

# 5. Просмотр файла разными командами
cat project/docs/notes.txt
less project/docs/notes.txt       # выход: q
head -n 2 project/docs/notes.txt
tail -n 2 project/docs/notes.txt

# 6. Копирование и переименование
cp project/docs/notes.txt project/backup/notes-copy.txt
mv project/src/config.conf project/src/config.local

# 7. Добавление в конец файла и сравнение
printf 'Изменения удобно проверять командой diff.\n' >> project/docs/notes.txt
diff -u project/backup/notes-copy.txt project/docs/notes.txt

# 8. Поиск и удаление конкретного файла
find project -type f -print
rm project/backup/notes-copy.txt

# Проверка результата
find project -maxdepth 2 -print
```

> Важно: `>` перезаписывает файл, а `>>` добавляет текст в конец. Команду `rm` используйте внимательно: восстановить удалённый файл обычными средствами нельзя.
