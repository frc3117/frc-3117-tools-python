class BaseFeedForward:
    def __call__(self, ff: float, *args, **kwargs):
        return self.evaluate(ff)

    def evaluate(self, ff: float):
        raise NotImplementedError()


class ConstantFeedForward(BaseFeedForward):
    def __init__(self, constant: float):
        self.constant = constant

    def evaluate(self, ff: float):
        return self.constant
