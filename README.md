# Image Batch Kit

フォルダ内の画像をまとめてリサイズ・WebP/JPEG/PNG変換し、一覧用コンタクトシートとJSON manifestまで作る無料OSSです。

```bash
python image_batch_kit.py ./images --outdir ./output --max-px 1600 --format webp --quality 88 --contact-sheet ./output/contact.jpg --json manifest.json
```

## できること
- JPEG / PNG / WebPを一括処理
- EXIF orientationを反映
- 長辺基準のリサイズ
- WebP / JPEG / PNG変換
- 再エンコードで余計なメタデータを引き継がない
- 画像一覧のコンタクトシート生成
- 元/出力サイズ・容量のJSON manifest

## 入出力の境界
既存の出力ファイルと同名になる場合も上書きせず、`name-2.webp` のように次の空き名へ保存します。

フォルダを入力にする場合、`--outdir` は入力フォルダとは別の場所を指定してください。同じフォルダを出力先にすると、前回生成したWebP等を次回入力として再取り込みできてしまうため、現在は処理開始前にエラーで停止します。

`--json` のreport pathも、元画像・変換後画像・contact sheetと同じ実体pathにはできません。衝突する指定は画像処理前に拒否し、画像をJSONで上書きしません。

```bash
python3 -m unittest -v tests.test_image_batch_kit
```

Python 3.10+ / Pillow / MIT License。
- BOOTH 0円DL: https://amase-memo.booth.pm/items/8778724
- 作者サイト: https://paper-daemon.github.io/
