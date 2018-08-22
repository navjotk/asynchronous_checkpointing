from devito import Operator, Grid, TimeFunction, solve, Eq

class DevitoOperator(object):
    def __init__(self, shape, order):
        grid = Grid(shape=shape)
        c = 10.0
        u = TimeFunction(name='u', grid=grid, spc_order=order)
        eq = Eq(u.dt + c*u.dxl + c*u.dyl)
        stencil = solve(eq, u.forward)
        self.op = Operator([Eq(u.forward, stencil)])

    def apply(self, *args, **kwargs):
        t_start = kwargs['t_start']
        t_end = kwargs['t_end']
        self.op(time_m=t_start, time_M=t_end, dt=0.1, profile_output=False)



if __name__ == "__main__":
    op = DevitoOperator((10, 10), 2)
    op.apply(t_start=0, t_end=30)
