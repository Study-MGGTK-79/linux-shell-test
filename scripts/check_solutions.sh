#!/bin/bash
set -euo pipefail

echo "========================================================"
echo "Проверка эталонных решений для всех 5 заданий"
echo "========================================================"

FAILED=0

# Задание 1
ANS1=$(grep -c ' 404 ' data/server.log)
EXPECTED1="3421"
if [ "$ANS1" = "$EXPECTED1" ]; then
    echo "✅ Задание 1 (server.log, 404 count): $ANS1 (верно)"
else
    echo "❌ Задание 1: получено $ANS1, ожидалось $EXPECTED1"
    FAILED=1
fi

# Задание 2
ANS2=$(sort data/logins.txt | uniq -c | sort -nr | head -n 1 | awk '{print $2}')
EXPECTED2="m_ivanov"
if [ "$ANS2" = "$EXPECTED2" ]; then
    echo "✅ Задание 2 (logins.txt, top user): $ANS2 (верно)"
else
    echo "❌ Задание 2: получено $ANS2, ожидалось $EXPECTED2"
    FAILED=1
fi

# Задание 3
ANS3=$(tail -n +2 data/products.csv | sort -t, -k4,4n | tail -n 1 | cut -d, -f1)
EXPECTED3="SKU-58421"
if [ "$ANS3" = "$EXPECTED3" ]; then
    echo "✅ Задание 3 (products.csv, max price SKU): $ANS3 (верно)"
else
    echo "❌ Задание 3: получено $ANS3, ожидалось $EXPECTED3"
    FAILED=1
fi

# Задание 4
ANS4=$(find project -type f -name "*.conf" | wc -l | tr -d ' ')
EXPECTED4="37"
if [ "$ANS4" = "$EXPECTED4" ]; then
    echo "✅ Задание 4 (project/, *.conf regular files): $ANS4 (верно)"
else
    echo "❌ Задание 4: получено $ANS4, ожидалось $EXPECTED4"
    FAILED=1
fi

# Задание 5
ANS5=$(grep "Failed password" data/auth.log | cut -d' ' -f11 | sort -u | wc -l | tr -d ' ')
EXPECTED5="164"
if [ "$ANS5" = "$EXPECTED5" ]; then
    echo "✅ Задание 5 (auth.log, unique failed IPs): $ANS5 (верно)"
else
    echo "❌ Задание 5: получено $ANS5, ожидалось $EXPECTED5"
    FAILED=1
fi

echo "========================================================"
if [ "$FAILED" -eq 0 ]; then
    echo "🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!"
    exit 0
else
    echo "⚠️ Были обнаружены расхождения."
    exit 1
fi
