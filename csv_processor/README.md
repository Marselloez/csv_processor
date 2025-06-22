# CSV Processor

## Описание
Скрипт обрабатывает CSV-файл, поддерживает фильтрацию, агрегации и сортировку.

## Запуск
```
python main.py --file products.csv --where "price>500" --aggregate "rating=avg" --order-by "price=desc"
```

## Аргументы
- `--file` — путь к файлу CSV
- `--where` — фильтрация
- `--aggregate` — агрегатная функция (`avg`, `min`, `max`)
- `--order-by` — сортировка по колонке (`asc` или `desc`)

## Пример CSV
```
name,brand,price,rating
iphone 15 pro,apple,999,4.9
galaxy s23 ultra,samsung,1199,4.8
redmi note 12,xiaomi,199,4.6
```
