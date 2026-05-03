#!/usr/bin/env python3
"""Statistical style analysis for Chinese novel reference text.

Usage:
    python analyze_style.py reference.txt [output.yaml]

Input: UTF-8 plain text of a reference novel.
Output: style-metrics.yaml with quantifiable style rules.
"""

import re
import sys
import math
from collections import Counter
from pathlib import Path

import yaml

try:
    import jieba
    import jieba.posseg as pseg
except ImportError:
    print("请先安装 jieba: pip install jieba")
    sys.exit(1)


# ── text preprocessing ──────────────────────────────────────────

def load_and_clean(path: str) -> str:
    text = Path(path).read_text(encoding="utf-8")
    # Remove common chapter title patterns
    text = re.sub(r'^第[零一二三四五六七八九十百千\d]+[章节卷].*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*[#＃]\s*.*$', '', text, flags=re.MULTILINE)
    # Normalize newlines
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    # Collapse multiple blank lines
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


# ── sentence splitting ──────────────────────────────────────────

SENTENCE_ENDS = re.compile(r'[。！？；!?;]')
# Chinese quotes
QUOTE_PAIRS = [
    ('“', '”'),  # ""
    ('‘', '’'),  # ''
    ('「', '」'),  # 「」
    ('『', '』'),  # 『』
    ('"', '"'),
    ('"', '"'),
]

def split_sentences(text: str) -> list[str]:
    """Split Chinese text into sentences, respecting quote pairs."""
    sentences = []
    buf = ''
    depth = 0
    opener = None
    for ch in text:
        if opener and ch == opener[1]:
            depth -= 1
            if depth == 0:
                opener = None
            buf += ch
        elif not opener:
            for o, c in QUOTE_PAIRS:
                if ch == o:
                    depth = 1
                    opener = (o, c)
                    break
        if not opener:
            for o, _ in QUOTE_PAIRS:
                if ch == o:
                    depth = 1
                    opener = (o, _)
                    break
        if ch == opener[1] if opener else False:
            depth -= 1
            if depth == 0:
                opener = None

        buf += ch
        if not opener and ch in '。！？；':
            if buf.strip():
                sentences.append(buf.strip())
            buf = ''
    if buf.strip():
        sentences.append(buf.strip())
    return sentences


def sentence_length_stats(sentences: list[str]) -> dict:
    lengths = [len(s) for s in sentences]
    n = len(lengths)
    if n == 0:
        return {}
    mean = sum(lengths) / n
    variance = sum((l - mean) ** 2 for l in lengths) / n
    short = sum(1 for l in lengths if l < 10)
    medium = sum(1 for l in lengths if 10 <= l <= 40)
    long = sum(1 for l in lengths if l > 50)
    return {
        'short_ratio': round(short / n, 4),
        'medium_ratio': round(medium / n, 4),
        'long_ratio': round(long / n, 4),
        'mean': round(mean, 1),
        'stdev': round(math.sqrt(variance), 1),
    }


# ── sentence openings ───────────────────────────────────────────

def sentence_opening_stats(sentences: list[str]) -> list[dict]:
    c = Counter()
    for s in sentences:
        # Take first 1-2 chars as opening
        first = s[:2] if len(s) >= 2 else s[:1]
        # Only count hanzi openings
        if re.match(r'[一-鿿]', first[0]):
            c[first] += 1
        elif len(s) >= 1 and re.match(r'[一-鿿]', s[0]):
            c[s[0]] += 1
    total = sum(c.values())
    if total == 0:
        return []
    return [{'char': k, 'ratio': round(v / total, 4)} for k, v in c.most_common(20)]


# ── paragraph stats ─────────────────────────────────────────────

def paragraph_stats(text: str, sentences: list[str]) -> dict:
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    para_lengths = [len(p) for p in paragraphs]
    n = len(para_lengths)
    if n == 0:
        return {}
    mean = sum(para_lengths) / n
    sorted_lens = sorted(para_lengths)
    median = sorted_lens[n // 2]

    single_sentence_paras = 0
    for p in paragraphs:
        s_count = 0
        for s in sentences:
            if s in p:
                s_count += 1
        if s_count == 1:
            single_sentence_paras += 1

    return {
        'mean': round(mean, 1),
        'median': median,
        'min': min(para_lengths),
        'max': max(para_lengths),
        'count': n,
        'single_sentence_ratio': round(single_sentence_paras / n, 4) if n else 0,
    }


# ── dialogue ratio ──────────────────────────────────────────────

def dialogue_stats(text: str) -> dict:
    """Estimate dialogue ratio by counting characters inside Chinese quotes."""
    dialogue_chars = 0
    for o, c in [('“', '”'), ('「', '」'), ('"', '"'), ('‘', '’')]:
        pattern = re.escape(o) + r'([^' + re.escape(c) + r']*)' + re.escape(c)
        for m in re.finditer(pattern, text):
            dialogue_chars += len(m.group(1))
    total_chars = len(re.sub(r'\s', '', text))
    return {
        'dialogue_ratio': round(dialogue_chars / total_chars, 4) if total_chars else 0,
        'total_chars': total_chars,
    }


# ── punctuation profile ─────────────────────────────────────────

def punctuation_stats(text: str) -> dict:
    total = len(re.sub(r'\s', '', text))
    if total == 0:
        return {}
    result = {}
    total_per_1000 = total / 1000
    for char, name in [('。', 'period'), ('，', 'comma'), ('！', 'exclamation'),
                       ('？', 'question'), ('…', 'ellipsis'), ('；', 'semicolon'),
                       ('、', 'enum_comma')]:
        count = text.count(char)
        result[name] = {'count': count, 'per_1000': round(count / total_per_1000, 1)}
    return result


# ── word frequency ──────────────────────────────────────────────

FUNCTION_CHARS = set('的地得了着过在是和有这那不也就要对可可以会但然其后到于之与而所能自从此将因所被比向从')

PUNCTUATION_CHARS = set('，。！？；：、""''「」『』（）《》…—·～\t\n\r ' + '"' + "'")

def word_frequency_stats(text: str) -> dict:
    words = jieba.lcut(text)
    words = [w for w in words if w not in PUNCTUATION_CHARS and not w.isspace()
             and not (len(w) == 1 and (w in FUNCTION_CHARS or w in PUNCTUATION_CHARS))]
    c = Counter(words)
    total = c.total()
    top200 = [{'word': w, 'count': n, 'per_100k': round(n / total * 100000, 1)}
              for w, n in c.most_common(200)]

    # Categorize: adverbs, conjunctions, common patterns
    adverbs = [item for item in top200
               if any(kw in item['word'] for kw in ['很', '非常', '极', '特别', '太', '十分',
                                                     '不由得', '不禁', '忍不住', '渐渐', '忽然',
                                                     '突然', '始终'])]
    conjunctions = [item for item in top200
                    if any(kw in item['word'] for kw in ['然而', '但是', '于是', '接着', '然后',
                                                          '这时', '便', '却', '但', '虽'])]

    return {
        'top_200': top200,
        'high_freq_adverbs': adverbs[:20],
        'high_freq_conjunctions': conjunctions[:20],
    }


# ── idiom density ───────────────────────────────────────────────

IDIOM_RE = re.compile(r'[一-鿿]{4}')

def idiom_stats(text: str) -> dict:
    """Estimate four-character idiom density. Uses a heuristic: the 4-char
    string must contain at least 2 hanzi and not be a common non-idiom pattern.
    For accurate results, pair with a known idiom list."""
    cleaned = re.sub(r'\s', '', text)
    matches = IDIOM_RE.findall(cleaned)
    # Filter: idiom must contain at least 2 hanzi, no common non-idiom patterns
    filtered = [m for m in matches
                if sum(1 for ch in m if '一' <= ch <= '鿿') >= 3
                and not re.match(r'[的了着过在和是]', m[-1])]  # unlikely idiom end
    total = len(cleaned)
    per_500 = round(len(filtered) / (total / 500), 1) if total else 0
    return {
        'four_char_count_raw': len(matches),
        'four_char_count_filtered': len(filtered),
        'per_500_chars': per_500,
        'note': 'Upper-bound estimate. Not all 4-char sequences are idioms.',
    }


# ── adjective / adverb density (POS tagging) ────────────────────

def adjective_adverb_stats(text: str) -> dict:
    words = [(w, flag) for w, flag in pseg.cut(text) if not w.isspace()]
    adj_count = sum(1 for _, flag in words if flag == 'a')
    adv_count = sum(1 for _, flag in words if flag == 'd')
    total = len(re.sub(r'\s', '', text))
    per_300 = round((adj_count + adv_count) / (total / 300), 1) if total else 0
    return {
        'adjective_count': adj_count,
        'adverb_count': adv_count,
        'combined_per_300_chars': per_300,
    }


# ── description ratio ───────────────────────────────────────────

ENV_KEYWORDS = re.compile(
    r'(天[空气]|阳光|月[光色]|风|云|雨|雪|雾|星|'
    r'山|河|湖|海|树|花|草|路|街|巷|楼|屋|房间|'
    r'灯|光[线芒]|暗|荫|影|窗户|门|墙|地板|天花|'
    r'桌椅|沙发|床|柜|帘|气味|声音|温度|寒冷|炎热|潮湿|干燥)'
)
PSYCH_KEYWORDS = re.compile(
    r'(想[着到]|觉得?|感到?|意识[到]?|注意到?|明白|知道|'
    r'心里|心底|心中|心头|脑海|思绪|回忆|记[得]|'
    r'犹豫|挣扎|决定|打算|准备|'
    r'担心|害怕|恐惧|愤怒|悲伤|痛苦|快乐|喜悦|满足|失望|后悔)'
)

def description_stats(text: str) -> dict:
    cleaned = re.sub(r'\s', '', text)
    total_chars = len(cleaned)
    if total_chars == 0:
        return {}

    # Environment keywords
    env_matches = ENV_KEYWORDS.findall(cleaned)
    env_char_estimate = len(env_matches) * 30  # rough: each keyword anchors ~30 chars of description

    # Psychology keywords
    psych_matches = PSYCH_KEYWORDS.findall(cleaned)
    psych_char_estimate = len(psych_matches) * 25

    return {
        'env_keyword_hits': len(env_matches),
        'env_ratio_estimate': round(env_char_estimate / total_chars, 4),
        'psych_keyword_hits': len(psych_matches),
        'psych_ratio_estimate': round(psych_char_estimate / total_chars, 4),
    }


# ── body emotion density ────────────────────────────────────────

BODY_PARTS = re.compile(r'[眼目][睛神瞳眶底]?|手[心指标掌背]?|心[里头底中]|'
                         r'喉咙?|眉[头毛]|指[尖节]|嘴[角唇]|拳[头]|'
                         r'脸[色颊]|额[头角]|胸[口膛]|腿|脚[步]|'
                         r'身体|脊背|后背')
EMOTION_SUFFIX = re.compile(r'(一[沉紧颤抖缩松暖寒冷热酸]|'
                             r'微微?[一颤动跳抖缩沉]|'
                             r'发[颤抖热凉冷酸麻]|'
                             r'变得|泛起|涌上|传来)')

def body_emotion_stats(text: str) -> dict:
    cleaned = re.sub(r'\s', '', text)
    total = len(cleaned)
    if total == 0:
        return {}

    # Count body part + emotion combos
    body_hits = len(BODY_PARTS.findall(cleaned))
    # Simple heuristic: body part + nearby emotion suffix within 5 chars
    combo_count = 0
    for m in BODY_PARTS.finditer(cleaned):
        end = m.end()
        nearby = cleaned[end:end+6]
        if EMOTION_SUFFIX.match(nearby):
            combo_count += 1

    per_500 = round(combo_count / (total / 500), 1)
    return {
        'body_part_hits': body_hits,
        'body_emotion_combos': combo_count,
        'per_500_chars': per_500,
    }


# ── structural tic matching ─────────────────────────────────────

TIC_PATTERNS = [
    {'name': '不是而是句式', 'pattern': r'不是.{1,20}(而是|，是|,是)', 'threshold': 3, 'severity': 'high'},
    {'name': '没有X只是Y句式', 'pattern': r'没有.{1,20}(只不过|只是|而是)', 'threshold': 3, 'severity': 'medium'},
    {'name': '否定-纠正句式', 'pattern': r'(不[,，]?\s*不是这样|其实并非如此|更准确[地性]说|不[,，]?\s*[他她它那这])', 'threshold': 2, 'severity': 'high'},
    {'name': '破折号解释句式', 'pattern': r'——(他|她|它|这|那)', 'threshold': 5, 'severity': 'medium'},
    {'name': '公式化副词', 'pattern': r'(不由得|不禁|忍不住|不由自主地|下意识地|鬼使神差地)', 'threshold': 4, 'severity': 'high'},
    {'name': '一边一边句式', 'pattern': r'一边.{1,20}一边', 'threshold': 2, 'severity': 'medium'},
    {'name': '就在这时句式', 'pattern': r'(就在这时|正在这时|突然[,，])', 'threshold': 5, 'severity': 'medium'},
    {'name': '身体部位情绪模板', 'pattern': r'(眼神|目光|瞳孔|心头|心里|心中|心底|手心|指尖|喉咙).{0,10}(一|微|暗|沉|紧|颤|抖|缩|松|暖|寒|凉|热|酸)', 'threshold': 6, 'severity': 'high'},
]

def structural_tic_stats(text: str) -> list[dict]:
    results = []
    for tic in TIC_PATTERNS:
        matches = re.findall(tic['pattern'], text)
        results.append({
            'name': tic['name'],
            'hits': len(matches),
            'current_threshold': tic['threshold'],
            'severity': tic['severity'],
            'suggested_threshold': min(len(matches) + 2, tic['threshold'] + 3),
        })
    return results


# ── paragraph opening variety ───────────────────────────────────

def paragraph_opening_stats(text: str) -> list[dict]:
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    openings = Counter()
    for p in paragraphs:
        first_char = p[:2] if len(p) >= 2 else p[:1]
        if re.match(r'[一-鿿]', first_char[0]):
            openings[first_char] += 1
    total = openings.total()
    if total == 0:
        return []
    return [{'char': k, 'ratio': round(v / total, 4)} for k, v in openings.most_common(15)]


# ── chapter boundary detection ──────────────────────────────────

CHAPTER_HEADER = re.compile(r'^第[零一二三四五六七八九十百千\d]+[章节卷].*$', re.MULTILINE)

def chapter_count(text: str) -> int:
    return max(len(CHAPTER_HEADER.findall(text)), 1)


# ── main ────────────────────────────────────────────────────────

def analyze(path: str) -> dict:
    text = load_and_clean(path)
    sentences = split_sentences(text)
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]

    print(f"文本统计: {len(text):,} 字符, {len(sentences)} 句, {len(paragraphs)} 段, ~{chapter_count(text)} 章")
    print("分析中...")

    metrics = {
        'source': {'path': path, 'total_chars': len(re.sub(r'\s', '', text)), 'approx_chapters': chapter_count(text)},
        'sentence_length': sentence_length_stats(sentences),
        'sentence_openings_top20': sentence_opening_stats(sentences),
        'paragraph': paragraph_stats(text, sentences),
        'dialogue': dialogue_stats(text),
        'punctuation': punctuation_stats(text),
        'word_frequency': word_frequency_stats(text),
        'idiom_density': idiom_stats(text),
        'adjective_adverb_density': adjective_adverb_stats(text),
        'description_ratio': description_stats(text),
        'body_emotion_density': body_emotion_stats(text),
        'structural_tic_usage': structural_tic_stats(text),
        'paragraph_opening_variety': paragraph_opening_stats(text),
    }
    return metrics


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else 'style-metrics.yaml'

    metrics = analyze(input_path)

    # Write YAML with readable formatting
    Path(output_path).write_text(
        yaml.dump(metrics, allow_unicode=True, default_flow_style=False, sort_keys=False),
        encoding='utf-8'
    )
    print(f"已输出: {output_path}")


if __name__ == '__main__':
    main()
