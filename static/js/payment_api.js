
requirejs(['commonjs', 'apps/payments/payments', 'form_verification' , 'styling'], function(common,PaymentManager){
    var payment_manager = new PaymentManager();
    payment_manager.init();
});
