from django.contrib import admin
from payments.models import Reduction, Transaction, Transfer, Payment, CaseIssue, Service ,AvailableService, ServiceCategory

# Register your models here.


class AvailableServiceInline(admin.StackedInline):
    model = AvailableService

class ServiceCategoryInline(admin.StackedInline):
    model = ServiceCategory

class ReductionInline(admin.StackedInline):
    model = Reduction

class ServiceInline(admin.StackedInline):
    model = Service

class TransactionInline(admin.StackedInline):
    model = Transaction


class PaymentInline(admin.StackedInline):
    model = Payment


class TransferInline(admin.StackedInline):
    model = Transfer


class CaseIssueInline(admin.StackedInline):
    model = CaseIssue



admin.site.register(ServiceCategory)
admin.site.register(AvailableService)
admin.site.register(Service)
admin.site.register(Reduction)
admin.site.register(Transaction)
admin.site.register(Transfer)
admin.site.register(Payment)
admin.site.register(CaseIssue)