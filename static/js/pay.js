
function ajax(options){
    return new Promise(function(resolve, reject){
        $.ajax(options).done(resolve).fail(reject);
    });
}

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
                lang_form.submit();
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


var CardFactory = (function(){
    function CardFactory(options){
        this.required_keys = ["label", "label_attr_title", "title", "date", "amount", "initials", "initials_title", "is_seller"];
        this.default_option = options;
        this.template = $('#list-card-template');
        this.template_found = this.template.length > 0;
    }

    CardFactory.prototype.isOptionsValide = function(options){
        var flag = true;
        if(options){
            if (Object.keys(options).length < 0){
                flag = false;
            }
            else{
                flag = this.required_keys.every(function(key, index){
                    return options.hasOwnProperty(key);
                });
            }
        }
        else{
            flag = false;
        }
        return flag;
    };

    CardFactory.prototype.createCard = function(options){
        var card = null;
        if(this.isOptionsValide(options)){
            if(this.template_found){
                var $template = this.template.clone();
                $('.card-label', $template).attr('title', options.label_attr_title).html(options.label);
                $('.list-card-title', $template).html(options.title);
                $('.date', $template).html(options.date);
                $('.amount', $template).html(options.amount);
                $('.member-initials', $template).attr('title', options.initials_title).html(options.initials);
                if(options.is_seller){
                    $('.member-is-a-seller', $template).attr('title', 'Ce membre est un prestataire de services').removeClass('hide');
                }
                card = $template;
                card.removeAttr('id');
            }
            else{
                console.log('No card template could be found');
            }
            

        }
        else{
            console.log('No valid card actions');
        }
        return card;
    };

    CardFactory.prototype.default_card = function(){
        return this.createCard(this.default_option);
    }


    return CardFactory;
})();

var Transaction = (function(){
    function Transaction(){
        this.template =$("#transaction-form-wrapper.template");
        this.init();
        
    }

    Transaction.prototype.init = function(){
        this.re = RegExp('^[0-9]+$');
        var form = $('.template #transaction-form');
        console.log("Intialization transaction Form.");
        if(form.length == 0){
            console.log("transaction Form not found.");
            return;
        }
        regex = this.re;
        console.log("Found transaction Form.");
        $("#transaction-modal .modal-body").on("submit","#transaction-form", function(event){
            var form = $(this);
            var flag = true;
            event.preventDefault();
            var recipient = $("#recipient", this).val();
            var amount = 0;
            var amount_val = $("#amount", this).val();
            var description = $("#description", this).val();
            var fields = [recipient, amount_val, description];
            var errors_fields = $("#recipient-error , #amount-error , #description-error",this);
            
            fields.forEach(function(field, index){
                //console.log("Field #\n",index);
                if(field.length > 0){
                    $(errors_fields[index]).hide();
                }else{
                    //console.log("Field #", index, " is incorrect\n");
                    $(errors_fields[index]).show();
                    flag = false;
                }
            });
            if(!regex.test(amount_val)){
                $('#amount-error', this).html('Le montant doit être un numbre').show();
                console.log("the field amount must be a number");
            }
            else{
                amount = parseInt(amount_val);
            }
            if(flag){
                console.log("Recipient : ", recipient, "Amount : ", amount, "Description : ", description);
            }
            
            return flag;
        });
        
    };

    Transaction.prototype.create = function(){
        var transaction = null;
        transaction = this.template.clone().removeClass("template");
        console.log("new transaction element created");
        return transaction;
    };

    return Transaction;
})();

var CaseIssue = (function(){
    function CaseIssue(options){
        console.log("Issue construction...");
        this.template = $("#case-form-wrapper.template");
        if(options && options.selector){
            this.form_selector = options.selector;
        }
        else{
            this.form_selector = "#case-form";
        }
        console.log("Issue constructed ...");
        this.init();

    }

    CaseIssue.prototype.init = function(){
        if(this.form_selector){
            this.form = $(this.form_selector);
            if(this.form.length == 0){
                console.log("No Case Issue form found on this page");
                return;
            }
            var form = this.form;
            $(".modal .modal-body").on("submit", "#case-form",function(event){
            event.preventDefault();
            var flag = true;
            
            var $reporter = $("#reporter", this);
            var $participant = $("#participant", this);
            var $reference = $("#reference", this);
            var $description = $("#case-description", this);

            var reporter = $reporter.val();
            var participant = $participant.val();
            var reference = $reference.val();
            var description = $description.val();
            var fields = [participant, reference, description];
            var errors_fields = $("#participant-error , #reference-error , #case-description-error",this);
            
            fields.forEach(function(field, index){
                //console.log("Field #\n",index);
                if(field.length > 0){
                    $(errors_fields[index]).hide();
                }else{
                    //console.log("Field #", index, " is incorrect\n");
                    $(errors_fields[index]).show();
                    flag = false;
                }
            });
            if(flag){
                console.log("Reporter : ", reporter, " - Participant : ", participant, " - Ref : ", reference, " - Description : ", description);
            }
            else{
                console.log("The issue form contains invalid fields");
            }
            return flag;
            });
        }
        else{
            return;
        }

    };

    CaseIssue.prototype.create = function(){
        var issue = null;
        issue = this.template.clone().removeClass("template");
        console.log("new CaseIssue element created");
        return issue;
    };

    return CaseIssue;
})();


var Modal = (function(){
    function Modal(options){
        this.init();
        if(options ){
            this.transaction_factory = options.transaction_factory;
            this.factories = options.factories;
        }
        

    }


    Modal.prototype.init = function(){
        that = this;
        var trigger = $(".open-modal").click(function(event){
            var target = $($(this).data('target'));
            //console.log("opening modal ...");
            var options = {template: $(this).data('template'), modal: $(this).data('target'), factory:$(this).data('factory')};
            that.create(options);
            target.show();
        });

        $("body .modal").on("click", ".close-modal", function(event){
            //console.log("Close modal clicked");
            var target = $($(this).data('target'));
            target.hide();
            $(".modal-content .modal-body", target).empty();

        });
        if(window){
            $(window).click(function(event){
                var target = $(event.target);
                if(target.hasClass("modal")){
                    //console.log("Closing current modal");
                    target.hide();
                    $(".modal-content .modal-body", target).empty();
                }
            });
        }
    }

    Modal.prototype.create = function(options){
        var template = this.factories[options.factory].create();
        var modal = $(options.modal);
        $(".modal-content .modal-body", modal).append(template);
        //console.log("added into the modal");

    }
    return Modal;
})();


var Notify = (function(){
    function Notify(){
        this.template = $("#notify");
    }

    Notify.prototype.init = function(){
        $(".modal .modal-body").on("click", "#notify .close", function(event){
            var target = $($(this).data("target"));
            target.hide();
            $(".modal-body", target).empty();
        });

    };

    Notify.prototype.notify = function(data){
        if(data && data.hasOwnProperty('msg')){
            alert(data.msg);
        }
        else{
            alert("Notify called with wrong parameters");
        }
    };

    Notify.prototype.create = function(){

        var template = null;
        template = this.template.clone().removeClass("template");
        console.log("new Notification template element created");
        return template;
    };

    return Notify;
})();



var Collapsible = (function(){
    function Collapsible(){
        this.$collapsible   = {}; // all element with collapsible class
        this.$close         = {}; // all button used to close a collapsible elements.

    }
    Collapsible.prototype.init = function(){
        console.log("Initializing Collapsible ...");
        this.$collapsible = $(".collapsible");
        //this.$close = this.$collapsible.find(".close");
        
        if(this.$collapsible.length == 0){
            console.log("No collapsible found on this page.");
            return;
        }
        console.log("Found " + this.$collapsible.length + " collapsibles on this pages.");
        $(this.$collapsible).on("click", ".open", function(event){
            console.log("collapsible clicked");
            var target =$(event.target).data("target");
            //var taret = $(this).siblings("collapse-content");
            if(target == undefined){
                $(this).parent().children("collapse-content").toggle();
            }
            else{
                $(target).toggle();
                console.log("Target : " + target);
            }
        });

        $(this.$collapsible).on("click", ".close", function(event){
            event.stopPropagation();
            console.log("collapsible closing ...");
            var target =$(event.target).data("target");

            if(target == undefined){
                $(this).parent().children("collapse-content").toggle();
            }
            else{
                $(target).toggle();
                console.log("Target : " + target);
            }
        });

        console.log("Initializing Collapsible done.");
    };

    return Collapsible;
})();

//var trans = new Transaction();
var issue_descr = "J'ai acheter un article le 23.03.2019."
" Jusqu'aujourd'hui je n'ai toujours pas recu la commande."
" Je souhaite recevoir mon article dans les plus bref delai sinon j'aimerai me faire rembourser.";

var options = {label: 'Reception', label_attr_title: 'Entrant', title: 'Reception venant de Cyrille', date: '04-05-2019', amount: 25000, initials: 'CN',initials_title: 'Cyrille Ngassam', is_seller: false};



var notify = new Notify();


function fetchTransaction(){
    $.ajax({
        url: "transactions",
        type: 'post',
        success : function(data){
            notify.notify({msg: "Nouvell Transaction sur votre compte"});
        },
        error: function(data){
            notify.notify({msg: "Error : Votre compte n'a pas pu etre actualisé"});
        },
        complete: function(data){
            setTimeout(fetchTransaction, 60000);
        }
    });
}

$(document).ready(function(){
let account = new Account();
account.init();
let tabs = new Tabs();
tabs.init();
let slider = new Slider();
slider.init();
    var factory = new CardFactory(options);
    var list = $('.list-cards');
    var transaction = new Transaction();
    var cases = new CaseIssue();
    var collapsible = new Collapsible();
    collapsible.init();
    
    var modal = new Modal({transaction_factory: transaction, factories: {transaction : transaction, cases : cases, notify : notify}});

    //setTimeout(fetchTransaction, 60000);
    $('.js-add-another').click(function(event){
        var card = factory.default_card();
        if(card != null){
            card.appendTo(list).addClass('list-card').hide().fadeIn(600);
            console.log("Added new card");
        }
        else{
            console.log("Card not created");
        }
        
    });
});


