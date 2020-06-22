function account_form_validation(){
    console.log("Account form validation not implemented yet.")
    return true;
}


function activate_editable_inputs(context){
    console.debug("activating editableinputs");
    var $editable_inputs = $('input.js-editable', context);
    $editable_inputs.addClass('editable').prop('disabled', false);

}

function deactivate_editable_inputs(context){
    console.debug("deactivating editableinputs");
    var $editable_inputs = $('input.js-editable', context);
    $editable_inputs.removeClass('editable').prop('disabled', true);;
}


function init(){
    var $editable_inputs = $('input.js-editable');
    $editable_inputs.removeClass('editable').prop('disabled', true);;
    $('#form-controls').hide();
}

$(document).ready(function(){
    init();
    $('.js-edit-form').on('click', function(event){
        var ctx = $($(this).data('target'));
        $(this).addClass('disabled');
        activate_editable_inputs(ctx);
        $('#form-controls').show();
    });

    $('.js-form-edit-cancel').on('click', function(event){
        event.preventDefault();
        var ctx = $($(this).data('target'));
        var hide_el = $($(this).data('hide'));
        hide_el.hide();
        $('.js-edit-form').removeClass('disabled');
        deactivate_editable_inputs(ctx);
    });
});