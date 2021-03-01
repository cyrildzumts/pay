
requirejs(['commonjs', 'payments/payments'], function(common,PaymentManager){
    //var PaymentManager =  require(['payments/payments']);
    console.log("PaymentManager : ", PaymentManager);
    var payment_manager = new PaymentManager();
    payment_manager.init();
});

/*
define(['apps/payments/payments', 'commonjs'], function(PaymentManager, common) {
    'use strict';
    //var PaymentManager = require('payments/payments');
    var payment_manager = new PaymentManager();
    payment_manager.init();
});
*/