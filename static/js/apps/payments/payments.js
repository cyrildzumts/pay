define(function(require) {
    'use strict';
    var $ = require('jquery');
    var ajax_api = require('ajax_api');
    var PaymentManager = (function(){
        function PaymentManager(params) {
            this.csrfmiddlewaretoken = document.querySelector('input[name="csrfmiddlewaretoken"]');
        };
        PaymentManager.prototype.init = function(){
            this.balance = $('.balance').data('balance');
            var self = this;
            $('#tranfer-form').on('submit', function(event){
                event.preventDefault();
                event.stopPropagation();
                self.make_transfer($(this).serialize());

            });

            $('#payment-form').on('submit', function(event){
                event.preventDefault();
                event.stopPropagation();
                self.make_payment($(this).serialize());

            });

        };

        PaymentManager.prototype.make_payment = function(data){
            console.log("run make_payment request");

        };

        PaymentManager.prototype.make_transfer = function(data){
            console.log("run make_transfer request");
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

        return PaymentManager;

    })();
    $(function(){
       
        console.log("Payment app module ready. Balance : %s", balance);
    });
    
});