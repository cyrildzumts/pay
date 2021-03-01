requirejs(['commonjs'], function(common){
    var PaymentManager =  requirejs(['apps/payments/payments']);
    var payment_manager = new PaymentManager();
    payment_manager.init();
});