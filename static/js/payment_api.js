/*
requirejs(['commonjs', 'apps/payments/payments'], function(common,PaymentManager){
    //var PaymentManager =  requirejs(['apps/payments/payments']);
    var payment_manager = new PaymentManager();
    payment_manager.init();
});
*/

define(['require', 'commonjs'], function(require, common) {
    'use strict';
    var PaymentManager = requirejs('payments/payments');
    var payment_manager = new PaymentManager();
    payment_manager.init();
});