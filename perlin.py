import torch
import numpy as np
import cv2
import pyredner


class Perlin2D:
    def __init__(self, interval=1.,
                 range_x: int = 1,
                 range_y: int = 1,
                 sigma_of_value=1.,
                 sigma_of_grad=1.):
        self.interval = interval
        self.range_x = range_x
        self.range_y = range_y
        self.sigma_of_value = sigma_of_value
        self.sigma_of_grad = sigma_of_grad
        self.value = torch.randn(range_x, range_y) * sigma_of_value
        self.grad_x = torch.randn(range_x, range_y) * sigma_of_grad
        self.grad_y = torch.randn(range_x, range_y) * sigma_of_grad

    def refresh(self):
        self.value = torch.randn(self.range_x, self.range_y) * self.sigma_of_value
        self.grad_x = torch.randn(self.range_x, self.range_y) * self.sigma_of_grad
        self.grad_y = torch.randn(self.range_x, self.range_y) * self.sigma_of_grad

    def get_value(self, real_x: float, real_y: float):
        x = real_x / self.interval
        y = real_y / self.interval
        xl = int(x)
        xr = xl + 1
        yl = int(y)
        yr = yl + 1
        assert 0 <= xl < self.range_x - 1, "range_x exceeded"
        assert 0 <= yl < self.range_y - 1, "range_y exceeded"

        v1 = self.value[xl, yl] + self.grad_x[xl, yl] * (x - xl) + self.grad_y[xl, yl] * (y - yl)
        v2 = self.value[xl, yr] + self.grad_x[xl, yr] * (x - xl) + self.grad_y[xl, yr] * (y - yr)
        v3 = self.value[xr, yl] + self.grad_x[xr, yl] * (x - xr) + self.grad_y[xr, yl] * (y - yl)
        v4 = self.value[xr, yr] + self.grad_x[xr, yr] * (x - xr) + self.grad_y[xr, yr] * (y - yr)

        def f(t):
            return 1 - 3 * t ** 2 + 2 * t ** 3

        value = v1 * f(x - xl) * f(y - yl) + v2 * f(x - xl) * f(yr - y) \
                + v3 * f(xr - x) * f(y - yl) + v4 * f(xr - x) * f(yr - y)
        return value

    def get_map(self, range_x, range_y, interval):
        ret = torch.zeros(range_x, range_y)
        y = torch.tensor(range(range_y)).expand(range_x, -1) * interval / self.interval
        x = torch.tensor(range(range_x)).reshape(-1, 1).expand(-1, range_y) * interval / self.interval
        xl = x.floor().to(torch.int64)
        yl = y.floor().to(torch.int64)
        xr = xl + 1
        yr = yl + 1
        #  not finished yet

p = Perlin2D(interval=20., range_x=100, range_y=100, sigma_of_grad=0.2, sigma_of_value=0.1)
# img = np.zeros((100, 100))
# for i in range(100):
#     for j in range(100):
#         img[i, j] = p.get_value(i, j) + 0.5
# cv2.imshow("img", img)
# cv2.imwrite("perlin.jpg", 255 * img)
# cv2.waitKey(200)
