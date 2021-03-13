define(function(){

    var api_baseUrl = '/api/V1';
    var api_paymentBaseUrl = api_baseUrl + '/payments/';
    var api_transferBaseUrl = api_baseUrl + '/transfers/';
    console.log("Constants is ready");

    return {
        'api_baseUrl': api_baseUrl,
        'make_payment_url': api_paymentBaseUrl + "make-payment/",
        'make_transfer_url': api_transferBaseUrl + "make-transfer/"
    }
});