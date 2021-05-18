import torch
import numpy as np
import cv2
import pyredner


class Perlin2D(object):
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

    def get_value_list(self, point_list: torch.Tensor):
        pos = point_list / self.interval

        pos_ll = pos.floor().to(torch.int64)
        pos_rr = pos_ll + 1
        pos_lr = pos_ll + torch.tensor([0, 1])
        pos_rl = pos_ll + torch.tensor([1, 0])
        tx_l = pos[:, 0] - pos_ll[:, 0]
        tx_r = pos[:, 0] - pos_rr[:, 0]
        ty_l = pos[:, 1] - pos_ll[:, 1]
        ty_r = pos[:, 1] - pos_rr[:, 1]

        v1 = self.value[pos_ll[:, 0], pos_ll[:, 1]] + self.grad_x[pos_ll[:, 0], pos_ll[:, 1]] * tx_l + self.grad_y[
            pos_ll[:, 0], pos_ll[:, 1]] * ty_l
        v2 = self.value[pos_lr[:, 0], pos_lr[:, 1]] + self.grad_x[pos_lr[:, 0], pos_lr[:, 1]] * tx_l + self.grad_y[
            pos_lr[:, 0], pos_lr[:, 1]] * ty_r
        v3 = self.value[pos_rl[:, 0], pos_rl[:, 1]] + self.grad_x[pos_rl[:, 0], pos_rl[:, 1]] * tx_r + self.grad_y[
            pos_rl[:, 0], pos_rl[:, 1]] * ty_l
        v4 = self.value[pos_rr[:, 0], pos_rr[:, 1]] + self.grad_x[pos_rr[:, 0], pos_rr[:, 1]] * tx_r + self.grad_y[
            pos_rr[:, 0], pos_rr[:, 1]] * ty_r

        def f(t):
            return 1 - 3 * t ** 2 + 2 * t ** 3

        value = v1 * f(tx_l) * f(ty_l) + v2 * f(tx_l) * f(-ty_r) \
                + v3 * f(-tx_r) * f(ty_l) + v4 * f(-tx_r) * f(-ty_r)
        return value

    def get_map(self, range_x, range_y, interval):
        ret = torch.zeros(range_x, range_y)
        x = torch.tensor(range(range_x)) * interval / self.interval
        y = torch.tensor(range(range_y)) * interval / self.interval

        xl = x.floor().to(torch.int64)
        yl = y.floor().to(torch.int64)
        xr = xl + 1
        yr = yl + 1

        x = x.reshape(-1, 1).expand(-1, range_y)
        y = y.expand(range_x, -1)
        xll = xl.reshape(-1, 1).expand(-1, range_y)
        yll = yl.expand(range_x, -1)
        xrr = xr.reshape(-1, 1).expand(-1, range_y)
        yrr = yr.expand(range_x, -1)

        v1 = self.value[xl][:, yl] + self.grad_x[xl][:, yl] * (x - xll) + self.grad_y[xl][:, yl] * (y - yll)
        v2 = self.value[xl][:, yr] + self.grad_x[xl][:, yr] * (x - xll) + self.grad_y[xl][:, yr] * (y - yrr)
        v3 = self.value[xr][:, yl] + self.grad_x[xr][:, yl] * (x - xrr) + self.grad_y[xr][:, yl] * (y - yll)
        v4 = self.value[xr][:, yr] + self.grad_x[xr][:, yr] * (x - xrr) + self.grad_y[xr][:, yr] * (y - yrr)

        def f(t):
            return 1 - 3 * t ** 2 + 2 * t ** 3

        value = v1 * f(x - xll) * f(y - yll) + v2 * f(x - xll) * f(yrr - y) \
                + v3 * f(xrr - x) * f(y - yll) + v4 * f(xrr - x) * f(yrr - y)
        return value


