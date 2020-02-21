
function paymentCounts(){
    var options = {

    }
    var promise = ajax(options).then(function(response){

    }, function(error){
        console.log("payments fetch failed");
        console.log(error);
    });
}


$(document).ready(function(){
console.log("analytics ready");

var ctx_payments = $('#payments-diagram');
var ctx_transfers = $('#transfers-diagram');
var ctx_requests = $('#payment-request-diagram');
var ctx_users = $('#users-diagram');

var payment_diagram_options = {
    type : 'line',
    data : {
        labels : ['Jan', 'Feb', 'Mar', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        datasets : [{
            label: 'Payments',
            borderColor: "#009688",
            borderWidth: 2,
            data: [12,48,23,45,15,16,35,26,45,48,56,66]
        }],
    },
    options:{}
};

var payment_chart = new Chart(ctx_payments, payment_diagram_options);
});