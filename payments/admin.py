from django.contrib import admin
from payments.models import Reduction, Transaction, Payment, CaseIssue

# Register your models here.



class ReductionInline(admin.StackedInline):
    model = Reduction


class TransactionInline(admin.StackedInline):
    model = Transaction


class PaymentInline(admin.StackedInline):
    model = Payment


class CaseIssueInline(admin.StackedInline):
    model = CaseIssue



admin.site.register(Reduction)
admin.site.register(Transaction)
admin.site.register(Payment)
admin.site.register(CaseIssue)