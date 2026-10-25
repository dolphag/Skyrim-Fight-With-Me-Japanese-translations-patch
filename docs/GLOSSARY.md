# 用語集(FWM / Paths)

決定済みの用語。変更するときは、ユーザーの了承を得て、`tools/fwm_trans*.py` と README・Nexus 文面を同時に直す。

| 英語 | 日本語 | 備考 |
|---|---|---|
| skill(Paths / FWM の能力) | **アビリティ**(Ability) | バニラのスキルと混同しないため。FWM 本体の画面も同じ語に統一(0.3.0-2) |
| skill tree | **ツリー** | 「スキルツリー」は使わない |
| PATHS(画面名) | PATHS - **従者専用ツリー** | 従者ごとのツリー、の意味 |
| IN HAND | **武器** | 「手持ち」は使わない |
| Path of the Blade/Shield/Mender/Hammer/Arrow/Storm | `fwm_names6.py` 参照(刃の道 など) | 実際の訳は `tools/fwm_names6.py` が正。「槌の道」は暫定 |
| Magnus(Storm の最上位) | マグナス | |
| 共通アビリティ(Taunt, Heal, Ward, War cry …) | FWM 本体側の訳に統一 | 挑発、回復 など。T6 の統合順で T6 が勝つ点に注意 |
| 役割名 | ファイター/タンク/ヒーラー/ブルーザー/アーチャー/メイジ | FWM 本体の表記 |

アビリティ名は公式日本語訳に合わせる(Slow Time=時間減速、Healing Hands=治癒の手)。Paths の名称は意訳を含み、一部は暫定。全ノードの対照は `PATHS_TABLE.md`。
