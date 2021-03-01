
requirejs(['commonjs', 'apps/payments/payments'], function(common,PaymentManager){
    var payment_manager = new PaymentManager();
    payment_manager.init();
});
