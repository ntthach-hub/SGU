# Ant Colony Optimization for Shortest Path in Graphs
## Thành viên nhóm
- 3123580046 - Thạch Ngọc Thảo
- 3123580051 - Phạm Hoàng Tiến
- 3123580058 - Nguyễn Thái Tú
- 3123580017 - Biện Hữu Khang
  
Giảng viên hướng dẫn: TS. Huỳnh Minh Trí

Project cho đề tài môn Tính Toán Thông Minh:
**Xây dựng thuật toán Ant Colony Optimization cho bài toán tìm đường đi ngắn nhất trên đồ thị**

## Mục tiêu

Chương trình mô phỏng đàn kiến tìm đường đi ngắn nhất từ đỉnh nguồn đến đỉnh đích trên đồ thị có trọng số. Xác suất chọn đỉnh kế tiếp được tính dựa trên:

- `pheromone`
- `heuristic = 1 / distance`

Sau mỗi vòng lặp, pheromone sẽ bay hơi và được tăng cường trên những đường đi tốt. Project cũng so sánh kết quả ACO với Dijkstra để phục vụ phần đánh giá trong báo cáo.

## Cấu trúc thư mục hiện tại

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
│   ├── comparison_chart.png
│   ├── comparison_report.txt
│   ├── convergence.png
│   └── graph_result.png
├── src/
│   ├── aco.py
│   ├── ant.py
│   ├── config.py
│   ├── graph_utils.py
│   └── visualize.py
└── tests/
    └── test_small_graph.py
```

Lưu ý:

- Thư mục `__pycache__/` không liệt kê trong cây vì là file sinh tự động.
- Thư mục `results/` sẽ được cập nhật lại mỗi khi chạy `main.py`.

## Cài đặt

```bash
pip install -r requirements.txt
```

## Cách chạy

Chạy chương trình chính:

```bash
python main.py
```

Chạy kiểm thử:

```bash
python -m unittest discover -s tests
```

## Dữ liệu đầu vào

Project hỗ trợ 2 dạng dữ liệu mẫu trong `data/`:

- `sample_matrix.csv`: ma trận kề có trọng số, giá trị `0` nghĩa là không có cạnh.
- `sample_graph.txt`: danh sách cạnh theo định dạng `u v w`.

Hiện tại `main.py` đang đọc từ `sample_matrix.csv`.

## Ý tưởng thuật toán ACO

1. Khởi tạo pheromone đều trên các cạnh.
2. Mỗi con kiến xuất phát từ đỉnh nguồn.
3. Ở mỗi bước, kiến chọn đỉnh kế tiếp theo xác suất:

```text
P(i, j) ∝ [tau(i, j)]^alpha * [eta(i, j)]^beta
```

Trong đó:

- `tau(i, j)` là pheromone trên cạnh `(i, j)`
- `eta(i, j) = 1 / weight(i, j)`

4. Nếu kiến tới đích, tính tổng độ dài đường đi.
5. Sau mỗi vòng lặp:

```text
pheromone = (1 - evaporation_rate) * pheromone + delta_pheromone
delta_pheromone = Q / path_length
```

6. Lưu lại đường đi tốt nhất toàn cục.

## Các file đầu ra

Sau khi chạy `python main.py`, chương trình sẽ sinh:

- `results/best_path.txt`: đường đi tốt nhất do ACO tìm được và tổng chi phí.
- `results/convergence.png`: biểu đồ hội tụ của ACO theo số vòng lặp.
- `results/graph_result.png`: đồ thị với đường đi tốt nhất được tô nổi bật.
- `results/comparison_report.txt`: báo cáo text so sánh ACO với Dijkstra.
- `results/comparison_chart.png`: ảnh so sánh trực quan khoảng cách và thời gian chạy giữa ACO và Dijkstra.

## Các module chính

- `src/config.py`: chứa các tham số cấu hình của ACO.
- `src/ant.py`: mô tả hành vi của một con kiến khi xây dựng đường đi.
- `src/aco.py`: cài đặt thuật toán Ant Colony Optimization.
- `src/graph_utils.py`: đọc dữ liệu đồ thị, tính độ dài đường đi, chạy Dijkstra để đối chiếu.
- `src/visualize.py`: vẽ đồ thị, biểu đồ hội tụ và biểu đồ so sánh.
- `tests/test_small_graph.py`: kiểm tra ACO trên đồ thị nhỏ.

## Tùy chỉnh tham số

Bạn có thể đổi các tham số trong `src/config.py`:

- `num_ants`
- `num_iterations`
- `alpha`
- `beta`
- `evaporation_rate`
- `q`
- `initial_pheromone`
- `max_steps_factor`
- `source`
- `destination`
- `random_seed`

## So sánh ACO với Dijkstra

### Điểm giống nhau

- Cả hai đều giải bài toán tìm đường đi từ đỉnh nguồn đến đỉnh đích.
- Cả hai đều trả về đường đi và tổng chi phí tương ứng.

### Điểm khác nhau

| Tiêu chí | ACO | Dijkstra |
|---|---|---|
| Bản chất | Metaheuristic, mô phỏng hành vi đàn kiến | Thuật toán chính xác |
| Kết quả | Có thể gần tối ưu hoặc tối ưu | Đảm bảo tối ưu với trọng số không âm |
| Tốc độ | Chậm hơn do chạy nhiều vòng lặp | Nhanh hơn cho bài toán shortest path cổ điển |
| Tính ngẫu nhiên | Có | Không |
| Mục tiêu phù hợp | Bài toán tối ưu tổ hợp phức tạp | Bài toán đường đi ngắn nhất chuẩn |

### Nhận xét dùng trong báo cáo

Trên đồ thị mẫu của project, ACO có thể tìm được cùng đường đi ngắn nhất như Dijkstra sau một số vòng lặp. Tuy nhiên, Dijkstra vẫn là mốc chuẩn để đánh giá vì đây là thuật toán xác định và cho nghiệm tối ưu trên đồ thị có trọng số không âm. Điểm mạnh của ACO là khả năng mở rộng sang các bài toán tối ưu khó hơn, nơi không dễ áp dụng thuật toán chính xác.

## Gợi ý trình bày trong báo cáo

- Giới thiệu bài toán shortest path trên đồ thị có trọng số.
- Trình bày cơ chế pheromone và heuristic trong ACO.
- Giải thích vai trò của bay hơi pheromone để tránh kẹt nghiệm cục bộ.
- Dùng `comparison_report.txt` và `comparison_chart.png` để đánh giá ACO so với Dijkstra.
