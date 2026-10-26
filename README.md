# Fight With Me - Japanese Translations Patch (tools and translation table)

Nexus Mods page: <https://www.nexusmods.com/skyrimspecialedition/mods/194874>

Sister patches: Path of the Companions (Paths) <https://github.com/dolphag/Skyrim-POTC-JP-Patch> (Nexus page: not published yet), Walk With Me <https://www.nexusmods.com/skyrimspecialedition/mods/194872> (tools: <https://github.com/dolphag/Skyrim-Walk-With-Me-Japanese-translations-patch>)

[日本語は下](#日本語)

Scripts and the translation table for the Japanese translation patch for
[Fight With Me](https://www.nexusmods.com/skyrimspecialedition/mods/194766) **0.5.0** by **hashhbbrown** (GitHub: fatalCMD).
Path of the Companions (Paths) is a separate mod and an optional companion of Fight With Me; it has its own patch (repository above).
Fight With Me 0.5.0 reads its messages from external text files (`SKSE/Plugins/FightWithMe/Translations/`); the patch is the Japanese version of that file, so no DLL is changed.
The patch files are distributed **only on Nexus Mods**, following the permissions on the original page.
**This repository is source code only: it contains no files of the original mod, no distribution zips and no fonts**:
only the scripts that build the Japanese message file, and the English → Japanese table.

## Credits
- **Fight With Me**: created by **hashhbbrown** (GitHub: [fatalCMD](https://github.com/fatalCMD)). All original strings and game design belong to the author.
  - Fight With Me: <https://www.nexusmods.com/skyrimspecialedition/mods/194766>
  - Source (declared GPL-3.0-or-later): <https://github.com/fatalCMD/potc>
- Japanese translation, tools and layout fixes: dolphag (with AI assistance, see Notes).
- Japanese UI font (a separate Nexus file, not in this repository): based on Noto Sans JP (Copyright 2014-2021 Adobe), SIL Open Font License 1.1, internal name changed.

## Files
- `translations_en_ja.csv`: all string pairs (822). The English column is the original author's and is not covered by the license of this repository.
- `tools/lang_build.py`: builds `FightWithMe_JAPANESE.txt` from the original zip and the table, with checks (missing translations, format fields, kanji range).
- `tools/make_zip.py`: test and distribution zips. `tools/make_font_pack.py`: renames and copies an OFL Japanese font under the three theme font names (the font itself is supplied by the user and not committed).
- `release/`: README templates and the Nexus text. `docs/`: findings about the original (format, fonts, packaging), glossary, a draft report for the original author (not sent).
- `legacy/0.3.0/`: the tools of the old method (patching `FightWithMe.dll` 0.3.0), kept for reference. They do not work with 0.5.0.

## Versions
Patch versions follow Fight With Me: **0.5.0-1** is for Fight With Me 0.5.0. Earlier versions (0.1.5 to 0.3.0-2) replaced a DLL; see the tags `v0.1.0` ... `v0.3.0-2` and `legacy/0.3.0/`.
Recommended for users: Japanese enabled in `SKSEMenuFramework.ini` (`EnableJapanese = true`), plus `EnableChinese = true` (SMF v3.18+) for kanji outside the Japanese glyph range in game-supplied strings. The separate Japanese UI font file is required (the original's theme fonts have no Japanese glyphs).

## How it works (short)
The original reads `*_<LANGUAGE>.txt` (one line per message: English, a tab, the translation) from the folder and replaces the English by the translation when the language is `JAPANESE` (`sLanguage` in Skyrim.ini, or in `FightWithMe(_user).ini`). The patch is `FightWithMe_JAPANESE.txt`.
Long Japanese lines get ASCII spaces at phrase boundaries (janome), because the UI wraps only at spaces. The build fails if a translation uses a kanji outside the glyph range (`tools/jp_kanji.txt`; such kanji would show as "?").

## Reproduce (Python 3.11+, `pip install -r requirements-dev.txt`)
```
python3 -I tools/lang_build.py --fwm "<Fight With Me zip>" --out out/ja
python3 -I tools/make_font_pack.py --font NotoSansJP-Medium.ttf --license OFL.txt --out out/font
python3 -I tools/make_zip.py release out/ja --version 0.5.0-1
python3 -I tools/make_zip.py font out/font --version 0.5.0-1
```

## Notes
- The role / focus / position dropdowns on the Party settings page are not read from the message files by the original, so they stay English (`docs/upstream-report-draft.md`).
- Log lines, key names and theme names are intentionally left in English.
- Translations were produced with AI assistance (Claude, Anthropic) and checked in game.
- The scripts and the Japanese column of the table are provided under GPL-3.0-or-later, as stated in [`LICENSE`](LICENSE). The English column reproduces strings of Fight With Me, which belong to their author; it is included only so that the patch can be reproduced.
- This repository was split off from the Walk With Me patch repository (where the first release, tag `fwm-0.1.0`, still lives under `fwm/`); the patches are maintained independently. The Path of the Companions patch was in turn split off from this repository on 2026-10-26.

## 日本語
Nexus Mods のページ: <https://www.nexusmods.com/skyrimspecialedition/mods/194874>

姉妹MODのパッチ: Path of the Companions(Paths)<https://github.com/dolphag/Skyrim-POTC-JP-Patch>(Nexus のページは公開前)、Walk With Me <https://www.nexusmods.com/skyrimspecialedition/mods/194872>(ツール: <https://github.com/dolphag/Skyrim-Walk-With-Me-Japanese-translations-patch>)

[Fight With Me](https://www.nexusmods.com/skyrimspecialedition/mods/194766) **0.5.0** の日本語化パッチのスクリプトと翻訳表です。原作者は **hashhbbrown**(GitHub: fatalCMD)。
Path of the Companions(Paths)は別の MOD で、Fight With Me の任意の連携先です。Paths には別のパッチがあります(上のリポジトリ)。
Fight With Me 0.5.0 は、メッセージを外部のテキストファイル(`SKSE/Plugins/FightWithMe/Translations/`)から読みます。本パッチはその日本語版で、DLL は変更しません。
パッチのファイルは、原MODページの権限表示に従い、**Nexus Mods でのみ配布**します。
**このリポジトリはソースコードのみです。原MODのファイル、配布用の zip、フォントは含みません**。日本語のメッセージファイルを作るスクリプトと、英日対応表だけを置いています。

### クレジット
- **Fight With Me**: **hashhbbrown**(GitHub: [fatalCMD](https://github.com/fatalCMD))作。原作のすべての文言・ゲームデザインは原作者のものです。
  - Fight With Me: <https://www.nexusmods.com/skyrimspecialedition/mods/194766>
  - ソース(GPL-3.0-or-later と宣言されています): <https://github.com/fatalCMD/potc>
- 日本語訳・ツール・表示の調整: dolphag(AI の支援あり。上の Notes を参照)。
- 日本語フォント(Nexus の別ファイル。このリポジトリには含みません): Noto Sans JP(Copyright 2014-2021 Adobe)を元に、内部の名前を付け替えたもの。SIL Open Font License 1.1。

### ファイル
- `translations_en_ja.csv`: 英日の全組(822)。英語の列は原作者のもので、このリポジトリのライセンスの対象外です。
- `tools/lang_build.py`: 原作の zip と対応表から `FightWithMe_JAPANESE.txt` を作ります(未訳・書式欄・漢字範囲の検査つき)。
- `tools/make_zip.py`: テスト版と配布用の zip。`tools/make_font_pack.py`: OFL の日本語フォントを、テーマ用フォントの 3 つの名前で書き出します(フォント本体は利用者が用意し、コミットしません)。
- `release/`: README の雛形と Nexus 用文面。`docs/`: 原作の調査(形式・フォント・同梱)、用語集、原作者向け報告の文案(未送信)。
- `legacy/0.3.0/`: 旧方式(`FightWithMe.dll` 0.3.0 を書き換える)のツール。参照用に残しています。0.5.0 には使えません。

### 版
パッチの版は Fight With Me に連動します。**0.5.0-1** は Fight With Me 0.5.0 用です。それ以前(0.1.5〜0.3.0-2)は DLL を差し替える方式でした。タグ `v0.1.0` 〜 `v0.3.0-2` と `legacy/0.3.0/` を参照してください。
利用者への推奨: `SKSEMenuFramework.ini` で日本語を有効にする(`EnableJapanese = true`)。ゲーム由来の文字列の、日本語範囲外の漢字には `EnableChinese = true`(SMF v3.18 以降)。別ファイルの日本語フォントが必須です(原作のテーマ用フォントは日本語を含まないため)。

### しくみ(短く)
原作は、フォルダ内の `*_<言語名>.txt`(1 行 = 英語、タブ、訳)を読み、言語が `JAPANESE` のとき(Skyrim.ini または `FightWithMe(_user).ini` の `sLanguage`)英語を訳に置き換えます。本パッチは `FightWithMe_JAPANESE.txt` です。
画面は半角スペースでしか折り返さないため、長い日本語には文節の切れ目に半角スペースを入れます(janome)。範囲外の漢字を使うと(「?」になるため)ビルドが失敗します(`tools/jp_kanji.txt`)。

### 再現(Python 3.11+、`pip install -r requirements-dev.txt`)
上の「Reproduce」を参照してください。

### 補足
- パーティ設定ページの、役割・注目対象・位置取りのドロップダウンは、原作がメッセージのファイルを通していないため、英語のままです(`docs/upstream-report-draft.md`)。
- ログ・キー名・テーマ名は、意図的に英語のままにしています。
- 訳文は AI(Claude, Anthropic)の支援で作り、ゲーム内で確認しています。
- スクリプトと翻訳表の日本語の列は GPL-3.0-or-later です([`LICENSE`](LICENSE))。英語の列は Fight With Me の文言で、原作者のものです。パッチを再現できるようにするためだけに含めています。
- このリポジトリは Walk With Me のパッチのリポジトリから分けたもので(初版のタグ `fwm-0.1.0` は今もそちらの `fwm/` にあります)、各パッチは独立して保守しています。Path of the Companions のパッチは、2026-10-26 にこのリポジトリから分けました。
