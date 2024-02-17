class MotorGroup:
    def __init__(self, positives=None, negatives=None):
        self.positives = [] if positives is None else positives
        self.negatives = [] if negatives is None else negatives

    def set(self, value):
        for pos in self.positives:
            pos.set(value)

        for neg in self.negatives:
            neg.set(-value)
