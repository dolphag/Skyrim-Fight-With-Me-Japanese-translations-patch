Fight With Me - Japanese Translations Patch 0.5.0-2 (for Fight With Me 0.5.0)
=====================================================================
A Japanese translation for Fight With Me 0.5.0. The original keeps its messages in external text files; this patch is the Japanese version of those files, so no DLL is changed (just files to place).
This is different from the old patch (0.3.0-2 and earlier), which replaced a DLL. If you used the old one, remove it first.
Original mods:
- Fight With Me        https://www.nexusmods.com/skyrimspecialedition/mods/194766
- Path of the Companions (Paths, optional companion)  https://www.nexusmods.com/skyrimspecialedition/mods/196635
Original author: hashhbbrown (GitHub: fatalCMD)

Requirements
- Fight With Me 0.5.0
- SKSE Menu Framework 3 with Japanese enabled: [Fonts] EnableJapanese = true, PrimaryFont = NotoSansJP-Medium.ttf (or similar) in SKSEMenuFramework.ini.
- A Japanese font: included in this patch (see "Japanese font (included)" below).
If you also use Path of the Companions (Paths)
Paths is a separate mod that works without Fight With Me (Fight With Me is an optional companion). If you use Paths, install the Path of the Companions Japanese Translations Patch (a separate page) too. Its translation already contains most of this mod's screen texts; having both is fine (for shared texts this patch is read later and wins).

Japanese font (included)
The original draws its screens with theme fonts (Lora / Spectral / BarlowSemiCondensed) that have no Japanese glyphs, so Japanese would show as "?".
This patch includes a Japanese-capable font under the same names (based on Noto Sans JP, SIL OFL; full text in FONT-LICENSE.txt); it replaces the original's fonts.
Mod order: original -> this patch, so the font wins over the original's fonts. Latin letters will look different too.
To use your own font, disable the three files in SKSE/Plugins/Fonts/ of this patch and put a Japanese-capable TTF under the same three names.
The Path of the Companions Japanese patch contains the same font (identical files, so having both is fine; if you are asked to overwrite, either choice is the same).

Recommended: [Fonts] EnableChinese = true (SMF v3.18+), so kanji outside the Japanese glyph range in game-supplied strings (spell and companion names) do not show as "?".

If it stays English
The language follows the game (sLanguage in Skyrim.ini). FightWithMe_JAPANESE.txt is read when it is JAPANESE; FightWithMe_JA_ENGLISH.txt, a copy of the same content, is read when it is ENGLISH (an English game that was Japanized, for example). Either way, just placing the files is enough.
For any other language name (FRENCH, ...), add this to SKSE/Plugins/FightWithMe_user.ini (create it if missing; restart the game):
    [Interface]
    sLanguage = JAPANESE
This setting only affects the texts of Fight With Me's own screens. It does not affect SKSE Menu Framework as a whole, the game's language, or strings that come from the game (spell names, ...).
The SKSE log should show "[Text] JAPANESE: N lines from ..." (or "[Text] ENGLISH: ..." in an English setup) if the files were read.

Install
Install as a mod (MO2, Vortex, ...). Files placed:
SKSE/Plugins/FightWithMe/Translations/FightWithMe_JAPANESE.txt    Fight With Me's screens (battle plan, settings, notices)
SKSE/Plugins/FightWithMe/Translations/FightWithMe_JA_ENGLISH.txt    the same content, read when the language is ENGLISH
SKSE/Plugins/Fonts/Lora-SemiBold.ttf, Spectral-SemiBold.ttf, BarlowSemiCondensed-SemiBold.ttf    a Japanese-capable font (replaces the original fonts of the same names)
FONT-LICENSE.txt    the font's license (SIL OFL)
No DLL, INI or save is touched; disable it to go back to English.
When the original updates you do not have to remove the patch, but new texts stay in English until the patch is updated. Keep versions matched: the version follows the original, with a suffix (x.x.x-1) for patch-only fixes.

SHA-256 of the text files:
  FightWithMe_JAPANESE.txt       {SHA_JA}

What is not in Japanese
- The role / focus / position dropdowns on the Party settings page (the choices and their hover tooltips): the original does not read their text from its external message files, so they stay English until it is fixed upstream.
- Theme names (Vanilla / Oxblood / Nordic) are kept as in the original.
- Key names and button labels (Tab, Esc, ...), logs, INI comments.
- Strings that come from the game or other mods (spell and companion names).
- Texts the original added after this version.

Rights, source and credits
Original author: hashhbbrown (GitHub: fatalCMD). All original strings, trees and game design belong to the author.
This unofficial translation follows the permissions shown on the Fight With Me page (checked by the user on 2026-10-26: modification and asset use allowed with credit; re-uploading the file elsewhere is not allowed).
This patch contains no file of the originals (no DLL or images), only the original's English strings (the left column of the message files), the Japanese translation and a Japanese font.
Distributed on Nexus Mods only, as a translation page. Please do not re-upload it. GitHub holds only the source (scripts and the translation table), not these files or the font.
Please do not contact the original author about problems with this patch. It will be removed promptly if the author asks. No warranty.
Original source (declared GPL-3.0-or-later): https://github.com/fatalCMD/potc
Scripts and translation table: https://github.com/dolphag/Skyrim-Fight-With-Me-Japanese-translations-patch
The Japanese translation and scripts are GPL-3.0-or-later; the English column is the original author's and is not covered.
The Japanese font (included) is based on Noto Sans JP (Copyright 2014-2021 Adobe) with its internal names changed; SIL Open Font License 1.1, full text in FONT-LICENSE.txt.

AI disclosure
The translation and this text were made with AI assistance (Claude, Anthropic). Checked in game, but mistakes may remain; please report them in the Nexus comments.

Changelog
0.5.0-2: Works in a game set to English (sLanguage=ENGLISH) too: just place the files (added a copy of the same content that is read when the language is ENGLISH).
0.5.0-1: For Fight With Me 0.5.0 (battle plan, settings and notices translated). Unlike the old patch (0.3.0-2 and earlier) it does not replace a DLL; remove the old one first.
0.3.0-2: Paths 0.1.0 translated (tree screens, all 88 nodes, ranks, bonuses, guide, settings, notices). "Skill" unified as "アビリティ". Text position and wrapping adjusted on the Paths screens.
0.3.0-1: Updated for Fight With Me 0.3.0 (auto battle, the abilities section, reworded role/position tooltips, healer heal notices, Volley notices, sight range and theme are translated). Paths is not translated yet.
0.2.0-1: Updated for Fight With Me 0.2.0 (healer rework, magicka rejuvenation, spell picker and bracing states are translated).
0.2.0 series is for Fight With Me 0.2.0.
0.1.5 series (last: 0.1.5-4) is for Fight With Me 0.1.5.
0.1.5-4: Fixed the overhead-view control hint "LS Move" showing "移?" (the last character was cut off).
0.1.5-3: The label over your own character in the overhead view now reads "あなた" (YOU) and is lifted so it no longer overlaps the ring.
0.1.5-2: Fixed "AUTO" on the skill tiles and "LEVEL" on the companion panel partly showing "?", and truncated reasons for unavailable roles.
0.1.5-1: Replaced kanji that showed as "?" (the font cannot draw them); translated the missing tooltip on the overhead-view tab;
         reordered the potion-brewed notice for Japanese; relabelled "Attacking you / the party" as "attackers of you / the party";
         enlarged battle plan text (about 1.2x -> 1.4x) and widened the spacing under the RESISTANCE heading.
0.1.5  : First release.
