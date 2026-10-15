# Fight With Me - Japanese Translations Patch (tools and translation table)

Nexus Mods page: <https://www.nexusmods.com/skyrimspecialedition/mods/194874>  
Sister patch (Walk With Me): <https://www.nexusmods.com/skyrimspecialedition/mods/194872>, tools in <https://github.com/dolphag/Skyrim-Walk-With-Me-Japanese-translations-patch>

[日本語は下](#日本語)

Scripts and the translation table for the Japanese translation patch for
[Fight With Me](https://www.nexusmods.com/skyrimspecialedition/mods/194766) **0.2.0** (by hashhbbrown).
The patched `FightWithMe.dll` is distributed **only on Nexus Mods** (as a translation of the original page),
following the permissions on the original page. **This repository contains no DLL and no code of Fight With Me**:
only the scripts that patch a DLL you own, and the English → Japanese table (609 pairs).

- Original DLL SHA-256: `009076c92bb0861e011551446e71fb48914dca5d0db21be19f5aff899771864f`
- Expected output SHA-256: `b076d27c7bbb38cf8c28216ccfdcc2e5764eaac0ee344aedd9d12f3c7f75167a`
- Original source (for reference): <https://github.com/fatalCMD/fight-with-me> (the published source was still 0.1.5 (commit `be5808f`) when 0.2.0 was released, so addresses were found by diffing the 0.1.5 and 0.2.0 binaries)

## How it works (short)
A new section (`.jpn`, read+execute) holds the Japanese strings and a few stubs. `lea reg,[rip+disp]` references,
`.rdata` pointer slots (relocation-checked) and fmt length immediates are retargeted; inline-expanded
`std::string` constructions are replaced by a call to the string constructor (register liveness is checked).
Label/LabelWidth draw one byte at a time and break UTF-8, so calls are redirected to stubs that use Text/TextSize
when the string contains non-ASCII bytes; Japanese text is enlarged by `FONT_SCALE` (1.4) except for the title,
the tooltip's size/width constants are scaled together (`TIP_SCALE`, 1.2) so its box fits, and the spacing under the RESISTANCE heading is widened.
The build fails if a translation uses a kanji outside the font range (`tools/jp_kanji.txt`; such kanji would show as "?").

## Reproduce (Python 3.11+, `pip install pefile capstone unicorn`)
```
python3 -I tools/fwm_fmtcheck.py                                  # format-string field check
python3 -I tools/fwm_patch.py FightWithMe.dll out.dll report.json   # original DLL -> patched DLL
python3 -I tools/fwm_verify.py FightWithMe.dll out.dll              # independent static verification
python3 -I tools/fwm_emu_stub.py out.dll report.json                # dispatch/scale check of the stubs (unicorn)
```

## Notes
- For 0.2.0 only (addresses are fixed). The scripts for 0.1.5 are in the git history (up to commit `0ab3065`); the 0.1.0 scripts are in tag `v0.1.0`.
- Translations were produced with AI assistance (Claude, Anthropic) and checked in game (parts added in 0.2.0 are not fully checked in game yet).
- The scripts and the Japanese column of the table are mine and are provided under GPL-3.0-or-later, as stated in [`LICENSE`](LICENSE).
  The English column reproduces strings of Fight With Me, which belong to its author (the original ships without a license file); it is included only so that the patch can be reproduced, and is not covered by that license.
- This repository was split off from the Walk With Me patch repository (where the first release, tag `fwm-0.1.0`, still lives under `fwm/`); the two patches are maintained independently.

## 日本語
Nexus Mods のページ: <https://www.nexusmods.com/skyrimspecialedition/mods/194874>
姉妹MOD(Walk With Me)のパッチ: <https://www.nexusmods.com/skyrimspecialedition/mods/194872>、ツールは <https://github.com/dolphag/Skyrim-Walk-With-Me-Japanese-translations-patch>

[Fight With Me](https://www.nexusmods.com/skyrimspecialedition/mods/194766) **0.2.0** の日本語化パッチのスクリプトと翻訳表です。
パッチ済みの `FightWithMe.dll` は、原MODページの権限表示に従い、**Nexus Mods(原MODの翻訳ページ)でのみ**配布します。
**このリポジトリには、DLLも Fight With Me のコードも含みません**。手元のDLLにパッチを当てるスクリプトと、英日対応表(609組)だけです。
再現手順は上の英語の節を参照してください。元DLLの SHA-256 は `009076c92bb0861e011551446e71fb48914dca5d0db21be19f5aff899771864f`、
出力DLLは `b076d27c7bbb38cf8c28216ccfdcc2e5764eaac0ee344aedd9d12f3c7f75167a` になります。
