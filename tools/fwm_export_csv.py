# -*- coding: utf-8 -*-
"""翻訳表 translations_en_ja.csv を作る: DLL に実際に反映された英語(fwm_patch.py の <report>.sites)と、その日本語訳。
使い方: python3 -I tools/fwm_export_csv.py report.json.sites > translations_en_ja.csv
Paths の長文は、折り返し用に挿入した半角スペースを除いた訳(T6_RAW)を出す。"""
import csv, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fwm_trans1 import T1
from fwm_trans2 import T2
from fwm_trans3 import T3
from fwm_trans4 import T4
from fwm_trans5 import T5
from fwm_trans6 import T6_RAW
T = {**T1, **T2, **T3, **T4, **T5, **T6_RAW}
used = []
for e in json.load(open(sys.argv[1], encoding='utf-8')):
    if e['en'] not in used: used.append(e['en'])
sys.stdout.reconfigure(encoding='utf-8-sig', newline='')
w = csv.writer(sys.stdout, lineterminator='\n')
w.writerow(['en', 'ja'])
for en in used: w.writerow([en, T[en]])
