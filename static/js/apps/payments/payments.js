define(['require', 'constants'],function(require, Constants) {
    'use strict';

    var $ = require('jquery');
    var ajax_api = require('ajax_api');
    var PaymentManager = (function(){
        function PaymentManager() {
            this.csrfmiddlewaretoken = document.querySelector('input[name="csrfmiddlewaretoken"]');
        };
        PaymentManager.prototype.init = function(){
            this.balance = $('.balance').data('balance');
            var self = this;
            $('#transfer-form').submit(function(event){
                event.preventDefault();
                event.stopPropagation();
                self.make_transfer($(this).serialize());
                return false;

            });

            $('#payment-form').submit(function(event){
                event.preventDefault();
                event.stopPropagation();
                self.make_payment($(this).serialize());
                return false;

            });

            console.log("PaymentManager initialized.");
        };

        PaymentManager.prototype.make_payment = function(data){
            console.log("run make_payment request with data : ", data);
            var options = {
                //url : Constants.make_payment_url,
                url : '/api/dummy/',
                type:'POST',
                dataType: 'json',
                data : data
            };
            var p = ajax_api(options, true, false);
            p.then(function (response) {
                console.log(response);
            }, function(reason){
                console.log(response);
            });
        };

        PaymentManager.prototype.make_transfer = function(data){
            console.log("run make_transfer request with data : ", data);
            var options = {
                url : '/api/dummy/',
                //url : Constants.make_transfer_url,
                type:'POST',
                data : data,
                dataType: 'json',
            };
            var p = ajax_api(options, true, false);
            p.then(function (response) {
                console.log(response);
            }, function(reason){
                console.log(response);
            });
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
       
        console.log("Payment app module ready.");
    });

    return PaymentManager;
    
});