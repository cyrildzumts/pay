number_regex = RegExp('^[0-9]+$');


function validate_transfert_form(){
    var $form = $("#transfer-form");
    var $amount = $("#amount",$form);
    var $recipient = $("#recipient", $form);
    var $details = $("#details", $form);
    var is_valid = true;
    var submitBtn = $("#submit-btn", $form);
    if($recipient.val().length == 0){
        is_valid = false;
        console.log("Recipient is missing");

    }
    if(!number_regex.test($amount.val())){
        is_valid = false;
        console.log("Amount must be a number");
    }
    if($details.val().length == 0){
        is_valid = false;
        console.log("You must provide a description of the transfer");
    }
    if(is_valid){
        submitBtn.removeClass("disabled");
    }else{
        submitBtn.addClass("disabled");
    }
    return is_valid;
}

function validate_payment_form(){
    var $form = $("#payment-form");
    var $amount = $("#amount",$form);
    var $recipient = $("#recipient", $form);
    var $details = $("#details", $form);
    var is_valid = true;
    var submitBtn = $("#submit-btn", $form);
    if($recipient.val().length == 0){
        is_valid = false;
        console.log("Recipient is missing");

    }
    if(!number_regex.test($amount.val())){
        is_valid = false;
        console.log("Amount must be a number");
    }
    if($details.val().length == 0){
        is_valid = false;
        console.log("You must provide a description of the transfer");
    }
    if(is_valid){
        submitBtn.removeClass("disabled");
    }else{
        submitBtn.addClass("disabled");
    }
    return is_valid;
}

function validate_recharge_form(){
    var $form = $("#recharge-form");
    var $voucher = $("#voucher",$form);
    var is_valid = true;
    var submitBtn = $("#submit-btn", $form);
    if($voucher.val().length == 0){
        is_valid = false;
        console.log("Voucher is missing");
    }
    if(is_valid){
        submitBtn.removeClass("disabled");
    }else{
        submitBtn.addClass("disabled");
    }
    return is_valid;
}

function validate_service_form(){
    var $form = $("#service-form");
    var submitBtn = $("#submit-btn", $form);
    var service_name = $("#name", $form);
    var reference_number = $("#reference-number", $form);
    var customer_reference = $("#customer-reference", $form);
    var amount = $("#amount", $form);
    var issue_date = $("#issue-date", $form);
    var details = $("#details", $form);

    var is_valid = true;
    if(service_name.val().length == 0){
        is_valid = false;
        console.log("Service name required");
    }
    if(reference_number.val().length == 0){
        is_valid = false;
        console.log("Reference number required");
    }
    if(customer_reference.val().length == 0){
        is_valid = false;
        console.log("Customer Reference required");
    }
    if(!number_regex.test(amount.val())){
        is_valid = false;
        console.log("Amount is required and must be a number");
    }
    if(issue_date.val().length == 0){
        is_valid = false;
        console.log("issue date is required");
    }
    if(details.val().length == 0){
        is_valid = false;
        console.log("Details is required");
    }
    if(is_valid){
        submitBtn.removeClass("disabled");
    }else{
        submitBtn.addClass("disabled");
    }
    return is_valid;
}


$(document).ready(function(){
    var $transfer_form = $("#transfer-form");
    var $payment_form = $("#payment-form");
    var $recharge_form = $("#recharge-form");
    var $service_form = $("#service-form");
    $("input",$transfer_form).on('keyup change', function(){
        validate_transfert_form();
    });
    $("input",$payment_form).on('keyup change', function(){
        validate_payment_form();
    });
    $("input",$recharge_form).on('keyup change', function(){
        validate_recharge_form();
    });
    $("input",$service_form).on('keyup change', function(){
        validate_service_form();
    });
    $transfer_form.on("submit", validate_transfert_form);
    $payment_form.on("submit", validate_payment_form);
    $recharge_form.on("submit", validate_recharge_form);
    $service_form.on("submit", validate_service_form);

    $("#submit-btn", $form).addClass("disabled");
});