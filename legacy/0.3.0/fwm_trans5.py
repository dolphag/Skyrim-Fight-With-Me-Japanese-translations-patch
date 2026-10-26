# -*- coding: utf-8 -*-
# Fight With Me 0.3.0 で追加・文言変更された表示文字列の訳 (Paths 関連の文字列は今回訳さない)
T5 = {
    # --- 文言が変わった既存の文 ---
    "Stay at your side, weapons out, and fight from there: melee takes whatever comes near you, ranged shoots the nearest enemy.":
        "武器を構えてあなたのそばに留まり、そこから戦います。近接の従者はあなたに近づく敵を、遠距離の従者は最も近い敵を迎え撃ちます。",
    "A Healer holds any spell, with attack spells up to {}":
        "ヒーラーは、どんな魔法でも手に持てます（攻撃魔法は{}まで）",
    "Role strength, role guessing, what happens before a fight and standing down back to their defaults. Companions' orders are not touched.":
        "役割の強さ、役割の推定、戦闘前の動作、戦闘解除を初期値に戻します。従者への命令は変更されません。",
    "The spells you can give a healer's hands on their sheet: any heal, ward, armor, cloak or summons, and attack spells up to Novice, then Apprentice from level 10 and Adept from 25, never Expert or Master. On: attack spells of any strength too.":
        "ヒーラーの手に持たせられる魔法：回復・防護・鎧・マント・召喚の各魔法と、素人までの攻撃魔法（レベル10から見習い、25から精鋭）。熟練者と達人は不可。オンにすると、どんな強さの攻撃魔法でも持たせられます。",
    "With me (what To me! gives everyone): they keep this close to you and fight from there. Melee companions take anything that comes near you; archers and casters shoot the nearest enemy, however far.":
        "随伴（「集合！」で全員に与えられる位置取り）：あなたからこの距離以内に留まり、そこから戦います。近接の従者はあなたに近づく敵を、アーチャーと術者は距離を問わず最も近い敵を迎え撃ちます。",
    "Healing auras, protective barriers, wind and earth bursts, and weapon particles for abilities. Red marks enemies held by a taunt. Requires Triumvirate, Elemental Destruction Magic Redux and Vibrant Weapons (Fire Frost Shock); missing sources use simpler vanilla effects.":
        "回復のオーラ、防護の障壁、風と大地の衝撃波、武器のパーティクルなど、アビリティの演出効果です。挑発で引きつけた敵は赤くなります。Triumvirate、Elemental Destruction Magic Redux、Vibrant Weapons - Fire Frost Shock が必要です。足りないものは、より簡素なバニラの効果になります。",
    "Abilities": "アビリティ",
    "Volley! {} looses {} arrows at {}.": "一斉射撃！{0}が{2}に矢を{1}本放った。",
    "Volley: {} arrows at {}.": "一斉射撃：{1}に矢を{0}本。",
    "{} heals {}: {}.": "{}が{}を回復した：{}。",
    "Healed {}: {} each.": "{}を回復：{}ずつ。",
    "+{:.0f} health": "体力+{:.0f}",
    "Could not cast it.": "魔法を使えませんでした。",
    "{} wards you and {} more: {}.": "{}があなたと他{}人を護った：{}。",
    "They carry no special ability right now.": "今は使えるアビリティがありません。",
    "\nHolds level {} and below  ·  {:.0f} reach  ·  {:.0f} stamina":
        "\nレベル{}以下を確実に引きつける  ·  射程{:.0f}  ·  スタミナ{:.0f}",
    # --- 役割 ---
    "{}\n{}\nRoles are set out of a fight: open the plan with nobody fighting to change it.":
        "{}\n{}\n役割は戦闘外で設定します：誰も戦っていないときにプランを開いて変更してください。",
    "SET OUT OF A FIGHT": "戦闘外で設定",
    "Roles are set out of a fight.": "役割は戦闘外で設定します。",
    # --- オートバトル / 視認 ---
    "AUTO BATTLE": "オートバトル",
    "Auto battle": "オートバトル",
    "they start the fight": "自分から戦闘を始める",
    "they wait to be attacked": "攻撃されるまで待つ",
    "\nEither way, weapons come out when an enemy is in view.": "\nどちらの場合も、敵が視界に入ると武器を構えます。",
    "Auto battle: {}\nOn: a companion who sees an enemy starts the fight. Those on Hold back wait, and nobody starts one while you sneak.\nOff: they wait until an enemy attacks, or you do.{}":
        "オートバトル：{}\nオン：敵を見つけた従者が戦闘を始めます。後方待機の従者は待機し、あなたが隠密中は誰も始めません。\nオフ：敵に攻撃されるか、あなたが攻撃するまで待ちます。{}",
    "on: a companion who sees an enemy starts the fight": "オン：敵を見つけた従者が戦闘を始める",
    "off: they wait for the fight to come to them": "オフ：戦闘が向こうから来るのを待つ",
    "Auto battle on: whoever sees an enemy starts the fight.": "オートバトル オン：敵を見つけた従者が戦闘を始めます。",
    "Auto battle off: they wait for the fight to come to them.": "オートバトル オフ：戦闘が向こうから来るのを待ちます。",
    "Before a fight": "戦闘前",
    "Out of a fight, an enemy that a companion or you can see brings their weapons out. They put them away a few seconds after the last one is out of view, unless yours are out.":
        "戦闘外でも、従者かあなたが敵を視認すると、武器を構えます。最後の敵が視界から消えて数秒後に武器をしまいます。ただし、あなたが武器を出している間はしまいません。",
    "Weapons out when an enemy is in view": "敵が視界にいる間は武器を構える",
    "A companion who sees an enemy starts the fight instead of waiting to be attacked. Companions on Hold back wait, and nobody starts one while you sneak. Also a switch at the top right of the battle plan.":
        "敵を見つけた従者は、攻撃されるのを待たずに戦闘を始めます。後方待機の従者は待機し、あなたが隠密中は誰も始めません。バトルプラン右上のスイッチでも切り替えられます。",
    "How far away an enemy can be and still count as in view. 2500 is about a long bowshot.":
        "視界にいるとみなす敵の最大距離。2500は弓の長射程くらいです。",
    "Sight range": "視認距離",
    # --- テーマ ---
    "Theme": "テーマ",
    "Vanilla: charcoal and silver. Oxblood: the original red. Nordic: engraved stone, beveled metal and inset highlights. All use the same windows and controls. Applies to the battle plan, Paths, notices and these settings.":
        "Vanilla：チャコールとシルバー。Oxblood：従来の赤。Nordic：彫刻を施した石、面取りした金属、はめ込みの強調。どれも同じウィンドウと操作です。バトルプラン、Paths、通知、これらの設定に反映されます。",
}
