def calculate_total(prices):
    return sum(prices)

class ServiceStatus:
    def __init__(self, ready=True):
        self.ready = ready
