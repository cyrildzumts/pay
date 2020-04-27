


var payment_chart;
var transfers_chart;
var requests_chart;
var user_chart;
var analytics_data = [12,48,2,14,132,45,70,56,80,88,76,96];
var analytics_label = 'Payments';
var analytics_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
var chart_type = 'line';

function updateChart(){
    var options = {
        url:'/api/analytics/',
        type:'GET',
        data:{},
        dataType: 'json'
    }
    var promise = ajax(options).then(function(response){
        dispatchChartUpdate(response)
    }, function(error){
        console.log("payments fetch failed");
        console.log(error);
    });
}
function dispatchChartUpdate(response){
    var label = response.label;
    var datasets = response.datasets;
    console.log("Dispatching chart update to \"%s\"",label);
    updatePaymentChart(payment_chart, label, datasets);
}

function updatePaymentChart(chart,label, datasets){
    var payment_data = []
    datasets.forEach(dataset => {
        payment_data[dataset.month - 1] = dataset.count;
    });
    chart.data.datasets[0].data = payment_data;
    chart.update();
}

function paymentCounts(chart, label, data){
    if(!chart.data.labels.contains(label)){
        chart.data.labels.push(label);
        chart.data.datasets.push(data);
    }else{
        for(dataset in chart.data.datasets){
            if (dataset.label == data.label){

                break;
            }
        }
    }
}

function addMetric(container, data){
    var el = $('<div/>').addClass('metric');
    $('<span/>').addClass('metric-title').html(data.label).appendTo(el);
    $('<span/>').addClass('metric-value').html(data.count).appendTo(el);
    container.append(el);

}

function addReportMetric(container, data){
    var el = $('<div/>').addClass('metric');
    $('<span/>').addClass('metric-title').html(data.label).appendTo(el);
    $('<span/>').addClass('metric-value').html(data.count).appendTo(el);
    container.append(el);

}

function updateMetrics(metrics_data){
    var container = $('#metrics');
    if(container.length == 0){
        console.error("No metrics container found.");
        return;
    }
    metrics_data.forEach(data =>{
        if(data.label == "Vouchers"){
            $('#vouchers .metric-value .sold', container).text(data.sold);
            $('#vouchers .metric-value .total', container).text(data.count);
        }else if (data.label == "Payments"){
            $('#payments .metric-value', container).text(data.count);
        }else if(data.label == "Transfers"){
            $('#transfers .metric-value', container).text(data.count);
        }else if(data.label == "Payment Requests"){
            $('#p_requests .metric-value', container).text(data.count);
        }else if(data.label == "Users"){
            $('#users .metric-value', container).text(data.count);
        }else if(data.label == "Services"){
            $('#services .metric-value', container).text(data.count);
        }else{
            console.error("Metrics Error: no target found for label %s.", data.label);
        } 
    });
}

function dashboardUpdate(){
    var options = {
        url:'/api/analytics/',
        type:'GET',
        data:{},
        dataType: 'json'
    }
    var promise = ajax(options).then(function(response){
        updateMetrics(response)
    }, function(error){
        console.log("analytics fetch failed");
        console.log(error);
    });

}
$(document).ready(function(){
console.log("analytics ready");

Chart.defaults.global.elements.line.fill = false;
Chart.defaults.global.elements.line.borderWidth = 2;

var ctx_payments = $('#payments-diagram');
var ctx_transfers = $('#transfers-diagram');
var ctx_requests = $('#payment-request-diagram');
var ctx_users = $('#users-diagram');

var payments_conf = {
    type : chart_type,
    data : {
        labels : analytics_labels,
        datasets : [{
            label: 'Payments',
            data: []
        }],
    },
    options:{}
};
var transfers_conf = {
    type : chart_type,
    data : {
        labels : analytics_labels,
        datasets : [{
            label: 'Transfers',
            data: []
        }],
    },
    options:{}
};
var requests_conf = {
    type : chart_type,
    data : {
        labels : analytics_labels,
        datasets : [{
            label: 'Payment Requests',
            data: []
        }],
    },
    options:{}
};
var users_conf = {
    type : chart_type,
    data : {
        labels : analytics_labels,
        datasets : [{
            label: 'Users Online',
            data: []
        }],
    },
    options:{}
};
var empty_conf = {};
payment_chart = new Chart(ctx_payments, payments_conf);
transfers_chart = new Chart(ctx_transfers, transfers_conf);
requests_chart = new Chart(ctx_requests, requests_conf);
user_chart = new Chart(ctx_users, users_conf);
dashboardUpdate();
dashboardIntervalHandle = setInterval(dashboardUpdate,60000); // 1000*60*1 = 1min
});