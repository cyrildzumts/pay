jQuery(".add-to-cartt").click(function(){
    var item_id = parseInt(jQuery(this).attr("data-itemid"));
    var is_available = jQuery(this).attr("data-available");
    console.log("Item availability : " + is_available);
    if(is_available != "False")
        {
            cart_add_item(item_id, 1);
        }
    else{

    }

})

function cart_add_item(id, quantity)
{
    print("Cart Add Item ...clicked");

    $.ajax({
        type: 'POST',
        url : '/cart/add_to_cart/',
        data: {product_id: id, quantity: quantity},
        dataType: 'json',
        // success Function called in case of an http 200 response
        success: function(response){
            cart_edit_confirm(response);
        },
        error: function (){
            alert("Il y a une erreur, Veuillez reessayer.");
        }
    });
}

function print(str)
{
    console.log(str);
}

function update_input(element, value)
{
    var el = element;
    el.parent().attr("data-quantity", value);
     el.val(value);
}
function cart_update(inputElement, product_id, quantity)
{
    if(! isNaN(product_id) &&  ! isNaN(quantity))
    {
        $.ajax(
            {
                type : 'POST',
                url: '/cart/cart_update/',
                data:{product_id: product_id, quantity:quantity},
                dataType: 'json',
                success: function(response){
                    //update_input(inputElement, response.count);
                    //cart_edit_confirm(response);
                    location.reload();
                    print("Quittin onsuccess func  ...");
                },
                error: cart_edit_error
            });
    }
    print("Quittin cart_update ...");
}
/**
 This  function update the cart badge and display
 a popover confirming that the item has been added
 */
function cart_edit_confirm(response)
{
    //update the cart icon counter
    print("cart_edit_confirm :  count " + response.count);
    update_cart_icon(response.count);

}

function cart_edit_error()
{
    print("cart_edit_error is not implemented yet ...");
}
/**
    hideItemAdded : the function to be called on setTimeout
    */
function update_cart_icon(count)
{
jQuery(".cart_badge").html(count);
//setTimeout()
jQuery(".item_added").click();
setTimeout(hideItemAdded, 3000);
}

function hideItemAdded()
{
    jQuery(".item_added").trigger("click");
}

var help_text = "Debug Helper : ";
function debugHelper(node)
{
    print(help_text + node);
    print(help_text + " Node Parent : " + node.parentNode);
    //input = node.parentNode.getElementsByTagName('input')[0];
}

jQuery("input.quantity").keypress(function(e){
    if(e.which == 13)
    {
        print("Enter pressed ...");
        print("Input value : " +  $(this).val());
    }
});
jQuery(".add_item").click(function(){
    displayAttribute($(this), true);
});
/*
jQuery(".remove_item").click(function(){

    node = $(this);
    console.log("remove item clicked");
    displayAttribute(node, false);
});
*/
/*
jQuery(".delete").click(function(){
    print("Delete Item clicked " + this);
    node = $(this);
    displayAttribute(node, false, true);
});
*/
function displayAttribute(node, added, del){
    /**
    * node : a JSON representing an HTML element
    * added : a flag defining whether it was add_item clicked or
    * remove_item .
    */
    // This function search for input element present in a node

    var parent = node.parent();
    var item_id = parseInt(parent.attr("data-itemid"));
    var quantity = parseInt(parent.attr("data-quantity"));
    var old_quantity = quantity;
    if(added == true)
    {
        quantity = old_quantity + 1;
        if(quantity > 1)
        {
            print("displaying remove item ");
            node.siblings(".remove_item").show();
        }
    }
    else
     {
         if(quantity > 0)
         {
             quantity =  old_quantity -1;
             if(quantity < 2)
             {
                 print("hiding remove item ");
                //node.hide();
             }

         }

    }
    if(del == true)
        quantity = 0;
    parent.attr("data-quantity", quantity);
    var temp = {};
    temp.parent = parent;
    temp.item_id = item_id;
    temp.old_quantity = old_quantity;
    temp.quantity = quantity;
    temp.input = node.siblings("input");
    //temp.input.val(quantity);
    //print("Item Parent : " + temp.parent);
    //print("Parent Attributes : ");
    //print("Item ID : " +  temp.item_id );
    //print("Item Old Quantity : " + temp.old_quantity);
    //print("Item Quantity : " + quantity);
    //print("Input : " + temp.input );
    //print("Input Value : " + temp.input.val() );
    cart_update(temp.input, temp.item_id, temp.quantity);
    return temp;
}
