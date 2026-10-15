---
title: "Berikan Izin Pencerminan melalui ADB"
description: "Berikan izin perekaman layar ScreenOnAuto lebih dulu lewat ADB agar dialog tidak muncul setiap kali pencerminan dimulai."
lang: id
slug: grant-mirror-permission-via-adb
permalink: /docs/id/grant-mirror-permission-via-adb/
date: 2026-10-15
last_modified_at: 2026-10-15
---

# Berikan Izin Pencerminan melalui ADB

Secara default, Android menampilkan dialog izin setiap kali ScreenOnAuto memulai pencerminan layar.
Anda bisa memberikan izin **Perekaman layar (MediaProjection)** lebih dulu lewat ADB agar dialog itu tidak pernah muncul lagi.

Izin ini juga diperlukan untuk **Cerminkan aplikasi ini saja** (Android 15+), yang tidak berfungsi tanpanya.

## Prasyarat

- [ADB (Android Debug Bridge)](https://developer.android.com/tools/releases/platform-tools) terinstal di komputer Anda
- Proses debug USB diaktifkan di ponsel (**Setelan → Opsi developer → Proses debug USB**)
- Ponsel tersambung lewat USB (atau ADB lewat Wi-Fi)

## Langkah-langkah

1. Buka terminal (Command Prompt / PowerShell di Windows).

2. Pastikan ADB bisa melihat perangkat Anda:

   ```
   adb devices
   ```

   Perangkat Anda seharusnya tampil sebagai `device` (bukan `unauthorized`).

3. Berikan izinnya:

   ```
   adb shell appops set idv.lzn.screenonauto android:project_media allow
   ```

4. Buka ScreenOnAuto dan mulai pencerminan — dialog izin seharusnya tidak muncul lagi.

## Mencabut Izin

Untuk mengembalikan perilaku default (dialog muncul setiap kali):

```
adb shell appops set idv.lzn.screenonauto android:project_media default
```

## Pemecahan Masalah

- **`error: device unauthorized`** — Cari dialog "Izinkan proses debug USB?" di ponsel Anda lalu ketuk **Izinkan**.
- **Dialog masih muncul** — Paksa berhenti ScreenOnAuto lalu buka lagi. Jika masih terjadi, cabut lalu berikan lagi izinnya dengan perintah di atas.
- **Aplikasi diinstal ulang (atau berpindah antara saluran Play dan APK manual)** — mencopot aplikasi menghapus izin ini; jalankan lagi perintah pemberian izin setelah menginstal ulang.
- **Izin kembali seperti semula setelah ponsel dimulai ulang** — Di beberapa ROM (mis. MIUI/HyperOS), izin `appops` tidak bertahan setelah reboot. Jalankan lagi perintahnya setiap kali ponsel dimulai ulang; ADB lewat Wi-Fi (debugging nirkabel) menghemat Anda dari mencolokkan kabel setiap kali, tetapi tidak mencegah izin direset.
