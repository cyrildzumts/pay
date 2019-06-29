from django.contrib import admin
from payments.models import Reduction, Transaction, Transfer, Payment, CaseIssue

# Register your models here.



class ReductionInline(admin.StackedInline):
    model = Reduction


class TransactionInline(admin.StackedInline):
    model = Transaction


class PaymentInline(admin.StackedInline):
    model = Payment


class TransferInline(admin.StackedInline):
    model = Transfer


class CaseIssueInline(admin.StackedInline):
    model = CaseIssue



admin.site.register(Reduction)
admin.site.register(Transaction)
admin.site.register(Transfer)
admin.site.register(Payment)
admin.site.register(CaseIssue)