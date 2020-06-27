number_regex = RegExp('^[0-9]+$');


function validate_transfert_form(){
    var $form = $("#transfer-form");
    var $amount = $("#amount",$form);
    var $recipient = $(".recipient", $form);
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
    }
}


$(document).ready(function(){
    var $form = $("#transfer-form");
    $("input",$form).on('keyup change', function(){
        validate_transfert_form();
    });
    $("#submit-btn", $form).addClass("disabled");
});