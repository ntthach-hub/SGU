import numpy as np


class AVOA:
    """
    African Vultures Optimization Algorithm (AVOA)
    Phiên bản đơn giản hóa để học tập và minh họa.

    Thuật toán này dùng một quần thể cá thể (vultures),
    mỗi cá thể là một nghiệm trong không gian tìm kiếm.

    Parameters
    ----------
    obj_func : function
        Hàm mục tiêu cần tối ưu (minimize).
        Input: numpy array có kích thước (dim,)
        Output: một số thực (fitness)

    lb : float
        Cận dưới của miền tìm kiếm

    ub : float
        Cận trên của miền tìm kiếm

    dim : int
        Số chiều của bài toán

    pop_size : int
        Số lượng cá thể trong quần thể

    max_iter : int
        Số vòng lặp tối đa
    """

    def __init__(self, obj_func, lb, ub, dim, pop_size=30, max_iter=100):
        self.obj_func = obj_func
        self.lb = lb
        self.ub = ub
        self.dim = dim
        self.pop_size = pop_size
        self.max_iter = max_iter

        # Quần thể: ma trận kích thước (pop_size, dim)
        self.population = None

        # Fitness của từng cá thể
        self.fitness = None

        # Nghiệm tốt nhất toàn cục
        self.best_solution = None
        self.best_fitness = np.inf

        # Lưu lịch sử hội tụ (best fitness qua từng vòng lặp)
        self.convergence_curve = []

    def initialize_population(self):
        """
        Khởi tạo quần thể ngẫu nhiên trong đoạn [lb, ub].
        """
        self.population = np.random.uniform(
            low=self.lb,
            high=self.ub,
            size=(self.pop_size, self.dim)
        )

    def evaluate_population(self):
        """
        Tính fitness cho toàn bộ quần thể.
        """
        self.fitness = np.array([self.obj_func(ind) for ind in self.population])

    def update_best_solution(self):
        """
        Cập nhật nghiệm tốt nhất toàn cục.
        """
        min_idx = np.argmin(self.fitness)
        current_best_fitness = self.fitness[min_idx]

        if current_best_fitness < self.best_fitness:
            self.best_fitness = current_best_fitness
            self.best_solution = self.population[min_idx].copy()

    def get_two_best_vultures(self):
        """
        Lấy ra 2 cá thể tốt nhất trong quần thể.
        Đây là ý tưởng quan trọng trong AVOA:
        dùng 2 nghiệm mạnh nhất để dẫn hướng tìm kiếm.
        """
        sorted_indices = np.argsort(self.fitness)
        best1 = self.population[sorted_indices[0]].copy()
        best2 = self.population[sorted_indices[1]].copy()
        return best1, best2

    def clip_position(self, position):
        """
        Ép vị trí về lại trong miền [lb, ub]
        để tránh cá thể bay ra khỏi không gian tìm kiếm.
        """
        return np.clip(position, self.lb, self.ub)

    def optimize(self):
        """
        Hàm chạy chính của thuật toán AVOA.

        Returns
        -------
        best_solution : numpy array
            Nghiệm tốt nhất tìm được
        best_fitness : float
            Giá trị fitness tốt nhất
        convergence_curve : list
            Danh sách fitness tốt nhất qua từng vòng lặp
        """
        # Bước 1: khởi tạo quần thể
        self.initialize_population()

        # Bước 2: đánh giá fitness ban đầu
        self.evaluate_population()

        # Bước 3: cập nhật best global
        self.update_best_solution()

        # Vòng lặp chính
        for t in range(self.max_iter):
            # Lấy 2 cá thể tốt nhất hiện tại
            best1, best2 = self.get_two_best_vultures()

            # Hệ số giảm dần theo thời gian
            # Giúp chuyển từ exploration sang exploitation
            a = 2 - 2 * (t / self.max_iter)

            new_population = np.zeros_like(self.population)

            for i in range(self.pop_size):
                current = self.population[i].copy()

                # Chọn ngẫu nhiên 1 trong 2 con tốt nhất để dẫn hướng
                if np.random.rand() < 0.5:
                    leader = best1
                else:
                    leader = best2

                # F mô phỏng trạng thái "đói / năng lượng"
                # |F| >= 1: exploration
                # |F| < 1 : exploitation
                F = a * (2 * np.random.rand() - 1)

                # vector ngẫu nhiên
                rand_vec = np.random.rand(self.dim)

                if abs(F) >= 1:
                    # ==============================
                    # Exploration: tìm kiếm toàn cục
                    # ==============================
                    random_vulture = self.population[np.random.randint(self.pop_size)]

                    # Di chuyển theo hướng ngẫu nhiên quanh leader và cá thể khác
                    new_position = leader - np.abs(
                        rand_vec * leader - current
                    ) * F + np.random.rand(self.dim) * (random_vulture - current)

                else:
                    # ==============================
                    # Exploitation: tìm kiếm cục bộ
                    # ==============================
                    # Bám quanh leader để tinh chỉnh nghiệm
                    new_position = leader - F * np.abs(leader - current)

                    # thêm một nhiễu nhỏ để tăng đa dạng
                    noise = 0.01 * np.random.randn(self.dim)
                    new_position = new_position + noise

                # Ép về miền hợp lệ
                new_position = self.clip_position(new_position)

                # Gán vào quần thể mới
                new_population[i] = new_position

            # Cập nhật quần thể
            self.population = new_population

            # Đánh giá lại fitness
            self.evaluate_population()

            # Cập nhật nghiệm tốt nhất
            self.update_best_solution()

            # Lưu lại lịch sử hội tụ
            self.convergence_curve.append(self.best_fitness)

            # In log theo dõi
            print(f"Iteration {t+1}/{self.max_iter}, Best Fitness = {self.best_fitness:.6f}")

        return self.best_solution, self.best_fitness, self.convergence_curve