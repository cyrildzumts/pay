define(function(require) {
    'use strict';
    var $ = require('jquery');
    var ajax_api = require('ajax_api');
    var PaymentManager = (function(){
        function PaymentManager(params) {
            
        };
        PaymentManager.prototype.init = function(){

        };

        PaymentManager.prototype.make_payment = function(data){

        };

        PaymentManager.prototype.make_transfer = function(data){

        };

        PaymentManager.prototype.recharge = function(data){

        };

        PaymentManager.prototype.verify = function(data){

        };

        PaymentManager.prototype.fetch_balance = function(){

        };

        PaymentManager.prototype.is_recipient_seller = function(data){

        };

        PaymentManager.prototype.validate_form_transfer = function(){

        };

        PaymentManager.prototype.validate_form_payment = function(){

        };

    });
    $(function(){
        var balance = $('.balance').data('balance');
        console.log("Payment app module ready. Balance : %s", balance);
    });
    
});