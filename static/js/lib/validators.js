function search_form_validation(form){
    return $("input[name='q']").val() != "";
}

function coupon_validation(form){
    if (typeof form == 'undefined'){
        console.warn('no coupon form found. Validation not possible');
        return false;
    }
    let added_by = $('input[name="added_by"]', form);
    let name = $('input[name="name"]', form);
    let reduction = $('input[name="reduction"]', form);
    let seller = $('input[name="seller"]', form);
    let begin_at = $('input[name="begin_at"]', form);
    let expire_at = $('input[name="expire_at"]', form);
    if(added_by.val().length == 0){
        console.warn('added_by field is requiered');
        return false;
    }
    var flag = name.val().length == 0;
    name.toggleClass('warn', flag);
    if(flag){
        console.warn('name field is requiered');
        return false;
    }
   
    flag = reduction.val().length == 0;
    reduction.toggleClass('warn', flag);
    if(flag){
        console.warn('reduction field is requiered');
        return false;
    }
    
    flag = seller.val().length == 0;
    seller.toggleClass('warn', flag);
    if(flag){
        console.warn('seller field is requiered');
        return false;
    }
    
    flag = begin_at.val().length == 0;
    begin_at.toggleClass('warn', flag);
    if(flag){
        console.warn('begin_at field is requiered');
        return false;
    }
    
    flag = expire_at.val().length == 0;
    expire_at.toggleClass('warn', flag);
    if(expire_at.val().length == 0){
        console.warn('expire_at field is requiered');
        return false;
    }
    
    
    var begin_date = new Date(begin_at.val());
    var expire_date = new Date(expire_at.val());

    flag = begin_date.getTime() < Date.now();
    begin_at.toggleClass('warn', flag);
    if(flag){
        console.warn('begin_at field is invalid. it is on the past.');
        return false;
    }
    
    flag = begin_date.getTime() > expire_date.getTime();
    begin_at.toggleClass('warn', flag);
    expire_at.toggleClass('warn', flag);
    if(flag){
        console.warn('begin_at field is bigger than the expire_at field');
        return false;
    }

    return true;

}


