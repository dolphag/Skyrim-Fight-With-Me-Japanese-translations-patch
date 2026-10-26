# 原作者への報告文案(未送信。送るかはユーザーの判断。送信先: GitHub fatalCMD/potc の Issues、または Nexus のコメント)

確認元: 配布 zip の FWM 0.5.0 / Paths 1.0、原作 git `fatalCMD/potc` commit `17d5032`(配布版より古い可能性あり)。ユーザーの実機の画面でも確認済み(下記 1)。

## 英語(貼り付け用)

Thank you for Fight With Me 0.5.0 and Paths 1.0. The external translation files, the per-character UTF-8 text drawing and the `std::format` placeholders (including positional ones) are close to what I suggested earlier, and I am very grateful you took it on: the Japanese version is now a plain data file instead of a binary patch that I had to redo for every release, and Japanese works well with it.

While making the translation I ran into three small things:

1. **The role / focus / position dropdowns on the Party settings page are not translated.** `RoleName`, `FocusName` and `PositionName` in `src/Menu.cpp` (the `a_name` callbacks of `RosterCombo`) return `roles[i].name.data()` etc. without going through `Tr`. The same names are translated everywhere else (battle plan, HUD), so only these combos stay in English. The hover tooltips of the same combos (`Help(roles[..].summary.data())`, `focuses[..].summary`, `positions[..].summary`, same function) have the same omission. Wrapping them, e.g. `return Trc(roles[...].name.data());`, should be enough (the names are literals).

2. **Some template keys are mojibake** (the middle dot "·" double-encoded): for example keys starting with `  Â·  ` / `  ÃƒÆ’Ã†â€™…` in `FightWithMe_ENGLISH.txt` and `Â·` in `FightWithMePaths_ENGLISH.txt` (`{}x  Â·  {}% bleed`, `{} damage/s Â· {} reach`, ...). English players probably see garbage there too. I translated them keeping the broken key so it still matches, but fixing the source encoding (and the key) would be cleaner.

3. **The theme fonts (`Lora-SemiBold`, `Spectral-SemiBold`, `BarlowSemiCondensed-SemiBold`) are Latin-only**, so CJK text shows as `?` even with `EnableJapanese` on in SKSE Menu Framework. Putting a CJK-capable font under the same file names fixes it. A fallback/merged font (or a note in the Translating section) would help translators. Also, the README's Translating section could mention that translations are loaded by the language name only (files for other languages are ignored).

Not urgent. Thank you for the mod!

## 日本語(ユーザー向けの要約)
0. 前置きの感謝: 以前お願いした内容(翻訳ファイル化、UTF-8 の 1 文字ずつの描画、`std::format` の位置指定つき書式)が 0.5.0 / 1.0 に入っていた。パッチを毎回作り直さずに済むようになった。(確認したのは配布版・原作ソースの挙動。依頼が理由かどうかは断定していない)
1. パーティ設定ページのドロップダウン(役割・注目対象・位置取り)だけ翻訳が当たらない(`Tr` を通していない)。
2. 翻訳テンプレートの一部の鍵が文字化け(「·」の二重エンコード)している。
3. テーマ用フォントがラテン文字のみで、日本語が「?」になる(同名の日本語対応フォントを置くと直る)。
