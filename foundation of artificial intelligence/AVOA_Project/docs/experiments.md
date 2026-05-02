# Thực nghiệm và kết quả

Phần này mô tả lại đúng theo code trong project AVOA hiện tại để tránh lệch giữa báo cáo và kết quả sinh ra từ chương trình.

## 1. Mục tiêu thực nghiệm

So sánh khả năng hội tụ của AVOA với PSO trên các hàm benchmark cơ bản:
- `sphere`
- `rastrigin`
- `ackley`

Mỗi thuật toán được chạy trên cùng một thiết lập đầu vào để việc so sánh là công bằng.

## 2. Thiết lập thực nghiệm

Thiết lập mặc định được định nghĩa trong [src/experiments.py](../src/experiments.py):
- miền tìm kiếm: $[-10, 10]$
- số chiều: $30$
- kích thước quần thể: $40$
- số vòng lặp: $150$
- seed mặc định: `42`

Với seed cố định, kết quả có thể tái lập khi chạy lại cùng phiên bản code và môi trường thư viện tương tự.

## 3. Quy trình chạy

Chương trình chính gọi `run_all_experiments()` trong [src/main.py](../src/main.py), sau đó:
1. Khởi tạo AVOA và PSO với cùng tham số.
2. Chạy tối ưu trên từng hàm benchmark.
3. Ghi lại đường hội tụ của mỗi thuật toán.
4. Lưu biểu đồ vào thư mục `results/`.

Các file ảnh đầu ra được sinh bởi [src/visualize.py](../src/visualize.py).

## 4. Kết quả đầu ra

Project tạo ra 3 nhóm biểu đồ:
- `results/avoa/*_convergence.png`
- `results/pso/*_convergence.png`
- `results/comparison/*_comparison.png`

Tên file tương ứng với từng hàm benchmark:
- `sphere`
- `rastrigin`
- `ackley`

## 5. Cách kiểm tra nhanh

Để xác nhận kết quả đã được sinh đúng, chạy:

```bash
python scripts/verify_results.py
```

Nếu có file bị thiếu, chạy lại:

```bash
python run.py
```
