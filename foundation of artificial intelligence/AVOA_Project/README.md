# Tìm hiểu thuật toán tối ưu African Vultures Optimization Algorithm (AVOA) và ứng dụng trong bài toán tối ưu hóa
## Thành viên nhóm
- 3123580046 - Thạch Ngọc Thảo
- 3123580051 - Phạm Hoàng Tiến
- 3123580058 - Nguyễn Thái Tú
- 3123580017 - Biện Hữu Khang

- Giảng viên hướng dẫn: TS. Huỳnh Minh Trí

Project cho đề tài môn Tính Toán Thông Minh:
**Xây dựng thuật toán Ant Colony Optimization cho bài toán tìm đường đi ngắn nhất trên đồ thị**

## Giới thiệu
Project này cài đặt `African Vultures Optimization Algorithm (AVOA)` bằng Python để giải các bài toán tối ưu hóa hàm benchmark. Trong repo hiện tại, AVOA được dùng ở mức độ học tập và minh họa, không phải bản tái hiện đầy đủ mọi công thức trong paper gốc.

Project hiện có 2 cách sử dụng:
- chạy script để thực hiện các thí nghiệm AVOA và PSO trên các hàm benchmark
- chạy Streamlit để xem kết quả, đồ thị hội tụ và cách các "kền kền" di chuyển

## Mục tiêu
- tìm hiểu ý tưởng của AVOA
- cài đặt thuật toán tối ưu hóa theo quần thể
- so sánh nhanh với PSO trên một số hàm benchmark
- quan sát quá trình hội tụ và quỹ đạo di chuyển của các cá thể

## Các hàm benchmark đang dùng
Project đang dùng 3 hàm benchmark có sẵn trong [src/objective_functions.py](./src/objective_functions.py):
- `Sphere`
- `Rastrigin`
- `Ackley`

Cả 3 hàm này đều có giá trị tối ưu lý thuyết bằng `0` tại vector `0`.

## Cấu trúc thư mục
```text
AVOA_Project/
|-- app.py
|-- run.py
|-- requirements.txt
|-- README.md
|-- dataset/
|   `-- README.md
|-- docs/
|   `-- experiments.md
|-- results/
|   |-- avoa/
|   |-- pso/
|   `-- comparison/
|-- scripts/
|   `-- verify_results.py
`-- src/
    |-- __init__.py
    |-- main.py
    |-- experiments.py
    |-- objective_functions.py
    |-- visualize.py
    `-- algorithms/
        |-- __init__.py
        |-- avoa.py
        `-- pso.py
```

## Cài đặt
Dùng Python `3.10+` là hợp lý. Cài thư viện bằng:

```powershell
pip install -r requirements.txt
```

Nội dung file [requirements.txt](./requirements.txt):
- `numpy`
- `matplotlib`
- `streamlit`

## Cách chạy
### 1. Mở terminal tại đúng thư mục project
Nếu bạn đang ở thư mục gốc của workspace, chuyển vào project bằng:

```powershell
cd "foundation of artificial intelligence/AVOA_Project"
```

### 2. Cài thư viện
Chạy lệnh sau một lần trước khi chạy project:

```powershell
pip install -r requirements.txt
```

### 3. Chạy code thí nghiệm bằng terminal
Lệnh này sẽ chạy AVOA và PSO trên `Sphere`, `Rastrigin`, `Ackley`, sau đó lưu các đồ thị vào thư mục `results/`.

```powershell
python run.py
```

Hoặc nếu bạn muốn chạy theo module:

```powershell
python -m src.main
```

Kết quả thường sẽ gồm:
- file ảnh hội tụ của AVOA
- file ảnh hội tụ của PSO
- file ảnh so sánh AVOA và PSO

### 4. Chạy giao diện Streamlit
Giao diện Streamlit cho phép:
- chọn hàm benchmark
- chỉnh số chiều, kích thước quần thể, số vòng lặp, cận dưới, cận trên, random seed
- chạy AVOA
- so sánh với PSO
- xem đồ thị hội tụ
- xem minh họa cách "kền kền" di chuyển qua các iteration
- xem contour nền của hàm mục tiêu để thấy quần thể đang tiến về vùng fitness thấp nào

Chạy bằng lệnh:

```powershell

cd "foundation of artificial intelligence\AVOA_Project"
streamlit run app.py

```

Sau khi chạy lệnh trên, Streamlit sẽ mở một trang local trong trình duyệt. Nếu không tự mở, copy link local do terminal in ra, thường có dạng:

```text
http://localhost:8501
```

## Ý nghĩa các kết quả
### 1. Convergence curve
Đồ thị hội tụ thể hiện `best fitness` theo từng iteration.

- đường giảm dần cho thấy thuật toán đang cải thiện nghiệm
- nếu đường phẳng sớm, thuật toán có thể đã hội tụ hoặc mắc kẹt ở nghiệm chưa tốt

### 2. So sánh AVOA và PSO
Trong app và script, project có thể hiển thị:
- `best fitness`
- `runtime`
- đồ thị hội tụ của AVOA và PSO trên cùng một hàm

Điều này phù hợp để viết phần đánh giá thực nghiệm trong báo cáo.

### 3. Hình "Cách kền kền di chuyển"
Phần này trong Streamlit là minh họa quỹ đạo di chuyển của các cá thể.

- nền contour thể hiện giá trị hàm mục tiêu trên 2 chiều đầu tiên
- mỗi màu là một cá thể
- mỗi đường là quỹ đạo của cá thể đó từ lúc khởi tạo đến iteration đang xem
- chấm tròn là vị trí hiện tại của cá thể
- ngôi sao đỏ là `best solution so far`

Lưu ý:
- nếu bài toán có hơn 2 chiều, hình này chỉ hiện 2 chiều đầu tiên của nghiệm
- contour được tính bằng cách giữ các chiều còn lại bằng `0`
- vì vậy đây là hình minh họa trực quan, không phải toàn bộ không gian tìm kiếm thật

## Ghi chú về AVOA trong project này
Bản cài đặt hiện tại là `simplified AVOA`.

Điều đó có nghĩa là:
- code vẫn chạy đúng và có khả năng hội tụ
- có thể dùng để demo, báo cáo môn học, và so sánh cơ bản
- nhưng chưa nên khẳng định là bản tái hiện đầy đủ paper gốc

Nếu mục tiêu của bạn là báo cáo học phần, cách mô tả an toàn là:
`Project cài đặt một phiên bản đơn giản hóa của AVOA để minh họa cơ chế tìm kiếm và quan sát hành vi hội tụ trên hàm benchmark.`

## Tệp kết quả
Sau khi chạy, kết quả thường được lưu trong thư mục `results/`:
- `results/avoa/`: đồ thị hội tụ của AVOA
- `results/pso/`: đồ thị hội tụ của PSO
- `results/comparison/`: đồ thị so sánh AVOA và PSO

## File quan trọng
- [app.py](./app.py): giao diện Streamlit
- [run.py](./run.py): cách chạy nhanh project bằng `python run.py`
- [docs/experiments.md](./docs/experiments.md): mô tả phần thực nghiệm và kết quả
- [scripts/verify_results.py](./scripts/verify_results.py): kiểm tra nhanh các file kết quả đã đủ hay chưa
- [src/main.py](./src/main.py): gọi `run_all_experiments()`
- [src/experiments.py](./src/experiments.py): chạy AVOA, PSO và lưu kết quả
- [src/algorithms/avoa.py](./src/algorithms/avoa.py): cài đặt AVOA và lưu lịch sử di chuyển quần thể
- [src/algorithms/pso.py](./src/algorithms/pso.py): cài đặt PSO để đối chiếu
- [src/objective_functions.py](./src/objective_functions.py): các hàm benchmark
- [src/visualize.py](./src/visualize.py): hàm vẽ đồ thị

## Hướng mở rộng
Nếu muốn mở rộng project, bạn có thể:
- thêm benchmark function mới
- thêm animation theo thời gian trong Streamlit
- vẽ contour/background của hàm mục tiêu trong trường hợp 2D
- cài đặt phiên bản AVOA sát hơn với paper gốc
