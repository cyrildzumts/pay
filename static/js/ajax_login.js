 function ShoppingLogin(){
    this.username = "";
    this.loginState = false;
    this.cart = [];
    this.isLoggedIn = function(){
        return this.loginState;
    };
    this.setLoginState = function(state){
        this.loginState = state;
    };
    this.getUsername = function(){
        return this.username;
    };
    this.setUsername = function(username){
        this.username = username;
    };
    this.addToCart = function(itemID){
        this.cart.push(itemID);
    };
    this.getCartItem = function(index){
        if(index >= 0 && index < this.cart.length)
            {
                return this.cart[index];
            }
        return NaN;
    };
};

var ShoppingLogin = new ShoppingLogin();



$("#login_form_flat").submit(function(){
    $.ajax({
        type: $(this).attr('method'),
        url : '/api/ajax/ajax_login/',
        data: $('#login_form').serialize(),
        dataType: 'json',
        // success Function called in case of an http 200 response
        success: function(data){
            if(data.status == 200){
                text = "Connexion reussie ";
            }
            else {
                text = "erreur de connexion - veuillez ressayer";
            }
            document.getElementById("server_response").innerHTML = text;
        }

    });
});
$("#login_form").submit(function(event){
    event.stopPropagation();
    var username = document.forms["login_form"]["username"].value;
    var password = document.forms["login_form"]["password"].value;
    if(username == "" || password == "")
        return false;
    ShoppingLogin.setUsername(username);
    console.log("ShoppingLogin.username set to " + ShoppingLogin.getUsername());
    console.log("username set to " + username);
    return true;
});
