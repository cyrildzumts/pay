






class PaymentService :
    

    @classmethod
    def make_payment(cls, request):
        pass
    

    @classmethod
    def is_payment_validated(cls, request):
        return False
    
    @classmethod
    def extract_participants(cls, request):
        participants = {}
        participants['receiver_id'] = None
        participants['sender_id'] = None
        return None
    
    @classmethod
    def extract_amount(cls, request):
        return 0
    

    @classmethod
    def can_customer_pay(cls, customer_id):
        return False