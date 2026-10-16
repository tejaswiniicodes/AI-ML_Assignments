# Assignment-1

from abc import ABC, abstractmethod

class PaymentMethod(ABC):

    @abstractmethod
    def get_details(self):
        pass

    @abstractmethod
    def pay(self, amount):
        pass


class RazorpayCardPayment(PaymentMethod):

    def __init__(self, card_number):
        self.card_number = card_number

    def get_details(self):
        return "Card ending in " + self.card_number[-4:]

    def pay(self, amount):
        print("Payment of Rs.", amount, "made using Razorpay Card")
        return True


class RazorpayUPIPayment(PaymentMethod):

    def __init__(self, upi_id):
        self.upi_id = upi_id

    def get_details(self):
        return self.upi_id

    def pay(self, amount):
        print("Payment of Rs.", amount, "made using Razorpay UPI")
        return True


class StripeCardPayment(PaymentMethod):

    def __init__(self, card_number):
        self.card_number = card_number

    def get_details(self):
        return "Card ending in " + self.card_number[-4:]

    def pay(self, amount):
        print("Payment of Rs.", amount, "made using Stripe Card")
        return True


class StripeUPIPayment(PaymentMethod):

    def __init__(self, upi_id):
        self.upi_id = upi_id

    def get_details(self):
        return self.upi_id

    def pay(self, amount):
        print("Payment of Rs.", amount, "made using Stripe UPI")
        return True


class FactoryPaymentMethod(ABC):

    factory = {}

    @classmethod
    def get_payment_object(cls, method_type, **kwargs):
        if method_type not in cls.factory:
            raise ValueError("Invalid payment method")

        return cls.factory[method_type](**kwargs)


class RazorpayFactory(FactoryPaymentMethod):

    factory = {
        "card": RazorpayCardPayment,
        "upi": RazorpayUPIPayment
    }


class StripeFactory(FactoryPaymentMethod):

    factory = {
        "card": StripeCardPayment,
        "upi": StripeUPIPayment
    }


class Aggregator(ABC):

    def __init__(self, name, processing_fee):
        self.name = name
        self.processing_fee = processing_fee

    @abstractmethod
    def call_get_payment_object(self, method_type, amount, **kwargs):
        pass


class RazorpayAggregator(Aggregator):

    def __init__(self):
        super().__init__("Razorpay", 2.0)

    def call_get_payment_object(self, method_type, amount, **kwargs):
        payment = RazorpayFactory.get_payment_object(
            method_type, **kwargs
        )

        print("\nGateway:", self.name)
        print("Processing fee:", self.processing_fee, "%")
        print("Payment details:", payment.get_details())

        return payment.pay(amount)


class StripeAggregator(Aggregator):

    def __init__(self):
        super().__init__("Stripe", 2.9)

    def call_get_payment_object(self, method_type, amount, **kwargs):
        payment = StripeFactory.get_payment_object(
            method_type, **kwargs
        )

        print("\nGateway:", self.name)
        print("Processing fee:", self.processing_fee, "%")
        print("Payment details:", payment.get_details())

        return payment.pay(amount)


class AggregatorFactory:

    factory = {
        "razorpay": RazorpayAggregator,
        "stripe": StripeAggregator
    }

    @classmethod
    def register_aggregator(cls, name, aggregator):
        cls.factory[name] = aggregator

    @classmethod
    def get_aggregator_object(cls, name):
        if name not in cls.factory:
            raise ValueError("Invalid payment gateway")

        return cls.factory[name]()


def main():

    print("===== MULTI-GATEWAY PAYMENT ENGINE =====")

    try:
        gateway = input("Select gateway (razorpay/stripe): ").lower()

        aggregator = AggregatorFactory.get_aggregator_object(gateway)

        method = input("Select payment method (card/upi): ").lower()

        if method == "card":
            card_number = input("Enter card number: ")
            details = {"card_number": card_number}

        elif method == "upi":
            upi_id = input("Enter UPI ID: ")
            details = {"upi_id": upi_id}

        else:
            print("Invalid payment method")
            return

        amount = float(input("Enter amount: "))

        if amount <= 0:
            print("Amount must be greater than zero")
            return

        result = aggregator.call_get_payment_object(
            method, amount, **details
        )

        if result:
            print("\nPayment successful")
        else:
            print("\nPayment failed")

    except ValueError as error:
        print("Error:", error)


if __name__ == "__main__":
    main()
