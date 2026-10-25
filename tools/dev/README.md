# tools/dev — 調査用の補助スクリプト (scratch)

パッチの**作成時**に原DLLを調べるための使い捨てに近いスクリプトです。パッチの生成・検証(`tools/fwm_*.py`)には不要です。
**原DLLや逆アセンブル結果は、このリポジトリに含めません**(原作者の配布条件のため)。必要なときは手元の原DLLから再生成します。

作業ディレクトリは次の配置を前提にしています(スクリプト内のパスが固定のため。必要に応じて書き換えてください)。
```
<work>/x/SKSE/Plugins/FightWithMe.dll   原DLL
<work>/out/*.dll, *.json                 パッチ出力(tools/fwm_patch.py)
<work>/tools/                            このリポジトリの tools/
```
依存: `pip install -r requirements-dev.txt`

| ファイル | 用途 |
|---|---|
| `xr.py` | 共通部品: 逆アセンブル済み命令列、文字列検索 `find_str`、参照元 `refs`。他のスクリプトが `exec` で読み込む |
| `dasm.py` / `dasm_x.py` / `dis_x86.py` | アドレス範囲の逆アセンブル(`dis_x86.py` は capstone の skipdata 付き) |
| `annot.py` / `annot_sd.py` | 範囲の逆アセンブル + 参照している文字列の注釈 |
| `xref.py` | `.rdata` の文字列を指す `lea` の参照元を探す |
| `ibref.py` | 文字列への間接参照(オフセット付き)を探す |
| `fconst.py` | `rip` 相対の float 定数(mulss/addss など)を読む。`SPACING_CONSTS` の候補探し |
| `sigfind.py` / `sig2.py` | 旧版の命令列(アドレスをマスク)を新版から探す。**版の移行時のアドレス再導出**。`sig2.py` の旧アドレスは 0.2.0→0.3.0 用 |
| `scan_len.py` / `scan_len8.py` | 長さ即値(文字列長のリテラル)の取りこぼし探し。版・出力名が固定(t1/t5/t8) |
| `scan_reg.py` | 文字列長と同じレジスタを別用途(デストラクタのフラグなど)に使う箇所の検出。正式版は `tools/fwm_scan_flag.py` |

スクリプトは調査の都度書いたもので、整理されていません。再利用するときは、まず中身を読んでください。
