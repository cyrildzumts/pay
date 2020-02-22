
function paymentCounts(){
    var options = {

    }
    var promise = ajax(options).then(function(response){

    }, function(error){
        console.log("payments fetch failed");
        console.log(error);
    });
}

var payment_chart;
var transfers_chart;
var requests_chart;
var user_chart;
var analytics_data = [12,48,2,14,132,45,70,56,80,88,76,96];
var analytics_label = 'Payments';
var analytics_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
var chart_type = 'line';


$(document).ready(function(){
console.log("analytics ready");

var ctx_payments = $('#payments-diagram');
var ctx_transfers = $('#transfers-diagram');
var ctx_requests = $('#payment-request-diagram');
var ctx_users = $('#users-diagram');

var payment_diagram_options = {
    type : chart_type,
    data : {
        labels : analytics_labels,
        datasets : [{
            label: analytics_label,
            borderColor: "#009688",
            borderWidth: 2,
            data: analytics_data
        }],
    },
    options:{}
};

payment_chart = new Chart(ctx_payments, payment_diagram_options);
transfers_chart = new Chart(ctx_transfers, payment_diagram_options);
requests_chart = new Chart(ctx_requests, payment_diagram_options);
user_chart = new Chart(ctx_users, payment_diagram_options);
});