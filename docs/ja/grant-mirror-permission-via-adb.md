---
title: "ADB でミラーリング権限を付与"
description: "ADB で ScreenOnAuto の画面キャプチャ権限を事前に付与し、ミラーリングを始めるたびにダイアログが出ないようにします。"
lang: ja
slug: grant-mirror-permission-via-adb
permalink: /docs/ja/grant-mirror-permission-via-adb/
date: 2026-10-15
last_modified_at: 2026-10-15
---

# ADB でミラーリング権限を付与

初期状態では、ScreenOnAuto が画面のミラーリングを開始するたびに Android が許可ダイアログを表示します。ADB で **画面キャプチャ（MediaProjection）** の権限を事前に付与しておけば、このダイアログは二度と表示されなくなります。

この権限は **このアプリだけをミラーリング**（Android 15 以上）にも必要で、付与しないとこの機能は動作しません。

## 準備するもの

- パソコンにインストールした [ADB（Android Debug Bridge）](https://developer.android.com/tools/releases/platform-tools)
- スマホで USB デバッグを有効にしておくこと（**設定 → 開発者向けオプション → USB デバッグ**）
- USB（または Wi-Fi 経由の ADB）で接続したスマホ

## 手順

1. ターミナルを開きます（Windows ではコマンド プロンプトまたは PowerShell）。

2. ADB が端末を認識しているか確認します。

   ```
   adb devices
   ```

   端末が `device` と表示されていれば OK です（`unauthorized` ではないこと）。

3. 権限を付与します。

   ```
   adb shell appops set idv.lzn.screenonauto android:project_media allow
   ```

4. ScreenOnAuto を起動してミラーリングを開始します。許可ダイアログはもう表示されないはずです。

## 権限を取り消す

初期状態（毎回ダイアログを表示）に戻すには：

```
adb shell appops set idv.lzn.screenonauto android:project_media default
```

## トラブルシューティング

- **`error: device unauthorized`** — スマホに表示される「USB デバッグを許可しますか？」ダイアログで **許可** をタップしてください。
- **まだダイアログが表示される** — ScreenOnAuto を強制停止してから起動し直してください。それでも表示される場合は、上のコマンドで権限を取り消してから付与し直してください。
- **アプリを再インストールした（または Play とサイドロードの入手経路を切り替えた）** — アンインストールすると付与した権限も消えます。再インストール後に付与のコマンドをもう一度実行してください。
- **再起動すると権限が元に戻る** — 一部の ROM（MIUI / HyperOS など）では、`appops` で付与した権限が再起動後に保持されません。再起動のたびにコマンドを実行し直してください。Wi-Fi 経由の ADB（ワイヤレス デバッグ）を使えば毎回ケーブルをつなぐ手間は省けますが、リセット自体は防げません。
