Path of the Companions - Japanese Translations Patch 1.0.0-1 (for Path of the Companions 1.0.0)
=====================================================================
A Japanese translation for Path of the Companions 1.0.0. It uses the original's own translation-file feature, so no DLL is changed (just files to place).
Versions up to 0.3.0 replaced a DLL. The original added translation files in 0.5.0 / 1.0, so the method changed. Do not use this together with the old (0.3.0-2 or earlier) patch.
Original mods:
- Fight With Me        https://www.nexusmods.com/skyrimspecialedition/mods/194766
- Path of the Companions (Paths)  https://www.nexusmods.com/skyrimspecialedition/mods/196635
Original author: hashhbbrown (GitHub: fatalCMD)

Requirements
- Path of the Companions 1.0.0 and POTC Effects 1.0.21 or newer (required by the original)
- Fight With Me 0.5.0 (optional; if you use it, install the Fight With Me Japanese patch too)
- SKSE Menu Framework 3 with Japanese enabled: [Fonts] EnableJapanese = true, PrimaryFont = NotoSansJP-Medium.ttf (or similar) in SKSEMenuFramework.ini.
- The separate file "Japanese UI Font". **Without it Japanese shows as "?".** The original draws its screens with theme fonts (Lora / Spectral / BarlowSemiCondensed) that have no Japanese glyphs; the font file has the same names with Japanese glyphs (based on Noto Sans JP, SIL OFL).
  Mod order: original -> this patch -> Japanese UI Font, so the font wins over the original's fonts.
Recommended: [Fonts] EnableChinese = true (SMF v3.18+), so kanji outside the Japanese glyph range in game-supplied strings (spell and companion names) do not show as "?".

If it stays English
The language follows the game (sLanguage in Skyrim.ini); the files are read when it is JAPANESE. If your game is not set to JAPANESE, add this to SKSE/Plugins/FightWithMe_user.ini and SKSE/Plugins/FightWithMePaths_user.ini (both) (create them if missing; restart the game):
    [Interface]
    sLanguage = JAPANESE
The SKSE log should show "[Text] JAPANESE: N lines from ..." if the files were read.

Install
Install as a mod (MO2, Vortex, ...). Files placed:
SKSE/Plugins/FightWithMe/Translations/FightWithMe_JAPANESE.txt         Fight With Me's screens (battle plan, settings, notices) and the shared part of the Paths panel
SKSE/Plugins/FightWithMe/Translations/FightWithMePaths_JAPANESE.txt    the Paths trees, abilities and traits
No DLL, INI or save is touched; disable it to go back to English.
When the original updates you do not have to remove the patch, but new texts stay in English until the patch is updated. Keep versions matched: the version follows the original, with a suffix (x.x.x-1) for patch-only fixes.

SHA-256 of the translation files:
  FightWithMe_JAPANESE.txt       {SHA_FWM_JA}
  FightWithMePaths_JAPANESE.txt  {SHA_PATHS_JA}

What is not in Japanese
- The role / focus / position dropdowns on the Party settings page (the choices and their hover tooltips): the original does not pass them through its translation feature, so they stay English until it is fixed upstream.
- Theme names (Vanilla / Oxblood / Nordic) are kept as in the original.
- Key names and button labels (Tab, Esc, ...), logs, INI comments.
- Strings that come from the game or other mods (spell and companion names).
- Texts the original added after this version.

Rights, source and credits
Original author: hashhbbrown (GitHub: fatalCMD). All original strings, trees and game design belong to the author.
This unofficial translation follows the permissions shown on the original pages (checked by the user on 2026-10-26):
- Fight With Me: modification and asset use allowed with credit; re-uploading the file elsewhere is not allowed.
- Path of the Companions: modification, asset use and uploading to other sites allowed with credit.
This patch contains no file of the originals (no DLL, images or fonts), only the original's English strings (the left column of the translation files) and the Japanese translation.
Distributed on Nexus Mods only, as a translation page. Please do not re-upload it. GitHub holds only the source (scripts and the translation table), not these files or the font.
Please do not contact the original author about problems with this patch. It will be removed promptly if the author asks. No warranty.
Original source (declared GPL-3.0-or-later): https://github.com/fatalCMD/potc
Scripts and translation table: https://github.com/dolphag/Skyrim-Fight-With-Me-Japanese-translations-patch
The Japanese translation and scripts are GPL-3.0-or-later; the English column is the original author's and is not covered.
The Japanese font (separate file) is based on Noto Sans JP (Copyright 2014-2021 Adobe) with its internal names changed; SIL Open Font License 1.1, full text in FONT-LICENSE.txt.

AI disclosure
The translation and this text were made with AI assistance (Claude, Anthropic). Checked in game, but mistakes may remain; please report them in the Nexus comments.

Changelog
1.0.0-1: For Path of the Companions 1.0.0. Paths is now a mod of its own, so the method changed: no DLL replacement any more; the Japanese text goes into the original's translation file. All nodes, the guide, settings and notices are translated.
(0.1.0-1 and earlier replaced a DLL in the old way.)
0.1.0-1: First release. Translates Paths 0.1.0 (tree screens, all 88 nodes, ranks, bonuses, guide, settings, notices). The DLL is the same as in the Fight With Me Japanese patch 0.3.0-2.
(For the Fight With Me side, see the changelog on the Fight With Me Japanese patch page.)
