
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
});