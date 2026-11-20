from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    """Strategy interface: every discount takes an order total and returns the discounted total."""
    @abstractmethod
    def apply(self, total: float) -> float:
        pass


class NoDiscount(DiscountStrategy):
    def apply(self, total: float) -> float:
        return total


class PercentageDiscount(DiscountStrategy):
    """Takes a percentage off the total, e.g. PercentageDiscount(10) takes 10% off."""
    def __init__(self, percentage: float):
        self.__percentage: float = percentage

    def apply(self, total: float) -> float:
        return total * (1 - self.__percentage / 100)


class BulkDiscount(DiscountStrategy):
    """Takes a fixed amount off any total at or above the threshold,
    e.g. BulkDiscount(200, 20) takes 20 off a total of 200 or more."""
    def __init__(self, threshold: float, amount: float):
        self.__threshold: float = threshold
        self.__amount: float = amount

    def apply(self, total: float) -> float:
        return total - self.__amount if total >= self.__threshold else total


class StudentDiscount(DiscountStrategy):
    """Fourth strategy (Section 2.4): a flat 5% student discount.
    Added without changing Order."""
    def apply(self, total: float) -> float:
        return total * 0.95
