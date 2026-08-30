# 画像バッチ変換で先に見るpath衝突

画像変換の設定値が正しくても、入力と出力のpathがぶつかると「変換できた」ように見えながら元ファイルや別成果物を壊せる。

Image Batch Kitで一時fixtureを使って、path境界を実際に再現した。

## 1. outdirを入力フォルダ自身にすると元画像を上書きできた

修正前の実測では、1200×600のJPEGを入力フォルダ自身へJPEG出力したところ、同じ `photo.jpg` が300×150へ置き換わった。

- before: 1200×600 / 12,031 bytes
- after: 300×150 / 1,389 bytes
- source path == output path

現在は変換開始前にsource/outputの実pathを比較し、同一なら `ValueError` で止める。

## 2. contact sheetが変換画像と同じpathだとmanifestと実体がズレた

修正前は、300×100の `a.webp` を生成したあと、contact sheetも同じ `a.webp` に指定できた。

manifest側は変換画像を300×100と記録したままだが、実ファイルはcontact sheetの1040×294へ置き換わった。

現在はsource / converted output / contact sheetのpath衝突を処理前に検出して拒否する。

## 3. max_px=0は計算途中の例外になっていた

修正前は `max_px=0` で `ZeroDivisionError`。現在は `max_px >= 1` とquality範囲を入口で検証し、無効な設定を明示的な入力エラーとして扱う。

## 回帰テスト

今回の変更後に3テストを実行して3/3 PASSを確認した。

- 通常のresize / convert / contact sheet
- 同じstemを持つ複数入力の出力名衝突回避
- destructive path collision + invalid max_pxの拒否

ここで書いている数値は一時fixtureでの再現結果。実案件の品質実績や処理速度のベンチマークではない。

OSS: https://github.com/paper-daemon/image-batch-kit
