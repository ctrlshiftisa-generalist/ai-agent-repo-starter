# AI Minus-Word Agent — автоматизация минус-слов для маркетплейса и e‑commerce

> Кейc: Uzum / ZoomSelling. Время ручной фильтрации минус-слов — с 3–4 часов до ~15 минут.

![Demo placeholder](docs/cover.png)

## Что это
Лёгкий репозиторий-витрина с документацией и минимальным CLI-скриптом,
который демонстрирует логику работы агента: токенизация фраз, фильтрация по ядру,
формирование финального списка минус-слов и поддержка «сомнительных» кейсов.

- Подробности: `docs/PROBLEM_SOLUTION.md`
- База знаний (морфология, транслит, правила): `docs/knowledge_base.md`
- Инструкция для GPT-агента: `docs/INSTRUCTION.md`
- Презентация: `docs/presentation_uzum_zoomselling.pdf`

## Быстрый старт
```bash
python3 -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python src/main.py --help
```

## Мини‑CLI
Скрипт `src/main.py` умеет:
- принимать ядро (`--core "rolex, soat, erkaklar"`),
- принимать список фраз/слов из файла (`--input data/phrases.txt`) или из строки (`--text "soat korean, roleks qizlar"`),
- возвращать минус-слова строкой CSV и сохранять в файл (`--out data/minus_words.txt`).

## Формат данных
- вход: фразы через запятую или перенос строки;
- ядро: слова через запятую;
- вывод: одна строка CSV (UTF‑8), без дубликатов, отсортировано.

## Дисклеймер
Этот проект оформлен в стиле «vibe-coding»: логика агента концептуальная и демонстрационная.
