Paths - Japanese Translations Patch 0.1.0-1 (for Paths 0.1.0 / Fight With Me 0.3.0)
=====================================================================
An unofficial Japanese translation patch for Paths (an add-on for Fight With Me).
Paths looks like a separate mod, but the text of its screens is not in Paths: it is inside Fight With Me's FightWithMe.dll.
So this patch replaces the FightWithMe.dll of Fight With Me (it does not modify any Paths file).
As a side effect, Fight With Me's own screens are translated too.
The DLL is identical to the one in the Fight With Me Japanese patch 0.3.0-2; you only need one of them.
Original mods:
- Paths         https://www.nexusmods.com/skyrimspecialedition/mods/195610
- Fight With Me https://www.nexusmods.com/skyrimspecialedition/mods/194766
Original author: hashhbbrown (GitHub: fatalCMD)

[Requirements]
- Paths 0.1.0 and its requirement, Fight With Me 0.3.0
- A Japanese font set up in SKSE Menu Framework 3.
  No extra setup is needed if you already have a Japanese environment. The author tested with the Japanese localization by 2game:
  https://skyrimspecialedition.2game.info/detail.php?id=120352
  (To set it yourself: [Fonts] PrimaryFont = NotoSansJP-Medium.ttf, EnableJapanese = true in SKSEMenuFramework.ini.)
- This patch ships no font, because Fight With Me draws with the SMF3 font.

[Recommended]
- EnableChinese = true under [Fonts] in SKSEMenuFramework.ini (SMF v3.18 or later).
  Strings taken from the game itself (spell and shout names, etc.) cannot be changed by this patch, and kanji outside the Japanese glyph range show as "?".
  Paths is expected to show many such strings, so setting this is recommended (see "If spell names show ?" below).
- Sister patch: Walk With Me - Japanese Translations Patch
  https://www.nexusmods.com/skyrimspecialedition/mods/194872

[Load order]
Fight With Me -> Paths -> this patch. This patch must come last so that the patched FightWithMe.dll wins.

[Versions]
The patch version follows the original mod, Paths (for Paths 0.1.0 -> 0.1.0-1).
The DLL itself is for Fight With Me 0.3.0, so the Fight With Me version must match too.
If the patch alone is fixed within the same version, a suffix such as x.x.x-1 is added.
This file is for Fight With Me 0.3.0 only (fixed addresses). Do not use it with other versions of Paths or Fight With Me.

[Install]
Install above the original mod(s). INI and saves are untouched; disabling the patch restores the original.
Before updating Fight With Me, disable/remove this patch first, or its old DLL overwrites the new one and can cause errors or crashes.

Original DLL SHA-256: {ORIG_SHA}
Patched DLL SHA-256 : {OUT_SHA}

[If spell names show "?"]
Strings taken from the game itself, such as spell names, cannot be changed by this patch. If they contain kanji outside the Japanese glyph range of SKSE Menu Framework (for example 罠 or 痺), they show as "?".
In that case try EnableChinese = true under [Fonts] in SKSEMenuFramework.ini (added in SMF v3.18).
On the author's setup, kanji that show as "?" with the Japanese range (靭, 怯) are displayed with the Chinese setting; 罠 and 痺 have not been checked.

[Translated / not translated]
Settings pages, the battle plan screen, the Paths tree screens (abilities, traits, ranks, bonuses and the guide of every path) and combat notices are translated.
An English/Japanese table of all 88 Paths nodes is in PATHS_TABLE.md on GitHub.
Key names, button labels, logs, INI comments and a few short labels stay in English (they are expanded inline in the code and cannot be replaced safely).
"Skill" is rendered as "アビリティ" (Ability) everywhere, to avoid confusion with vanilla skills (changed from 0.3.0-1; this also changes Fight With Me's own screens).
The Paths screen is titled "PATHS - 従者専用ツリー" (follower-only trees).
Ability names follow the official Japanese Skyrim terms. "Slow Time" is "時間減速" and "Healing Hands" is "治癒の手".
Names of Paths trees and abilities include free renderings, and some are provisional. Feedback is welcome.
SKSE Menu Framework loads only about 3000 kanji, and others would show as "?", so the translations stay within that range.

[Changes to the original]
1. Strings in FightWithMe.dll are replaced with Japanese.
2. The functions that draw text one byte at a time (Label / LabelWidth) are redirected to the normal text functions (Text / TextSize)
   only when the string contains non-ASCII characters. ASCII-only strings behave as in the original.
3. Japanese text is enlarged about 1.4x (Japanese looks smaller than Latin at the same size); titles are not enlarged.
   Tooltips scale their text size and wrap width together (about 1.2x) so the box still fits.
   On the Paths screens, text positions and spacing are adjusted per place so that text lines up with icons and bands.
4. Long Paths descriptions get wrap spaces at phrase boundaries so Japanese text does not run off the box.
5. The Japanese strings and the redirect code live in a section (.jpn) appended to the DLL.

[Rights / source]
The originals ship without a license file. Following the permissions on the original Nexus pages (Fight With Me checked 2026-10-11, Paths checked 2026-10-20:
modification and asset use allowed with credit to the author, re-uploading elsewhere not allowed), this patch is distributed ONLY on Nexus Mods as a translation of each original page. Please do not repost it elsewhere.
GitHub holds source code only (patch scripts and the translation table); no DLL.
It is an unofficial translation made within those permissions; do not ask the original author for support. If the author asks for removal, I will comply promptly.
THIRD-PARTY-NOTICES_FightWithMe.md is included unchanged from the original (Paths ships the same notice text).
Fight With Me source: https://github.com/fatalCMD/fight-with-me (commit 6a5f5ce when checked; the commit that matches the 0.3.0 DLL)
Paths source: https://github.com/fatalCMD/paths-fwm-addon
Patch scripts and translation table (no DLL): https://github.com/dolphag/Skyrim-Fight-With-Me-Japanese-translations-patch (one tag per version)
No warranty.

[AI disclosure]
Translations and this text were produced with AI assistance (Claude, Anthropic).
Checked in game, but something may have been missed; please report mistranslations or layout problems in the Nexus comments.

[Thanks]
Huge thanks to hashhbbrown for creating and sharing Fight With Me and Paths.
This is an unofficial translation made with gratitude so Japanese players can enjoy it too.

Changelog
0.1.0-1: First release. Translates Paths 0.1.0 (tree screens, all 88 nodes, ranks, bonuses, guide, settings, notices). The DLL is the same as in the Fight With Me Japanese patch 0.3.0-2.
(For the Fight With Me side, see the changelog on the Fight With Me Japanese patch page.)
