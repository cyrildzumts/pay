number_regex = RegExp('^[0-9]+$');
real_number_regex = RegExp('^[0-9]*(\.[0-9]+)?$');


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
        submitBtn.removeClass("disabled").prop("disabled", false);
    }else{
        submitBtn.addClass("disabled").prop("disabled", true);
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
    if(!real_number_regex.test($amount.val())){
        is_valid = false;
        console.log("Amount must be a number");
    }
    if($details.val().length == 0){
        is_valid = false;
        console.log("You must provide a description of the transfer");
    }
    if(is_valid){
        submitBtn.removeClass("disabled").prop("disabled", false);
    }else{
        submitBtn.addClass("disabled").prop("disabled", true);
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
        submitBtn.removeClass("disabled").prop("disabled", false);
    }else{
        submitBtn.addClass("disabled").prop("disabled", true);
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
    if(!real_number_regex.test(amount.val())){
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
        submitBtn.removeClass("disabled").prop("disabled", false);
    }else{
        submitBtn.addClass("disabled").prop("disabled", true);
    }
    return is_valid;
}

function validate_category_form(params) {
    var $form = $("#category-form");
    var submitBtn = $("#submit-btn", $form);
    var category_name = $("#category-name", $form);
    var category_code = $("#category-code", $form);
    var is_valid = true;

    if((category_name.val().length == 0)){
        is_valid = false;
        console.log("Category name is required");
    }else if (number_regex.test(category_name.val())) {
        is_valid = false;
        console.log("Category name must not be a number");
    }

    if((category_code.val().length == 0)){
        is_valid = false;
        console.log("Category code is required");
    }else if (number_regex.test(category_name.val())) {
        is_valid = false;
        console.log("Category name must not be a number");
    }
    if(is_valid){
        submitBtn.removeClass("disabled").prop("disabled", false);
    }else{
        submitBtn.addClass("disabled").prop("disabled", true);
    }
    return is_valid;


}

function validate_available_service_form(params) {
    var $form = $("#available-service-form");
    var submitBtn = $("#submit-btn", $form);
    var is_valid = true;
    var service_code = $("#service-code", $form);
    var name = $("#name", $form);
    var operator = $("#operator", $form);
    var category = $("#category", $form);
    var description = $("#description", $form);
    if(name.val().length == 0){
        is_valid = false;
        console.log("Service Name is required");
    }
    if(service_code.val().length == 0){
        is_valid = false;
        console.log("Service code is required");
    }else if(!number_regex.test(service_code.val())){
        is_valid = false;
        console.log("Service Code must be a number");
    }
    if(operator.val().length == 0){
        is_valid = false;
        console.log("Operator is required");
    }else if(number_regex.test(operator.val())){
        is_valid = false;
        console.log("Operator must be a number")
    }
    if(category.val().length == 0){
        is_valid = false;
        console.log("Category is required");
    }else if(number_regex.test(category.val())){
        is_valid = false;
        console.log("Category must be a number")
    }
    if(description.val().length == 0){
        is_valid = false;
        console.log("Service Description is required");
    }
    if(is_valid){
        submitBtn.removeClass("disabled").prop("disabled", false);
    }else{
        submitBtn.addClass("disabled").prop("disabled", true);
    }
    return is_valid;
}

function validate_policy_form(){
    var $form = $("#policy-form");
    var submitBtn = $("#submit-btn", $form);
    var is_valid = true;
    var daily_limit = $("#daily-limit", $form);
    var weekly_limit = $("#weekly-limit", $form);
    var monthly_limit = $("#monthly-limit", $form);
    var commission = $("#commission", $form);

    if(daily_limit.val().length == 0){
        is_valid = false;
        console.log("Daily limit is required");
    }else if(!real_number_regex.test(daily_limit.val())){
        is_valid = false;
        console.log("Dailylimit must be a number");
    }

    if(weekly_limit.val().length == 0){
        is_valid = false;
        console.log("Weekly limit is required");
    }else if(!real_number_regex.test(weekly_limit.val())){
        is_valid = false;
        console.log("Weekly limit must be a number");
    }

    if(monthly_limit.val().length == 0){
        is_valid = false;
        console.log("monthly limit is required");
    }else if(!real_number_regex.test(monthly_limit.val())){
        is_valid = false;
        console.log("monthly limit must be a number");
    }

    if(commission.val().length == 0){
        is_valid = false;
        console.log("commission is required");
    }else if(!real_number_regex.test(commission.val())){
        is_valid = false;
        console.log("Commission must be a number");
    }

    if(is_valid){
        submitBtn.removeClass("disabled").prop("disabled", false);
    }else{
        submitBtn.addClass("disabled").prop("disabled", true);
    }
    return is_valid;
}

$(document).ready(function(){
    var $transfer_form = $("#transfer-form");
    var $payment_form = $("#payment-form");
    var $recharge_form = $("#recharge-form");
    var $service_form = $("#service-form");
    var $category_form = $("#category-form");
    var $policy_form = $("#policy-form");
    var $available_service_form = $("#available-service-form");
    $("input",$transfer_form).on('keyup change', validate_transfert_form);
    $("input",$payment_form).on('keyup change', validate_payment_form);
    $("input",$recharge_form).on('keyup change', validate_recharge_form);
    $("input",$service_form).on('keyup change', validate_service_form);
    $("input", $category_form).on('keyup change',validate_category_form);
    $("input", $policy_form).on('keyup change',validate_policy_form);
    $("input", $available_service_form).on('keyup change',validate_available_service_form);

    $transfer_form.on("submit", validate_transfert_form);
    $payment_form.on("submit", validate_payment_form);
    $recharge_form.on("submit", validate_recharge_form);
    $service_form.on("submit", validate_service_form);
    $available_service_form.on("submit", validate_available_service_form);
    $policy_form.on("submit", validate_policy_form);
    $category_form.on("submit", validate_category_form);

    $("#submit-btn").addClass("disabled").prop("disabled", true);
});