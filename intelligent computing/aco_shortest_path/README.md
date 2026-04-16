# Ant Colony Optimization for Shortest Path in Graphs

Project cho đề tài môn Tính Toán Thông Minh:
**Xây dựng thuật toán Ant Colony Optimization cho bài toán tìm đường đi ngắn nhất trên đồ thị**

## Mục tiêu

Chương trình mô phỏng đàn kiến tìm đường đi ngắn nhất từ đỉnh nguồn đến đỉnh đích trên đồ thị có trọng số. Xác suất chọn cạnh kế tiếp được tính dựa trên:

- `pheromone`
- `heuristic = 1 / khoảng cách`

Sau mỗi vòng lặp, pheromone sẽ bay hơi và được tăng cường trên những đường đi tốt.

## Cấu trúc thư mục

```text
aco_shortest_path/
├── main.py
├── requirements.txt
├── README.md
├── data/
│   ├── sample_matrix.csv
│   └── sample_graph.txt
├── results/
│   ├── best_path.txt
│   ├── convergence.png
│   └── graph_result.png
├── src/
│   ├── graph_utils.py
│   ├── ant.py
│   ├── aco.py
│   ├── visualize.py
│   └── config.py
└── tests/
    └── test_small_graph.py
```

## Cài đặt

```bash
pip install -r requirements.txt
```

## Chạy chương trình

```bash
python main.py
```

## Dữ liệu đầu vào

Có 2 file mẫu trong thư mục `data/`:

- `sample_matrix.csv`: ma trận kề có trọng số, giá trị `0` nghĩa là không có cạnh.
- `sample_graph.txt`: mô tả cạnh theo dạng `u v w`.

Mặc định chương trình đang đọc `sample_matrix.csv`.

## Ý tưởng thuật toán

1. Khởi tạo pheromone đều trên các cạnh.
2. Mỗi con kiến bắt đầu từ đỉnh nguồn.
3. Tại mỗi bước, kiến chọn đỉnh kế tiếp theo xác suất:

```text
P(i, j) ∝ [tau(i, j)]^alpha * [eta(i, j)]^beta
```

Trong đó:

- `tau(i, j)` là pheromone trên cạnh `(i, j)`
- `eta(i, j) = 1 / distance(i, j)`

4. Khi một kiến tới đích, tính độ dài đường đi.
5. Sau mỗi vòng lặp:

```text
pheromone = (1 - evaporation_rate) * pheromone + delta_pheromone
delta_pheromone = Q / path_length
```

6. Lưu đường đi tốt nhất toàn cục.

## Kết quả đầu ra

- `results/best_path.txt`: đường đi tốt nhất và tổng chi phí.
- `results/convergence.png`: biểu đồ hội tụ qua các vòng lặp.
- `results/graph_result.png`: đồ thị với đường đi tốt nhất được tô nổi bật.
- `results/comparison_chart.png`: biểu đồ so sánh trực quan ACO và Dijkstra.
- `results/comparison_report.txt`: so sánh ACO với Dijkstra trên cùng đồ thị.

## Kiểm thử

```bash
python -m unittest discover -s tests
```

## Tùy chỉnh tham số

Bạn có thể đổi tham số trong `src/config.py`:

- `num_ants`
- `num_iterations`
- `alpha`
- `beta`
- `evaporation_rate`
- `q`
- `source`
- `destination`

## Gợi ý dùng cho báo cáo

- Mô tả bài toán tìm đường đi ngắn nhất trên đồ thị có trọng số.
- Trình bày cơ chế chọn đường của kiến bằng pheromone và heuristic.
- Giải thích vai trò của bay hơi pheromone để tránh kẹt ở nghiệm cục bộ.
- So sánh kết quả ACO với Dijkstra trên đồ thị nhỏ nếu muốn mở rộng.

## So sánh ACO với Dijkstra

### 1. Điểm giống nhau

- Cả hai đều dùng để tìm đường đi từ đỉnh nguồn đến đỉnh đích trên đồ thị có trọng số dương.
- Cả hai đều trả về một đường đi và tổng chi phí tương ứng.

### 2. Điểm khác nhau

| Tiêu chí | ACO | Dijkstra |
|---|---|---|
| Bản chất | Metaheuristic, mô phỏng hành vi đàn kiến | Thuật toán chính xác, tham lam |
| Kết quả | Có thể gần tối ưu hoặc tối ưu | Đảm bảo tối ưu với trọng số không âm |
| Tốc độ | Chậm hơn do lặp nhiều vòng và nhiều kiến | Nhanh hơn trên đồ thị cỡ nhỏ và vừa |
| Tính ngẫu nhiên | Có | Không |
| Khả năng mở rộng | Linh hoạt, dễ mở rộng cho bài toán khó hơn | Tốt cho shortest path cổ điển |

### 3. Nhận xét cho báo cáo

Trên đồ thị mẫu của project, ACO thường tìm được cùng đường đi ngắn nhất như Dijkstra sau một số vòng lặp. Tuy nhiên, Dijkstra vẫn là mốc chuẩn để đánh giá vì đây là thuật toán xác định và cho nghiệm tối ưu trên đồ thị có trọng số không âm. Điểm mạnh của ACO không nằm ở tốc độ trên bài toán ngắn nhất cơ bản, mà ở khả năng áp dụng cho các bài toán tối ưu tổ hợp phức tạp hơn, nơi lời giải chính xác khó tìm hoặc chi phí tính toán quá lớn.

### 4. Cách trích kết quả thực nghiệm

Sau khi chạy:

```bash
python main.py
```

hãy dùng nội dung trong `results/comparison_report.txt` để đưa vào phần đánh giá kết quả.
