# OpenAI Pylint

## Problems

Pylint là không đủ điều kiện để tìm ra và vấn đề trong source code,
có những thoả thuận ngầm bên trong đó chỉ có dev mới hiểu. Dẫn đến
người sau không biết và khó để tìm ra vấn đề.

## Solution

Sử dụng OpenAI để phát hiện vấn đề, viết code cảnh báo pylint.
1. OpenAI review source code
2. sau đó tìm vấn đề với source code
3. sau đó viết pylint để tìm vấn đề đó
4. chạy pylint trên toàn bộ dự án.

Khi đó sẽ tránh vấn đề tiếp tục xảy ra trong tương lai.
