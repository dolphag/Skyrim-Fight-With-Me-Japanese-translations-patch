# Fight With Me / Paths - Japanese Translations Patch (tools and translation table)

Nexus Mods pages:
- Fight With Me Japanese patch: <https://www.nexusmods.com/skyrimspecialedition/mods/194874>
- Paths Japanese patch: *(page not yet created; link will be added here)*

Sister patch (Walk With Me): <https://www.nexusmods.com/skyrimspecialedition/mods/194872>, tools in <https://github.com/dolphag/Skyrim-Walk-With-Me-Japanese-translations-patch>

[日本語は下](#日本語)

Scripts and the translation table for the Japanese translation patch for
[Fight With Me](https://www.nexusmods.com/skyrimspecialedition/mods/194766) **0.3.0** and its add-on
[Paths](https://www.nexusmods.com/skyrimspecialedition/mods/195610), both by **hashhbbrown** (GitHub: fatalCMD).
Paths' text lives inside `FightWithMe.dll`, so one patched DLL covers both mods.
The patched `FightWithMe.dll` is distributed **only on Nexus Mods** (as a translation page of each original),
following the permissions on the original pages. **This repository is source code only: it contains no DLL and no code of Fight With Me or Paths**:
only the scripts that patch a DLL you own, and the English → Japanese table (745 pairs).

## Credits
- **Fight With Me** and **Paths**: created by **hashhbbrown** (GitHub: [fatalCMD](https://github.com/fatalCMD)). All original strings, perk trees and game design belong to the author.
  - Fight With Me: <https://www.nexusmods.com/skyrimspecialedition/mods/194766> / <https://github.com/fatalCMD/fight-with-me>
  - Paths: <https://www.nexusmods.com/skyrimspecialedition/mods/195610> / <https://github.com/fatalCMD/paths-fwm-addon>
- Japanese translation, tools and layout fixes: dolphag (with AI assistance, see Notes).

## Files
- [`PATHS_TABLE.md`](PATHS_TABLE.md): comparison table of all 88 Paths perk nodes (English / Japanese / effect / unlock / cooldown), terminology and naming notes. Feedback welcome.
- `translations_en_ja.csv`: all 745 string pairs.
- `tools/`: patcher, verifier, translation sources (`fwm_trans1..6.py`, `fwm_names6.py`) and helpers.

## Versions
- Original DLL SHA-256: `a2ea378348e6912bc391f0a33d8340bea14ce21e24118279857cef592402ad86`
- Expected output SHA-256 (patch 0.3.0-2): `203d62f403a8d86eb0ab82d99a43bd5daa25c9a3523ec8ce3b6f5177b3accd1d`
- Original source (for reference): <https://github.com/fatalCMD/fight-with-me> (the 0.3.0 DLL matches commit `6a5f5ce`, one commit after `f7f6e93` "Fight With Me 0.3.0"; addresses were re-derived from the 0.3.0 binary, using signature search against the 0.2.0 addresses)

Load order for users: Fight With Me → Paths → Japanese patch (the patched `FightWithMe.dll` must win).

## How it works (short)
A new section (`.jpn`, read+execute) holds the Japanese strings and a few stubs. `lea reg,[rip+disp]` references,
`.rdata` pointer slots (relocation-checked) and fmt length immediates are retargeted; inline-expanded
`std::string` constructions are replaced by a call to the string constructor (register liveness is checked).
Label/LabelWidth draw one byte at a time and break UTF-8, so calls are redirected to stubs that use Text/TextSize
when the string contains non-ASCII bytes; Japanese text is enlarged by `FONT_SCALE` (1.4) except for the title,
the tooltip's size/width constants are scaled together (`TIP_SCALE`, 1.2) so its box fits, and spacing constants and
per-call-site vertical lifts (`SPACING_CONSTS`, `LABEL_LIFT`, `TEXT_LIFT`) keep text aligned with icons and bands.
The Paths descriptions are wrapped at bunsetsu boundaries (ImGui wraps only at ASCII spaces) using janome.
The build fails if a translation uses a kanji outside the font range (`tools/jp_kanji.txt`; such kanji would show as "?").

## Reproduce (Python 3.11+, `pip install pefile capstone unicorn janome`)
```
python3 -I tools/fwm_fmtcheck.py                                  # format-string field check
python3 -I tools/fwm_patch.py FightWithMe.dll out.dll report.json   # original DLL -> patched DLL
python3 -I tools/fwm_verify.py FightWithMe.dll out.dll              # independent static verification
python3 -I tools/fwm_emu_stub.py out.dll report.json                # dispatch/scale check of the stubs (unicorn)
python3 -I tools/fwm_scan_flag.py ...                               # register-reuse hazard scan (known false positives documented)
python3 -I tools/fwm_export_csv.py ...                              # regenerate translations_en_ja.csv
python3 -I tools/paths_table.py <FWM include/FWM/Paths.h> > PATHS_TABLE.md
```

## Notes
- For 0.3.0 only (addresses are fixed). The 0.2.0 scripts are in the git history (commit `6069193`, tag `v.0.2.0`); the 0.1.5 scripts are in the history up to commit `0ab3065`; the 0.1.0 scripts are in tag `v0.1.0`.
- Terminology: "skill" is rendered as アビリティ (Ability) everywhere, including Fight With Me's own UI, to avoid confusion with vanilla skills. This changes wording from patch 0.3.0-1.
- Log lines are intentionally left in English.
- Translations were produced with AI assistance (Claude, Anthropic) and checked in game.
- The scripts and the Japanese column of the table are mine and are provided under GPL-3.0-or-later, as stated in [`LICENSE`](LICENSE).
  The English column reproduces strings of Fight With Me and Paths, which belong to their author (neither original repository ships a license file); it is included only so that the patch can be reproduced, and is not covered by that license.
  Paths' Nexus page permits modification and asset use with credit to the author, and forbids uploading the file elsewhere; hence no binaries here.
- This repository was split off from the Walk With Me patch repository (where the first release, tag `fwm-0.1.0`, still lives under `fwm/`); the two patches are maintained independently.

## 日本語
Nexus Mods のページ:
- Fight With Me 日本語化パッチ: <https://www.nexusmods.com/skyrimspecialedition/mods/194874>
- Paths 日本語化パッチ: (ページ作成後にリンクを追記します)

姉妹MOD(Walk With Me)のパッチ: <https://www.nexusmods.com/skyrimspecialedition/mods/194872>、ツールは <https://github.com/dolphag/Skyrim-Walk-With-Me-Japanese-translations-patch>

[Fight With Me](https://www.nexusmods.com/skyrimspecialedition/mods/194766) **0.3.0** と、そのアドオン
[Paths](https://www.nexusmods.com/skyrimspecialedition/mods/195610) の日本語化パッチのスクリプトと翻訳表です。
原作者はどちらも **hashhbbrown**(GitHub: fatalCMD)です。Paths の文字列は `FightWithMe.dll` の中にあるため、パッチ済みDLL 1つで両方に対応します。
パッチ済みの `FightWithMe.dll` は、原MODページの権限表示に従い、**Nexus Mods(各原MODの翻訳ページ)でのみ**配布します。
**このリポジトリはソースコードのみで、DLLも Fight With Me / Paths のコードも含みません**。手元のDLLにパッチを当てるスクリプトと、英日対応表(745組)だけです。

### クレジット
- **Fight With Me** / **Paths**: 作者 **hashhbbrown**(GitHub: [fatalCMD](https://github.com/fatalCMD))。原文・パークツリー・ゲームデザインはすべて作者のものです。
  - Fight With Me: <https://www.nexusmods.com/skyrimspecialedition/mods/194766> / <https://github.com/fatalCMD/fight-with-me>
  - Paths: <https://www.nexusmods.com/skyrimspecialedition/mods/195610> / <https://github.com/fatalCMD/paths-fwm-addon>
- 日本語訳・ツール・表示位置の調整: dolphag(AI支援あり)

### 内容
- [`PATHS_TABLE.md`](PATHS_TABLE.md): Paths 全88ノードの対照表(英語/日本語/効果/解放条件/再使用)、用語と命名の覚え書き。ご意見歓迎です。
- `translations_en_ja.csv`: 全745組の英日対応表。
- 再現手順は上の英語の節を参照してください(janome が必要です)。元DLLの SHA-256 は `a2ea378348e6912bc391f0a33d8340bea14ce21e24118279857cef592402ad86`、
  出力DLL(パッチ 0.3.0-2)は `203d62f403a8d86eb0ab82d99a43bd5daa25c9a3523ec8ce3b6f5177b3accd1d` になります。
- ロード順: Fight With Me → Paths → 日本語化パッチ(パッチ済み `FightWithMe.dll` が勝つ順)。
- 用語: 「skill」は、バニラのスキルとの混同を避けるため、Fight With Me 本体のUIも含めて「アビリティ」に統一しました(0.3.0-1 から変更)。
