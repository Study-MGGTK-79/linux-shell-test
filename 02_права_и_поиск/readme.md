# Задание 2. Права доступа, владельцы и поиск

## Цель

Научиться читать права доступа, менять их в символьной и числовой форме, искать файлы по имени, размеру и времени изменения, а также перенаправлять вывод команд в файлы.

## Условия

1. Создайте каталоги `server/{public,private,logs}` и файлы `public/index.html`, `private/secrets.txt`, `logs/app.log`.
2. Запишите в файлы по несколько строк, используя `printf` и перенаправление вывода.
3. Выведите подробные права доступа (`ls -l`) и объясните себе значение `r`, `w`, `x` для владельца, группы и остальных.
4. Сделайте `private/secrets.txt` доступным только владельцу: режим `600`.
5. Сделайте `public/index.html` обычным читаемым файлом: режим `644`.
6. Добавьте владельцу право выполнения для `logs/app.log`, затем уберите его. Зафиксируйте изменения через `stat`.
7. Найдите все `.log`-файлы, все файлы размером больше 20 байт и все файлы, изменённые за последние 10 минут.
8. Сохраните список найденных файлов в `report.txt`, посчитайте строки и слова в нём командами `wc`.
9. Найдите строки с ошибками в журнале через `grep` без учёта регистра.

## Решение

```bash
mkdir -p server/{public,private,logs}

printf '<h1>Главная страница</h1>\n' > server/public/index.html
printf 'login=student\npassword=change-me\n' > server/private/secrets.txt
printf 'INFO server started\nERROR database unavailable\nWARNING retrying\n' > server/logs/app.log

# Подробный список: права, владелец, размер, дата и имя
ls -lR server

# Символьная форма: только владелец может читать и изменять секреты
chmod u=rw,go= server/private/secrets.txt

# Числовая форма: владелец rw, группа r, остальные r
chmod 644 server/public/index.html

# Временно добавить и затем убрать право выполнения
chmod u+x server/logs/app.log
stat server/logs/app.log
chmod u-x server/logs/app.log
stat server/logs/app.log

# Поиск по расширению, размеру и времени изменения
find server -type f -name '*.log' -print
find server -type f -size +20c -print
find server -type f -mmin -10 -print

# Перенаправление результата поиска и статистика
find server -type f -print | sort > report.txt
wc -l report.txt
wc -w report.txt
wc report.txt

# Поиск ошибок в журнале (-i — без учёта регистра)
grep -in 'error' server/logs/app.log

# Удобная проверка прав
namei -l server/private/secrets.txt
```

## Краткая памятка по правам

`r` — чтение, `w` — изменение, `x` — выполнение файла или вход в каталог. Три группы прав идут в порядке: владелец, группа, остальные. В числовой записи `r=4`, `w=2`, `x=1`, поэтому `640` означает `rw-r-----`.

> Команды `chown` и `chgrp` требуют прав администратора и в этом задании не нужны. Не используйте `sudo` без понимания последствий.

