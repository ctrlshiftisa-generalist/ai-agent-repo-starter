import argparse
import re
from slugify import slugify

def normalize_token(t: str) -> str:
    t = t.strip().lower()
    # уберём символы пунктуации по краям
    t = re.sub(r'^[\W_]+|[\W_]+$', '', t, flags=re.UNICODE)
    return t

def token_variants(core_set):
    # базовая генерация вариаций: транслитерация упрощённая и частичные суффиксы
    variants = set(core_set)
    for w in list(core_set):
        # Частые узбекские/русские суффиксы
        for suf in ['lar', 'lari', 'ga', 'gacha', 'ni', 'ning', 'dan', 'li', 
                    'ы', 'и', 'а', 'я', 'ки', 'ок', 'ам', 'ов', 'ика', 'ике', 'ики']:
            variants.add(w + suf)
        # Примитив: латиница <-> кириллица на уровне отдельных букв (упрощённо)
        translit = (
            w.replace('с', 's').replace('о', 'o').replace('а','a').replace('т','t')
             .replace('ч','ch').replace('у','u').replace('к','k').replace('р','r')
        )
        variants.add(translit)
    return variants

def is_related(token, core_variants):
    if token in core_variants:
        return True
    # если содержит ядро как подстроку
    for c in core_variants:
        if len(c) >= 3 and c in token:
            return True
    return False

def split_phrases(text):
    # делим по запятой и переносам строк на фразы, затем каждую фразу на токены
    raw_phrases = re.split(r'[\n,]+', text, flags=re.UNICODE)
    tokens = []
    for ph in raw_phrases:
        # разбивка на слова
        for tok in re.split(r'[\s\-_/|.;:]+', ph.strip(), flags=re.UNICODE):
            tok = normalize_token(tok)
            if tok:
                tokens.append(tok)
    return tokens

def csv_line(words):
    # уникализируем, сортируем
    uniq = sorted(set(words))
    return ','.join(uniq)

def main():
    ap = argparse.ArgumentParser(description='Minus-word agent demo CLI')
    ap.add_argument('--core', type=str, required=True, help='Ядро, слова через запятую')
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument('--text', type=str, help='Текст со словами/фразами')
    src.add_argument('--input', type=str, help='Путь к файлу со словами/фразами')
    ap.add_argument('--out', type=str, default='data/minus_words.txt', help='Куда сохранить результат')
    args = ap.parse_args()

    core_tokens = [normalize_token(t) for t in args.core.split(',') if t.strip()]
    core_set = set(core_tokens)
    core_variants = token_variants(core_set)

    if args.text:
        text = args.text
    else:
        with open(args.input, 'r', encoding='utf-8') as f:
            text = f.read()

    tokens = split_phrases(text)

    minus_candidates = []
    doubtful = []
    for tok in tokens:
        if is_related(tok, core_variants):
            continue
        # если слишком похоже на ядро (Лёвенштейн можно, но без зависимостей сделаем эвристику)
        close = any(abs(len(tok)-len(c)) <= 1 and tok[:3] == c[:3] for c in core_set)
        if close:
            doubtful.append(tok)
        else:
            minus_candidates.append(tok)

    line = csv_line(minus_candidates)
    with open(args.out, 'w', encoding='utf-8') as f:
        f.write(line)

    print(line)
    if doubtful:
        print('\n[Сомнительные]:', ','.join(sorted(set(doubtful))))

if __name__ == '__main__':
    main()
