---
title: "Cấp quyền phản chiếu qua ADB"
description: "Cấp trước quyền ghi màn hình của ScreenOnAuto qua ADB để hộp thoại không xuất hiện mỗi khi bắt đầu phản chiếu."
lang: vi
slug: grant-mirror-permission-via-adb
permalink: /docs/vi/grant-mirror-permission-via-adb/
date: 2026-10-15
last_modified_at: 2026-10-15
---

# Cấp quyền phản chiếu qua ADB

Theo mặc định, Android hiện hộp thoại xin quyền mỗi khi ScreenOnAuto bắt đầu phản chiếu màn hình.
Bạn có thể cấp trước quyền **Ghi màn hình (MediaProjection)** bằng ADB để hộp thoại không bao giờ xuất hiện nữa.

Quyền này cũng bắt buộc cho **Chỉ phản chiếu ứng dụng này** (Android 15+) — thiếu nó, tính năng đó không hoạt động.

## Chuẩn bị

- Đã cài [ADB (Android Debug Bridge)](https://developer.android.com/tools/releases/platform-tools) trên máy tính
- Đã bật gỡ lỗi USB trên điện thoại (**Cài đặt → Tùy chọn cho nhà phát triển → Gỡ lỗi USB**)
- Điện thoại kết nối qua USB (hoặc ADB qua Wi-Fi)

## Các bước

1. Mở một cửa sổ dòng lệnh (Command Prompt / PowerShell trên Windows).

2. Kiểm tra xem ADB có nhận ra thiết bị không:

   ```
   adb devices
   ```

   Thiết bị của bạn phải hiện là `device` (không phải `unauthorized`).

3. Cấp quyền:

   ```
   adb shell appops set idv.lzn.screenonauto android:project_media allow
   ```

4. Mở ScreenOnAuto và bắt đầu phản chiếu — hộp thoại xin quyền sẽ không còn xuất hiện.

## Thu hồi quyền

Để khôi phục hành vi mặc định (hiện hộp thoại mỗi lần):

```
adb shell appops set idv.lzn.screenonauto android:project_media default
```

## Khắc phục sự cố

- **`error: device unauthorized`** — Tìm hộp thoại "Cho phép gỡ lỗi USB?" trên điện thoại và nhấn **Cho phép**.
- **Hộp thoại vẫn xuất hiện** — Buộc dừng ScreenOnAuto rồi mở lại. Nếu vẫn còn, hãy thu hồi rồi cấp lại bằng các lệnh ở trên.
- **Đã cài lại ứng dụng (hoặc chuyển giữa kênh Play và kênh cài APK)** — gỡ cài đặt sẽ xóa quyền đã cấp; hãy chạy lại lệnh cấp quyền sau khi cài lại.
- **Quyền bị đặt lại sau khi khởi động lại** — Trên một số ROM (ví dụ MIUI/HyperOS), quyền cấp bằng `appops` không giữ được qua lần khởi động lại. Hãy chạy lại lệnh sau mỗi lần khởi động lại; ADB qua Wi-Fi (gỡ lỗi không dây) giúp bạn khỏi phải cắm cáp mỗi lần, nhưng không ngăn được việc quyền bị đặt lại.
