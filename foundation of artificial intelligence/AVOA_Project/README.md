Thư mục này dành cho dữ liệu đầu vào nếu mở rộng project sang bài toán ứng dụng thực tế.
Hiện tại project sử dụng các hàm benchmark nên không cần dataset dạng CSV.# AVOA Project

## Giới thiệu
Project này cài đặt thuật toán **African Vultures Optimization Algorithm (AVOA)** bằng Python để giải các bài toán tối ưu hóa hàm benchmark.

Mục tiêu của project:
- tìm hiểu nguyên lý hoạt động của AVOA
- cài đặt thuật toán bằng Python
- thử nghiệm trên một số hàm benchmark phổ biến
- quan sát khả năng hội tụ thông qua đồ thị

## Cấu trúc thư mục
```text
AVOA_Project/
├── dataset/
│   └── README.md
├── results/
│   ├── avoa/
│   │   ├── sphere_convergence.png
│   │   ├── rastrigin_convergence.png
│   │   └── ackley_convergence.png
│   ├── pso/
│   │   ├── sphere_convergence.png
│   │   ├── rastrigin_convergence.png
│   │   └── ackley_convergence.png
│   └── comparison/
│       ├── sphere_comparison.png
│       ├── rastrigin_comparison.png
│       └── ackley_comparison.png
├── src/
│   ├── __init__.py
│   ├── algorithms/
│   │   ├── __init__.py
│   │   ├── avoa.py
│   │   └── pso.py
│   ├── experiments.py
│   ├── main.py
│   ├── objective_functions.py
│   └── visualize.py
├── README.md
├── requirements.txt
└── run.py