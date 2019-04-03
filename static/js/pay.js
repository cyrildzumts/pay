var Tabs = (function(){
    function Tabs(){
        this.currentTab     = 0;
        this.tabCount       = 0;
        this.tabs           = {};
        this.tab            = {};
        this.tabsCount      = 0;
        
    };

    Tabs.prototype.init = function(){
        this.tabsCount = $(".tabs").length;
        this.tabs = $(".tab-content");
        this.tab = $(".tab");
        this.tabCount = this.tab.length;
        if(this.tabCount == 0){
            return;
        }
        
        $('div.tab-container').each(function(){
            console.log("tab-container init...");
            $(this).find('div.tab-content:eq(0)').nextAll().hide();
        });
        //this.tabs.hide();
        $('div.tab-bar .tab').click(function(){
            var current = $(this);
            console.log("Tab clicked");
            console.log("current data : ", current.data('toggle'));
            
            if(!current.hasClass('active')){
                console.log("Has no class active");
                current.addClass('active').siblings().removeClass('active');
                $(current.data('toggle')).show().siblings('div.tab-content').hide();
            }
        });
    };
    Tabs.prototype.onTabClicked = function(event){
        var tab = parseInt($(event.target).data("index"));
        if(tab != this.currentTab){
            console.log("Tabs Plugin : Tab Clicked");
            this.currentTab = tab;
                this.update();
        }
    };
    Tabs.prototype.update = function(){
        this.tab.removeClass("active");
        $(this.tab[this.currentTab]).addClass("active");
        var that = this;
        this.tabs.hide();
        $(this.tabs[this.currentTab]).show();
    };
    return Tabs;
})();



var Slider = (function(){
    function Slider(){
        images_src = ['customer.png', 'businessman.png'];
    };

    Slider.prototype.init = function(){
       var slider =  $('#slider');
       var slides= slider.find('.slide');
       if(slides.length == 0){
           console.log("No slide found in this page");
           return;
       }

       console.log("slide found in this page : ", slides.length);
       slides.nextAll().hide();
       slides.first().html("I'm Slide 1");
    };

    return Slider;
})();


var Account = (function(){
    function Account(){
        this.is_logged = false;
    };

    Account.prototype.init = function(){
        $(".dialog-btn").click(function(event){
            var target = $(this).data('target');
            $(target).toggle();
         });
         $(".close").click(function(event){
            var target = $(this).data('target');
            $(target).hide();
         });
         var lang_form = $("#lang-form");
         var input = $("#current-lang");
         lang_form.submit(function(event){
            //event.preventDefault();
            console.log("lang-form submitted");
            return true;
         });
         $(".js-lang").click(function(event){
            var span = $(this);
            if(!span.hasClass("active")){
                console.log("span content [lang] : ");
                console.log(span.text());
                input.val(span.text());
            }
         });
         var login_form = $("#login-form");
         var transaction_form = $('#transaction-form');
         if(login_form.length == 0){
             console.log("no Login form found in this page");
             return;
         }
         else{
            console.log("Login form found in this page");
            login_form.submit(function(event){
                //event.preventDefault();
                var flag = false;
                console.log("Login received");
                var username = $('input[name="username"]', login_form).val();
                var password = $('input[name="password"]', login_form).val();
                var error_div = $("#error-login", login_form);
                var error_msg = "";
                if((username.length > 0) && (password.length > 0)){
                    
                    error_div.hide();
                    console.log("form : username = ", username);
                    console.log("form : password = ", password);
                    flag = true;
                }
                else{
                    error_msg = "Votre nom d'utilisateur ou votre mot est incoreecte. Veuillez verifier ces informations et essayez à nouveau."
                    console.log("form error : username or password is empty.");
                    error_div.html(error_msg).show();
                }
                return flag;
             });
         }
        if(transaction_form.length != 0){
            transaction_form.submit(function(event){
                //event.preventDefault();
                var flag = false;
                var error_div = $("#error-login", login_form);
                var error_msg = "";
                var recipient =  $('input[name="recipient"]', transaction_form).val();
                var amount =  $('input[name="amount"]', transaction_form).val();
                var details =  $('input[name="details"]', transaction_form).val();
                if((recipient.length > 0) && (details.length > 0) ){
                    if(parseInt(amount) > 0 ){
                        flag = true;
                        error_div.hide();
                    }
                    else{
                        flag = false;
                        error_msg = "Verifier les informations saisies."
                        error_div.html(error_msg).show();
                    }
                    
                }

                return flag;
            });
        }
         
         
        

         
    };

    return Account;
})();

account = new Account();
account.init();
tabs = new Tabs();
tabs.init();
slider = new Slider();
slider.init();