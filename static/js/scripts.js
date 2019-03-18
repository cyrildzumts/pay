

/*import {Dispatcher,Subscriber,Publisher} from './lib/pubsub.js';*/



// display an error message when the
function displayLoginError(){
  $("form.login").submit(function(){
    username = $("#username").val();
    password = $("#password").val();
    if(!(username != "" && password !="")){
        alert("Veuillez saisir le nom d'utilsateur et le mot de passe.");
        return false;
    }
  });
}
$(".search-form").submit(function(){
    var q = document.forms["search-form"]["q"].value;
    if(q == "")
        return false;
    return true;
});

function ajax(options){
    return new Promise(function(resolve, reject){
        $.ajax(options).done(resolve).fail(reject);
    });
}

// PUBLISHER - SUBSCRIBER MODULES

/**
 * Integer Constant used to represent TOPICS
 * The Client is of course free not to use it.
 * 0 - SearchResults
 * 1 - SortingOrderChanged
 * 2 - FILTERCHANGED
 * 3 - NewsletterRegister
 * 4 - CartAddItem
 * 5 - CartRemoveItem
 * 6 - CartRemoveAll
 * 7 - WishlistAddItem
 * 8 - WishlistRemoveItem
 * 9 - WishlistRemoveAll
 * 10 - LoginFormSubmit
 * 11 -  LogoutSent
 * 12 - CheckoutSubmit
 * 
 */

const PUBSUBTOPIC = {
    SEARCH : '/search',
    SEARCHRESULT : '/search/results/',
    SORTINGLOWERPRICE : '/sorting/lowerprice',
    SORTINGHIGHERPRICE: '/sorting/higherprice',
    SORTINGTOPARTCIEL  : '/sorting/top',
    SORTINGMOSTRECENT  : '/sorting/mostrecent',
    FILTERBRAND        : '/filter/brands',
    NEWSLETTERREGISTER : '/newsletter/register',
    CARTADDITEM        : '/card/add',
    CARTADDITEMFAILED  : '/card/add/failed',
    CARTREMOVEITEM     : '/card/remove',
    CARTUPDATE         : '/cart/update',
    CARTUPDATESUCCESS  : '/cart/update/success',
    CARTUPDATEFAILED   : '/cart/update/failed',
    CARTREMOVEITEMFAILED : '/card/remove/failed',
    CARTCLEAR          : '/card/clear',
    WISHLISTADD        : '/wishlist/add',
    WISHLISTREMOVE     : '/wishlist/remove',
    WISHLISTCLEAR      : '/wishlist/clear',
    WISHLISTADDTOCART  : '/wishlist/cart-add',
    CHECKOUTSUBMIT     : '/checkout/submit',
    CHECKOUTCANCEL     : '/checkout/cancel',
    FORMERROR          : '/forms/error'

};

var Dispatcher = (function(){
    function Dispatcher(){
        this.publishers         = [];
        this.subscribers        = [];
        this.topics             = new Set();
        /**
         * topics regroups all subscribers to a 
         * particule
         */
        this.topic_pool         = {};
        this.topic_ref          = -1;
    };

    /**
     * 
     * @param {*} topic 
     * @param {*} publisher 
     */
    Dispatcher.prototype.add_publisher = function(topic, publisher){
        this.publishers.push(publisher);
        if(!this.topic_pool.hasOwnProperty(topic)){
            this.topic_pool[topic] = [];
        }

    };
    Dispatcher.prototype.add_subscriber = function(subscriber){
        this.subscribers.push(subscriber);
    };

    /**
     * return a unique Token used to unsubscribe from topic
     * @param {*} topic (string): The topic to subscribe to
     * @param {*} listener(Function): The callback function to call when  a topic changed
     */
    Dispatcher.prototype.register_subscriber = function(topic, listener){
        if(!this.topic_pool.hasOwnProperty(topic)){
            this.topic_pool[topic] = [];
        }
        var token = (++this.topic_ref).toString();
        this.topic_pool[topic].push({callback:listener, token: token});
        return token;
    };

    /**
     * Unsubscribe a a listener from a topic
     * @param {*} token(string) : The token of the listener to unsubscribe
     */
    Dispatcher.prototype.unsubscribe = function(token){
        for(var topic in this.topic_pool){
            if(this.topic_pool.hasOwnProperty(topic)){
                for(var i = 0, j = this.topic_pool[topic].length; i < j; i++){
                    if(this.topic_pool[topic][i].token === token){
                        this.topic_pool[topic].splice(i, 1);
                        return token;
                    }
                }
            }
        }
        return false;
    };

    Dispatcher.prototype.notify = function(data){
        if(data){
            this.subscribers.forEach(function(subscriber){
                if(subscriber.get_topics().has(data.topic)){
                    subscriber.update(data);
                }
            });
        }
    };


    Dispatcher.prototype.publish = function(topic, data){
        //console.log("Dispatcher publish() : this ref :");
        //console.log(this);
        //console.log("Dispatcher publish() : this ref END");
        console.log("publishing to topic : " + topic);
        if(!this.topic_pool.hasOwnProperty(topic)){
            //console.log("New data publish for an undefined topic " + topic);
            //console.log("Published Data : " );
            //console.log(data);
            return false;
        }
        var subscribers = this.topic_pool[topic];
        for(var i = 0, j = subscribers.length; i < j; i++){
            try {
                subscribers[i].callback(topic, data);
            } catch (error) {
                throw error;
            }
        }
        //console.log("Dispatcher Publish() : ");
        //console.log(data);
        //console.log("Dispatcher publish() end");
        return true;
    };
    Dispatcher.prototype.get_topics = function(){
        return this.topics;
    };

    Dispatcher.prototype.contains_topic = function(topic){
        var flag = false;
        if(typeof topic === "number"){
            flag = this.topics.has(topic);
        }

        return flag;
    };

    Dispatcher.prototype.remove_topic = function(topic){
       this.topics.delete(topic);
    };

    Dispatcher.prototype.add_topic = function(topic){
        this.topics.add(topic);
    };
    return Dispatcher;
})();


var Publisher = (function(){
    function Publisher(){
        this.id = generate_id();
        this.topic = -1;
        this.dispatchers = [];

    };
    Publisher.prototype.set_topic = function(topic){
        this.topic = topic;
    };

    Publisher.prototype.get_topic = function(){
        return this.topic;
    };

    Publisher.prototype.register = function(dispatcher){
        this.dispatchers.push(dispatcher);
        dispatcher.add_publisher(this);
        console.log("Dispatcher registered on Publisher " + this.id + " ");

    };

    Publisher.prototype.deregister = function(dispatcher){
        //this.dispatchers.pop()
    };

    Publisher.prototype.publish = function(data){
        console.log("Publisher " + this.id + " published new data");
        if (data){
            data.topic = this.topic;
            this.dispatchers.forEach(function(dispatcher){
                dispatcher.notify(data);
            })
        }
    };

    return Publisher;
})();

var Subscriber = (function(){
    function Subscriber(){
        this.topics         = new Set();
        this.dispatchers    = [];
        this.id             = generate_id();
        this.listeners      = [];
    };
    Subscriber.prototype.set_callback = function(callback){
        this.callback = callback;
        this.listeners.push(callback);
    }

    Subscriber.prototype.add_listener = function(callback){
        this.listeners.push(callback)
    };

    Subscriber.prototype.get_topics = function(){
        return this.topics;
    };

    Subscriber.prototype.register = function(dispatcher){
        dispatcher.add_subscriber(this);
        this.dispatchers.push(dispatcher);
        console.log("Dispatcher registered on Subscriber " + this.id);
    };

    Subscriber.prototype.deregister = function(dispatcher){
        console.log("This method deregister(...) is not implemented yet")
    };

    Subscriber.prototype.register_to_topic = function(topic){
        this.topics.add(topic);
    };

    Subscriber.prototype.deregister_from_topic = function(topic){
        //this.topics.pop();
        if(this.topics.has(topic))
            this.topics.delete(topic);
    };

    Subscriber.prototype.update = function(data){
        if(data && data.hasOwnProperty( "topic" )){
            if(this.callback){
                this.callback(data);
            }
            else{
                console.log("Subscriber " +  this.id +  " received new Data : " + data.content +
                            " from topic " + data.topic + " .");
            }
        }

        
    };

    return Subscriber;
})();

/* END OF PUBLISHER - SUBSCRIBER MODULES */






var Collapsible = (function(){
    function Collapsible(){
        this.$collapsible   = {}; // all element with collapsible class
        this.$close         = {}; // all button used to close a collapsible elements.
        this.container      = {};
    }
    Collapsible.prototype.init = function(){
        console.log("Initializing Collapsible ...")
        this.$collapsible = $(".collapsible");
        this.container = $("#accordion-container");

        this.$close = this.$collapsible.children(".close");
        console.log("Found " + this.$collapsible.length + " collapsibles on this pages.");
        console.log("Found " + this.$close.length + " collapsibles closes on this pages.");
        this.$collapsible.children(".open").click(function(event){
            event.stopPropagation();
            var target =$(event.target).data("target");
            if(target == undefined){
                $(this).parent().children("ul").toggle();
            }
            else{
                $(target).toggle();
                console.log("Target : " + target);
            }
            
            
        });
        this.$close.click(function(event){
            console.log("collapsible closing ...");
            event.stopPropagation();
            var target =$(event.target).data("target");
            $(target).toggle();
        });
        var coll = $(".collapsible");
        coll.children(".header").click(this.onClick);

        
        $(".js-create").click(this.create.bind(this));
    };
    Collapsible.prototype.create = function(event){
            event.stopPropagation();
            
            var coll = $("<div>").addClass("collapsible").addClass("bordered").appendTo(this.container);
            var header = $("<div>").addClass("header").html("New HEADER").appendTo(coll);
            var content = $("<div>").addClass("content").html("NEW CONTENT").appendTo(coll);
            header.click(this.onClick);
    };
    Collapsible.prototype.onClick = function(event){
            var current = $(this);
            var was_visible = false;
            event.stopPropagation();
            var accordion = current.parent().parent();
            if(accordion.hasClass("accordion")){
                was_visible = !(current.siblings(".content").css('display') == "none");
                console.log("was visible : " + was_visible );
                accordion.children(".collapsible").children(".content").hide();
                if(!was_visible){
                    current.siblings(".content").show();
                }
            }
            else{
                current.siblings(".content").toggle();
            }
    };

    return Collapsible;
})();

var Modal = (function(){
    function Modal(){
        this.$modal         = {};
        this.$accountModal  = {};
        this.$cartModal     = {};
        this.$wishlistModal = {};
        this.$editModal     = {};
        this.$checkoutModal = {};
        this.$filterModal   = {};
        this.$sortOrderModal= {};
        this.$openModal     = {};
        this.$closeModal    = {};

    };

    Modal.prototype.init = function(){
        console.log("Modal plugin initialization ...");
        this.$accountModal  = $("#account-modal");
        this.$cartModal     = $("#cart-modal");
        this.$wishlistModal = $("#wishlist-modal");
        this.$editModal     = $(".edit-modal");
        this.$checkoutModal = $("#checkout-modal");
        this.$filterModal   = $("#filter-modal");
        this.$sortOrderModal= $("#sortOrder-modal");
        this.$openModal     = $(".flat-open-modal");
        this.$closeModal    = $(".flat-close-modal");
        
        that = this;
        this.$openModal.click(function(event){
            event.stopPropagation();
            that.$modal = $($(this).data('target'));
            that.$modal.show();
            
        });
        $(window).click(function(event){
            var $target = $(event.target);
            console.log("window click event fired ...");
            console.log("modal : ");
            console.log(that.$modal);
            console.log("event target : ");
            console.log($target);
            if($target.is(that.$modal)){
                console.log("modal clicked");
                that.$modal.hide();
            }
            
        });
        this.$closeModal.click(function(event){
            //that.$modal = $($(this).data('target'));
            that.$modal.toggle();
        });
        
        console.log("Modal plugin installed ...");
    };


    return Modal;
})();

var Tabs = (function(){
    function Tabs(){
        this.currentTab     = 0;
        this.tabCount       = 0;
        this.tabs           = {};
        this.tab            = {};
        this.tabsCount      = 0;
        
    };

    Tabs.prototype.init = function(){
        this.tabsCount = $(".flat-tabs").length;
        this.tabs = $(".flat-tabcontent");
        this.tab = $(".flat-tab");
        this.tabCount = this.tab.length;
        this.tab.click(this.onTabClicked.bind(this));
        this.tabs.hide();
        this.update();
        console.log("Tabs suceesfully initialized :");
        console.log(" Tabs found " + this.tabCount + " on this page");
        console.log("there are " + this.tabsCount + " tabs on this page");
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

var Cart = (function(){
    function Cart(){

        this.events                     = [];
        this.items                      = [];
        this.eventListeners             = [];
        this.total                      = 0;
        this.count                      = 0;
        this.userID                     = -1;
        this.observers                  = [];
        this.serverUrl                  = "";
        this.$counter                   = {};
        this.$add_to_cart_btn           = {};
        this.catalog                    = {};
        this.$add_to_wishlist_btn       = {};
        this.$checkout_link             = {};
        this.$summary                   = {};
        this.dispatcher                 = {};
    }
    Cart.prototype.init = function(){
        this.$summary = $("#js-cart-summary");
        //this.$add_to_wishlist_btn = $(".js-cart-add-to-wishlist");
        //this.$add_to_wishlist_btn.click(this.onAddToWishlistClicked.bind(this));
         this.$checkout_link = $(".flat-checkout-link");
         this.$counter = $(".cart-counter");
        //this.$add_to_cart_btn = $("#flat-add-to-cart-btn");
        //this.$add_to_cart_btn.click(this.onAddButtonClicked.bind(this));
        //$("#js-add-to-cart").click(this.onAddButtonClicked.bind(this));
        //$(".js-cart-item-up").click(this.onPlusButtonClicked.bind(this));
        //$(".js-cart-item-down").click(this.onMinusButtonClicked.bind(this));
        //$(".js-cart-remove").click(this.onRemoveButtonClicked.bind(this));

    };
    Cart.prototype.set_dispatcher = function(dispatcher){
        this.dispatcher = dispatcher;
        var token = dispatcher.register_subscriber(PUBSUBTOPIC['CARTADDITEM'], this.addItem.bind(this));
        dispatcher.register_subscriber(PUBSUBTOPIC['CARTADDITEMFAILED'], this.onAddItemFailed.bind(this));
        dispatcher.register_subscriber(PUBSUBTOPIC['CARTREMOVEITEM'], this.removeItem.bind(this));
        dispatcher.register_subscriber(PUBSUBTOPIC['CARTREMOVEITEMFAILED'], this.onRemoveItemFailed.bind(this));
        dispatcher.register_subscriber(PUBSUBTOPIC['CARTCLEAR'], this.clear.bind(this));
        dispatcher.register_subscriber(PUBSUBTOPIC['CARTUPDATE'], this.update.bind(this));

    }
    Cart.prototype.addCatalog = function(catalog){
        this.catalog = catalog;
        this.catalog.setCart(this);
    }
    Cart.prototype.onCloseBtnClicked = function(even){
        event.stopPropagation();
        console.log("Close Menu btn clicked ...");
        $(".cart-dropdown").toggle();
    };
    Cart.prototype.onCartButtonHover = function(event){
        event.stopPropagation();
        console.log("Cart hovered ..");
        event.preventDefault();
        //$(".cart-button").dropdown();
    };
    Cart.prototype.onCartButtonHoverLeave = function(event){
        event.stopPropagation();
        console.log("Cart hovered left..");
        event.preventDefault();
        console.log("Cart contains " + this.count + " article(s)");
        //$(".cart-button").dropdown();
    };
    Cart.prototype.onAddToWishlistClicked = function(event){
        event.stopPropagation();
        console.log("Cart : moving item to Wishlist");
        var item = {};
        var $target = $($(event.target).data('target'));
        item.id = $target.data("product-id");
        if(isNaN(item.id)){
            console.log("Item ID is NaN");
            this.catalog.notify({message: "ID non identifié. Si le problème persiste veuillez nous contatcter. "});
        }
        else{
            this.catalog.addToWishlist(item);
        }
        
    }
    Cart.prototype.onAddButtonClicked = function(event){
        event.stopPropagation();
        var item = {};
        var $target = $($(event.target).data("target"));
        item.id = parseInt($target.data("product-id"));
        item.is_available = $target.data("available");
        item.quantity = 1;
        //this.addItem(item);
        this.dispatcher.publish(PUBSUBTOPIC['CARTADDITEM'], item);
    };
    Cart.prototype.onRemoveButtonClicked = function(event){
        event.stopPropagation();
        var $target = $($(event.target).data("target"));
        var itemID = parseInt($target.data("product-id"));
        var that = this;
        console.log("Cart Remove : ID = " + itemID);
        $.ajax({
            type: 'POST',
            url: '/cart/cart_update/',
            data: {product_id: itemID, quantity : 0},
            dataType:'json',
            success: function(response){
                that.total = response.total;
                that.count = response.count;
                $target.remove();
                that.notify({});
                that.catalog.notify({message: "L'article a été retiré du Panier"});
            },
            error: function(response){
                that.catalog.notify({message: "L'article n'a pas pû être retiré du Panier"});
                console.log("Error : couldn't remove the  article");
            }
        });
    };
    Cart.prototype.onPlusButtonClicked = function(event){
        event.stopPropagation();
        console.log("PlusButton Clicked ...  : ");
        this.update(event, true);
    };
    Cart.prototype.onMinusButtonClicked = function(event){
        event.stopPropagation();
        console.log("MinusButton Clicked ...");
        this.update(event, false);
    };
    Cart.prototype.addObserver = function(observer){
        console.log("Adding Observer ...");
        this.observers.push(observer);
    };
    Cart.prototype.removeObserver = function(observer){
        console.log("Removing Observer ...");
        for(var i = 0; i < this.observers.length; i++){
            if(this.observers[i] === observer){
                this.observers.slice(i, i+1);
                break;
            }
        }
    };
    Cart.prototype.notify = function(item){
        console.log("Notifying Observers ...");
        $(".cart-subtotal").html(this.total);
        this.$counter.html(this.count);
        if(this.count == 0){
            this.$checkout_link.hide();
            this.$summary.hide();
        }
        else{
            this.$checkout_link.show();
            this.$summary.show();
        }
        this.badgeUpdate();
    };


    Cart.prototype.onAddItemSucess = function(response){
        this.total = response.total;
        this.count = response.count;
        //this.notify({});
        //this.catalog.notify({message: "L'article a été ajouté dans le Panier"});
        //this.dispatcher.publish(PUBSUBTOPIC['CARTADDITEMSUCCESS'], {message: "L'article a été ajouté dans le Panier", total: response.total, count: response.count});
    };

    Cart.prototype.onAddItemFailed = function(response){
        //this.catalog.notify({message: "L'article n'a pas pu être ajouté dans le Panier"});
        //this.dispatcher.publish(PUBSUBTOPIC['CARTADDITEMFAILED'], {message: "L'article n'a pas pu être ajouté dans le Panier."});
    };

    Cart.prototype.onRemoveItemFailed = function(e){

    };

    Cart.prototype.onRemoveItemSuccess = function(e){

    };

    Cart.prototype.addItem = function(topic, item){
        //console.log("Cart addItem() this ref : ");
        //console.log(this);
        //console.log("Cart addItem() this ref END ");
        // Send request to the Server 
        //console.log("Cart Additem new Item : ");
        //console.log(item);
        if(item.is_available == "True"){

            var settings = {
                            type: 'POST',
                            url : '/cart/add_to_cart/',
                            data: {product_id: item.id, quantity: item.quantity},
                            dataType: 'json'
                        };
            var future = ajax(settings).then(this.onAddItemSucess, this.onAddItemFailed);
        }
       
        else{
            this.dispatcher.publish(PUBSUBTOPIC['CARTADDITEMFAILED'], {message: "Cet article n'est plus disponible."});
            //that.catalog.notify({message: "Cet article n'est plus disponible."});
            
            //console.log("This article is not available ...");
        }
        
    };

    Cart.prototype.react = function(topic, item){
       
        //console.log("Cart received new data from topic : " + topic);
        //console.log("Cart React() new data : ");
       // console.log(item);
        this.dispatcher.publish(PUBSUBTOPIC['CARTADDITEMFAILED'], {message: "CARD ADD ITEM FAILDE !"});
        // Send request to the Server 
        /*
        if(item.is_available == "True"){

            var settings = {
                            type: 'POST',
                            url : '/cart/add_to_cart/',
                            data: {product_id: item.id, quantity: item.quantity},
                            dataType: 'json'
                        };
            var future = ajax(settings).then(this.onAddItemSucess.bind(this), this.onAddItemFailed.bind(this));
        }
       
        else{
            that.catalog.notify({message: "Cet article n'est plus disponible."});
            console.log("This article is not available ...");
        }
        */
        
    };
    Cart.prototype.removeItem = function(itemID){
        // Send request to the Server here 
        var index = this.items.findIndex(function(item){
            return item.id === itemID;
        });
        if(index >= 0){
            this.items.slice(index, index);
            this.total -= item.price * item.quantity;
            this.count -= item.quantity;
            this.notify(item);
        }
        
    };
    Cart.prototype.addEventListener = function(event){
        console.log("Adding Event  ... : " +  event.html() );
        this.eventListeners.push(event);
    };
    Cart.prototype.getCount = function(){
        return this.count;
    };
    Cart.prototype.getTotal = function(){
        
        return this.total;
    };

    Cart.prototype.getItem = function(index){
        if(index >= 0 && index < this.count)
            return this.items[index];
        else 
        return {id : -1};
    };

    Cart.prototype.clear = function(){
        while(this.items.length){
            this.items.pop();
        }
        while(this.eventss.length){
            this.events.pop();
        }
        while(this.observers.length){
            this.observers.pop();
        }
        while(this.eventListeners.length){
            this.eventListeners.pop();
        }
        this.total = 0.0;
        this.count = 0;
    };

    Cart.prototype.update = function(topic, data){
         var notification = {};
        var settings = {
            type: 'POST',
            url: '/cart/cart_update/',
            data: {product_id: data.id, quantity : data.requested_qty},
            dataType:'json'
        };
        var success = function(response){
            console.log("Cart Update Succes :");
            console.log(this);
            this.total = response.total;
            this.count = response.count;
            console.log("Cart Success Data :");
            console.log(data);
            console.log("quantity updated: " );
            console.log(response.updated);
            console.log("quantity : " + response.quantity);
            console.log(response);
            console.log("Log end Cart");
            if(response.updated){
               
               if(response.quantity > 0){
                   
                data.qty_target.html(response.quantity);
                data.target.data("quantity", response.quantity);
                data.subtotal.html(this.total);
                
               }
               else{
                data.target.remove();
               }
               notification.message= "Le Panier a été actualisé";
            }
            else{
                if(response.quantity_error){
                    notification.message= "Vous avez atteint la quantité maximale pour cet article";
                }
                else{
                    notification.message= "Il a eu une erreur interne. veuillez reéssayer plus tard";
                }
            }
           
            this.notify({});
            //that.catalog.notify(notification);

            this.dispatcher.publish(PUBSUBTOPIC['CARTUPDATESUCCESS'], notification);
            
        };
        var future = ajax(settings);
        future.then(success.bind(this), function(response){
            console.log("Cart Update Succes :");
            console.log(this);
            this.disptacher( PUBSUBTOPIC['CARTUPDATEFAILED'], {message: "Le Panier n'a pas pu être actualisé"});
            console.log("Error : l'article n'a pas pu etre actualiser");
        });
    };

    Cart.prototype.badgeUpdate = function(){
        console.log("Cart.badgeUpdate() not implemented yet ...");
    };
    
    return Cart;
})();

var Account = (function(){
    function Account (){
        this.username = "";
        this.email = "";
        this.address1 = "";
        this.address2 = "";
        this.loginState = false;
        this.wishlist = "";
        this.orders = "";


    }

    Account.prototype.init = function(){
        $(".account-Button").click(this.onAccountClicked.bind(this));
        $(".account-Button").hover(this.onAccountHover.bind(this));
        console.log("Account initialized ...");
    };
    Account.prototype.onAccountHover = function(event){
        console.log("AccountButton hovered ...");
        //$(".dropdown-toggle").dropdown();
    };
    Account.prototype.onAccountClicked = function(event){
        console.log("AccountButton clicked ...");
        $(".dropdown-toggle").dropdown();
    };

    return Account ;
})();



var Catalog = (function(){
    function Catalog(){
        this.sortOrder          = 1;
        this.CURRENT_SORTING    = 0;
        this.SORTING_PRICE_ASC  = 0;
        this.SORTING_PRICE_DSC  = 1;
        this.SORTING_POPULARITY = 2;
        this.SORTING_RANDOM     = 3;
        this.SORTING_RECENT     = 4;
        this.ordering           = [];
        this.viewedItems        = [];
        this.$items             = {};
        this.$select_filter     = {};
        this.$select_brands     = {};
        this.brands             = [];
        this.brand_filter       = [];
        this.account_menu_popup_is_visible = false;
        this.$category_btn      = {};
        this.$filter_btn        = {};
        this.$clickable         = {};
        this.$close_flat_main   = {};
        this.$brand_input       = {};
        this.$sorting_radios    = {};
        this.$product_list      = {};
        this.$brand_list        = {};
        this.$add_to_cart_btn   = {};
        this.$add_to_wishlist_btn = {};
        this.cart               = {};
        this.wishlist           = {};
        this.$canvamenu          = {};
        this.$site_wrapper      = {};
        this.$canva_menu_btn    = {};
        this.$canva_container   = {};
        this.$notification      = {};
        this.$notification_content = {};
        this.timeoutID          = -1;
        this.dispatcher         = {};
        this.cart_add_btn       = {};
        this.cart_remove_btn    = {};
        this.wl_add_btn         = {};
        this.wl_remove_btn      = {};
        this.wl_clear_btn       = {};
        this.wl_counter         = {};
        this.wl_add_to_cart_btn = {};
        this.show_filter        = {};
        this.hide_filter        = {};
        this.page_side          = {};

    }
    Catalog.prototype.init = function(sorting){
        var that = this;
        this.ordering[0]                         = "NO ACTIV SORTING ";
        this.ordering[this.SORTING_PRICE_ASC]     = "ASCENDING SORTING";
        this.ordering[this.SORTING_PRICE_DSC]     = "DESCENDING SORTING";
        this.ordering[this.SORTING_POPULARITY]    = "POPULARITY SORTING";
        this.ordering[this.SORTING_RANDOM]        = "RANDOM SORTING";
        if((sorting >= 0) && (sorting <= this.SORTING_RANDOM)){
            this.CURRENT_SORTING = sorting;
            this.filter();
        }
        this.$notification = $("#notification");
        this.$notification_content = this.$notification.children(".content");
        this.$canva_menu_btn = $("#js-canva-menu");
        this.$canvamenu = $("#site-canva-menu");
        this.$canva_container = this.$canvamenu.children(".canva-container");
        this.$site_wrapper= $("#site-wrapper");
        this.$sorting_radios = $("#flat-sorting-input span input:radio");
        this.$product_list = $("#flat-product-list");
        this.$items = $("#flat-product-list .flat-product");
        this.brands = $("#flat-brands span");
        this.$brand_list = $("#flat-brands span input:checkbox");
        this.$brand_input = $("#brands-filter-input");
        this.$brand_input.keyup(this.onBrandInputChanged.bind(this));
        this.$clickable = $(".flat-clickable");
        this.$close_flat_main = $(".flat-close-main");

        //this.$add_to_cart_btn = $("#flat-add-to-cart-btn");
        //this.$add_to_cart_btn.click(this.onCartAddBtnClicked.bind(this));
        $("#js-add-to-cart").click(this.onCartAddBtnClicked.bind(this));
        $(".js-cart-item-up").click(this.onCartPlusBtnClicked.bind(this));
        $(".js-cart-item-down").click(this.onCartMinusBtnClicked.bind(this));
        $(".js-cart-remove").click(this.onCartRemoveBtnClicked.bind(this));
        this.show_filter = $(".js-show-filter");
        this.hide_filter = $(".js-hide-filter");
        this.page_side   = $(".js-page-side");
        this.$wl_clear_btn = $(".js-wishlist-clear");
        this.$wlbagde = $(".wishlist-badge");
        this.$wl_counter = $(".js-wishlist-counter");
        this.$wl_add_to_cart_btn = $(".js-move-to-cart");
        this.$wl_add_to_cart_btn.click(this.onWLAddToCartClicked.bind(this));
        $("#js-add-to-wishlist").click(this.onWLAddBtnClicked.bind(this));
        $("#flat-add-to-wishlist-btn").click(this.onWLAddBtnClicked.bind(this));
        $(".js-remove-from-wishlist").click(this.onWLRemoveBtnClicked.bind(this));
        this.$wl_clear_btn.click(this.onWLClearBtnClicked.bind(this));

        $(".flat-hoverable").hover(function(event){
            event.stopPropagation();
            $(this).children(".flat-product-options").toggle();
            console.log("flat-product hovered");
        });
        this.show_filter.click(function(event){
            that.show_filter.toggle();
            that.hide_filter.toggle();
            console.log("page side left : " + that.page_side.css("width"));
            that.page_side.show();
            console.log("Show Filter clicked");
            
        });
        this.hide_filter.click(function(event){
            that.hide_filter.toggle();
            that.show_filter.toggle();
            console.log("page side left : " + that.page_side.css("width"));
            that.page_side.hide();

            console.log("Hide Filter clicked");
        });
        this.$clickable.click(function(event){
            event.stopPropagation();
            console.log("Clickable clicked ...");
            $(this).siblings(".flat-main-content").toggle();
        });
        this.$close_flat_main.click(function(event){
            event.stopPropagation();
            $(this).parents(".flat-main-content").hide();
        });
        this.$category_btn = $(".flat-cat-close");
        this.$filter_btn = $(".flat-filter-close");
        
        // Dropdown Account Menu 
        $(".flat-account-dropdown-btn").click(function(event){
            event.stopPropagation();
            console.log("Account icon clicked ...");
            $(".flat-account-drop-wrapper").toggle();
            console.log($(event.target));
        });
        $(".flat-cancel-btn").click(function(event){
            event.stopPropagation();
            $( ".flat-account-drop-wrapper, .flat-dropdown-wrapper").
            each(function(index, element){
                if($(element).css("display") !== "none"){
                    $(element).hide();
                }
            });
        });
        /**
         * Controls click event emitted from the Flat Account Menu
         * contained in a flat-account-drop-wrapper or flat-dropdown-wrapper
         */
        $(".flat-dropdown-btn").click(function(event){
            event.stopPropagation();
            console.log("drop clicked ");
            $(this).siblings(".flat-dropdown-wrapper").toggle();
        });
        
        /**
         * Controls click on the flat nav menu.
         * This element contains the side site menu
         */
        $(".flat-nav-menu").click(function(event){
            event.stopPropagation();
            $("#flat-site-menu").toggle();
            console.log("menu clicked ...")
        });
        $(".flat-btn-menu-close").click(function(event){
            event.stopPropagation();
            $("#flat-site-menu").hide();
            console.log("menu clicked ...")
        });
        $(".js-notify-close").click(function(event){
            event.stopPropagation();
            console.log("closing notification...");
            if(that.timeoutID > 0){
                console.log("A timer is active : timer ID = " + that.timeoutID);
                clearTimeout(that.timeoutID);
                that.timeoutID = -1;
            }
            that.$notification.hide();

        });
        this.getItems();
        $("#flat-filter-apply").click(this.onFilterChanged.bind(this));
        $("#btn-filter-reset").click(this.onFilterReset.bind(this));
        $("#flat-sort-apply").click(this.onSortingChanged.bind(this));
        $("#btn-sort-reset").click(this.onSortingReset.bind(this));
        this.$select_filter = $("#select-filter");
        this.$select_brands = $("#select-brands");
        for(var i = 0; i < this.brands.length; i++){
            this.$select_brands.append(`<input  type="checkbox" value=${i}> <span class="brand-entry"> ${this.brands[i]} </span>`); 
        }

        /**
         * OFF-CANVA-MENU
         */
         $("#js-canva-menu").click(function(event){
             console.log("click on canva button");
            var left = that.$canvamenu.css("left");
            console.log("click on canva button");
            console.log("canva menu  LEFT Property : " +  left);
            if (left == "0px"){
                that.$canvamenu.css("left", "-400px");
                that.$site_wrapper.css("margin-left", "0");
            }
            else if (left == "-400px"){
                that.$canvamenu.css("left", "0");
                that.$site_wrapper.css("margin-left", "400px");
            }
         });

         $(".js-close-canva").click(function(event){
            var target = $($(".js-close-canva").data("target"));
            target.css("left", "-400px");
            that.$site_wrapper.css("margin-left", "0");
            $(".collapsible ul").hide();
         });
         $(".mask").hide();

         $("li .reveal").click(function(event){
             event.stopPropagation();
             $(event.target).toggle();
             $(event.target).siblings(".mask").toggle().siblings(".submenu").toggle();
             console.log(event.target);
         });

         $("li .mask").click(function(event){
            event.stopPropagation();
            $(event.target).toggle();
            $(event.target).siblings(".reveal").toggle().siblings(".submenu").toggle();
            console.log(event.target);
        });
         

    };

    Catalog.prototype.onCartAddBtnClicked = function(event){
        event.stopPropagation();
        var item = {};
        var $target = $($(event.target).data("target"));
        item.id = parseInt($target.data("product-id"));
        item.is_available = $target.data("available");
        item.quantity = 1;
        console.log("Catalog publshing CARTADDITEM");
        this.dispatcher.publish(PUBSUBTOPIC['CARTADDITEM'], item);

    };
    Catalog.prototype.onCartPlusBtnClicked = function(event){
        event.stopPropagation();
        console.log("PlusButton Clicked ...  : ");
        //this.update(event, true);
        var $target = $($(event.target).data("target"));
        var $qty_target = $(event.target).siblings(".product-quantity");
        var itemID = parseInt($target.data("product-id"));
        var price = parseFloat($target.data("price"));
        var quantity = parseInt($target.data("quantity"));
        
        var $subtotal = $target.find(".product-price-total");
        var requested_qty = quantity + 1 ;
        this.dispatcher.publish(PUBSUBTOPIC['CARTUPDATE'], 
                                {
                                    id:itemID, quantity:quantity, 
                                    requested_qty:requested_qty,
                                    target: $target,
                                    qty_target: $qty_target,
                                    subtotal : $subtotal
                                });
        
    };
    Catalog.prototype.onCartMinusBtnClicked = function(event){
        event.stopPropagation();
        console.log("MinusButton Clicked ...");
        //this.update(event, false);
        var $target = $($(event.target).data("target"));
        var $qty_target = $(event.target).siblings(".product-quantity");
        var itemID = parseInt($target.data("product-id"));
        var price = parseFloat($target.data("price"));
        var quantity = parseInt($target.data("quantity"));
        
        var $subtotal = $target.find(".product-price-total");
        var requested_qty = quantity - 1 ;
        this.dispatcher.publish(PUBSUBTOPIC['CARTUPDATE'], 
                                {
                                    id:itemID, quantity:quantity, 
                                    requested_qty:requested_qty,
                                    target: $target,
                                    qty_target: $qty_target,
                                    subtotal : $subtotal
                                });
    };

    Catalog.prototype.onCartRemoveBtnClicked = function(event){
        event.stopPropagation();
    };

    // WISHLIST reactors:
    Catalog.prototype.onWLAddBtnClicked = function(event){
        event.stopPropagation();
        console.log("Add to wishlist : " );
        
        var item = {};
        var $target = $($(event.target).data("target"));
        console.log($target);
        item.id = parseInt($target.data("product-id"));
        
        if(!isNaN(item.id)){
            this.dispatcher.publish(PUBSUBTOPIC['CARTADDITEM'], item);
        }
        else{
            console.log("Item has an invalid ID : " + item.id);
        }
        
    };

    Catalog.prototype.onCartAddItemFailed = function(topic, data){
        this.notify(topic, data);
    };

    Catalog.prototype.onCartRemoveItemFailed = function(topic, data){
        this.notify(topic, data);
    };
    Catalog.prototype.onWLAddToCartClicked = function(event){
        event.stopPropagation();
    };

    Catalog.prototype.onWLRemoveBtnClicked = function(event){
        event.stopPropagation();
        var item = {};
        var target_id = $(event.target).data("target");
        this.$to_remove = $(target_id);
        console.log("Removing WI : " +  target_id);
        item.id = parseInt(this.$to_remove.data("itemid"));
        this.dispatcher.publish(PUBSUBTOPIC['WISHLISTREMOVE'], item);
        //var result = this.removeItem(item.id);
        //result.then(this.onRemoveItemSuccess.bind(this),
        //this.onRemoveItemFailed.bind(this));
        
    };
    Catalog.prototype.onWLClearBtnClicked = function(event){
        event.stopPropagation();
        //this.clear();
        this.dispatcher.publish(PUBSUBTOPIC['WISHLISTCLEAR'], {});
    };

    Catalog.prototype.set_dispatcher = function(dispatcher){
        this.dispatcher = dispatcher;
        var token = dispatcher.register_subscriber(PUBSUBTOPIC['CARTADDITEMSUCCESS'], this.notify.bind(this));
        dispatcher.register_subscriber(PUBSUBTOPIC['CARTADDITEMFAILED'], this.onCartAddItemFailed.bind(this));
        dispatcher.register_subscriber(PUBSUBTOPIC['CARTREMOVEITEMFAILED'], this.onCartRemoveItemFailed.bind(this));
        dispatcher.register_subscriber(PUBSUBTOPIC['SORTINGHIGHERPRICE'], this.onSortingChanged.bind(this));
        dispatcher.register_subscriber(PUBSUBTOPIC['SORTINGLOWERPRICE'], this.onSortingChanged.bind(this));
        dispatcher.register_subscriber(PUBSUBTOPIC['FILTERBRAND'], this.filter.bind(this));
        dispatcher.register_subscriber(PUBSUBTOPIC['CARTUPDATESUCCESS'], this.notify.bind(this));
        dispatcher.register_subscriber(PUBSUBTOPIC['CARTUPDATEFAILED'], this.notify.bind(this));

    };
    Catalog.prototype.setCart = function(cart){
        console.log("Catalog adding Cart instance ");
        this.cart = cart;
    };
    Catalog.prototype.setWishlist = function(wishlist){
        console.log("Catalog adding Wishlist instance ");
        this.wishlist = wishlist;
    };


    Catalog.prototype.addToCart = function(item){
        //this.cart.addItem(item);
        console.log("Catalog publishing to CARTADDITEM");
        console.log(item);
        console.log("Catalog puslishing to CARTADDITEm end");
        this.dispatcher.publish(PUBSUBTOPIC['CARTADDITEM'], item);
    };
    Catalog.prototype.addToWishlist = function(item){
        this.wishlist.addItem(item);
    }

    Catalog.prototype.onBrandInputChanged = function(event){
        var val = this.$brand_input.val().toLowerCase();
        this.brands.filter(function(i, e){
            $(e).toggle($(e).text().toLowerCase().indexOf(val) > -1)
        });
        console.log("Brands input changed ...");
    };
    Catalog.prototype.onFilterChanged = function(event){
        //this.$select_filter.collapse("toggle");
        var $selected_brands = this.$brand_list.filter(":checked");
        console.log("Filter Selected : " );
        console.log($selected_brands);
        that = this;
        var sel = {};
        var element = {};
        var match = false;
        if($selected_brands.length > 0){
            this.$items.each(function(i, e){
                element = $(e);
                $selected_brands.each(function(j,input){
                    sel = $(input).val();
                    console.log("Look for items to mask");
                    console.log("Brand : " + sel);
                    console.log("Item being checked " );
                    console.log(element);
                    console.log("Element Brand : " + element.data("brand"));
                    if(sel == $(e).data("brand")){
                        match = true;
                    }
                });
                if(match){
                    element.show();
                    match = false;
                }
                else{
                    element.hide();
                }
            });
        }
        else {
            this.$items.each(function(i, e){
                $(e).show();
            });
        } 
    };

    Catalog.prototype.onSortingChanged = function(event){
        event.stopPropagation();
        event.preventDefault();
        var order = this.$sorting_radios.filter(":checked").val();
        order = parseInt(order);
        console.log("Sorting changed to " + this.ordering[order]);
        this.sort(order);
        this.$product_list.empty();
        this.$items.appendTo(this.$product_list);

    };
    Catalog.prototype.onSortingReset = function(event){
        event.preventDefault();
        console.log("Sorting reset");
    };
    Catalog.prototype.onFilterReset = function(event){
        event.preventDefault();
        console.log("Reset pressed...");
        
        $('#select-brands input:checkbox').prop('checked', false);
        this.$items.show();

    };
    Catalog.prototype.filter = function(){
        console.log(" filter () : This method is not implemented yet ...");
        for(var i = 0; i < this.$items.length; i++){
            if(this.brand_filter.includes($(this.$items[i]).attr("data-brand"))){
                $(this.$items[i]).hide();
            }
            else{
                $(this.$items[i]).show();
            }
        }
        this.brand_filter_clear();
        
    };
    Catalog.prototype.brand_filter_clear = function(){
        while(this.brand_filter.length){
            this.brand_filter.pop();
        }
    };
    Catalog.prototype.sortByPrice = function(order){
        var key = "price";
        if(order == this.SORTING_PRICE_DSC){
            this.$items.sort(function(a, b){
                return $(b).data(key) - $(a).data(key);
            });
        }
        else if(order == this.SORTING_PRICE_ASC){
            this.$items.sort(function(a, b){
                return $(a).data(key) - $(b).data(key);
            });
        }
    };
    Catalog.prototype.sortByPopularity = function(key){
        this.$items.sort(function(a, b){
            return $(b).data(key) - $(a).data(key);
        });
    };
    Catalog.prototype.sort = function(sortType){
        console.log(" sort () : This method is not implemented yet ...");
        var key = "";
        switch (sortType) {
            case this.SORTING_PRICE_DSC:
            case this.SORTING_PRICE_ASC:
                this.sortByPrice(sortType);
                break;
            case this.SORTING_POPULARITY:
                this.sortByPopularity("viewcount");
                break;
            case this.SORTING_RANDOM:

                break;
            case this.SORTING_RECENT:

                break;
        
            default:
                break;
        }
    };
    Catalog.prototype.search = function(){
        console.log(" search () : This method is not implemented yet ...");
    };
    Catalog.prototype.onSearchInputChanged = function(query){
        console.log(" Searched Query : " + query);
    };
    Catalog.prototype.renderViewedItems = function(){
        console.log(" render () : This method is not implemented yet ...");
    };

    Catalog.prototype.getItems = function(){
        console.log(" getItems () : This method is not implemented yet ...");
        
        console.log(this.$items);
        console.log("We found " + this.$items.length + " in this page");

    };
    Catalog.prototype.getBrands = function (){
        console.log("getBrands() called ...");
    };

    Catalog.prototype.react = function(topic, notification){
        var that = this;
        if(notification.message != "undefined"){
            this.$notification_content.html(notification.message); 
        }
        else{
            console.log("Bad notification object");
            this.$notification_content.html("Erreur du format de notifition"); 
        }

        this.$notification.show("slow", function(){
            var element = this;
            that.timeoutID = setTimeout(function(){
                $(element).hide();
                //that.timeoutID = -1;
            }, 5000);
            console.log("timerID : " + that.timeoutID);
        });
    };

    Catalog.prototype.notify = function(topic, notification){
        var that = this;
        if(notification.message != "undefined"){
            this.$notification_content.html(notification.message); 
        }
        else{
            console.log("Bad notification object");
            this.$notification_content.html("Erreur du format de notifition"); 
        }

        this.$notification.show("slow", function(){
            var element = this;
            that.timeoutID = setTimeout(function(){
                $(element).hide();
                //that.timeoutID = -1;
            }, 5000);
            console.log("timerID : " + that.timeoutID);
        });
    };
    return Catalog;
})();
//var myCart = new Cart();

var Wishlist = (function(){
    function Wishlist(){
        this.items              = [];
        this.count              = 0;
        this.$bagde             = {};
        this.$counter           = {};
        this.catalog            = {};
        this.$add_to_cart_btn   = {};
        this.$clear_btn         = {};
        this.$to_remove         = {};
        this.dispatcher         = {};

    }
    Wishlist.prototype.init = function(){
        this.$clear_btn = $(".js-wishlist-clear");
        this.$bagde = $(".wishlist-badge");
        this.$counter = $(".js-wishlist-counter");
        this.$add_to_cart_btn = $(".js-move-to-cart");
        this.$add_to_cart_btn.click(this.onAddToCartClicked.bind(this));
        $("#js-add-to-wishlist").click(this.onAddButtonClicked.bind(this));
        $("#flat-add-to-wishlist-btn").click(this.onAddButtonClicked.bind(this));
        $(".js-remove-from-wishlist").click(this.onRemoveButtonClicked.bind(this));
        this.$clear_btn.click(this.onClearButtonClicked.bind(this));
    }
    Wishlist.prototype.set_dispatcher = function(dispatcher){
        this.dispatcher = dispatcher;
        dispatcher.register_subscriber(PUBSUBTOPIC['WISHLISTADD'], this.addItem.bind(this));
        dispatcher.register_subscriber(PUBSUBTOPIC['WISHLISTREMOVE'], this.removeItem.bind(this));
        dispatcher.register_subscriber(PUBSUBTOPIC['WISHLISTCLEAR'], this.clear.bind(this));
        //dispatcher.register_subscriber(PUBSUBTOPIC['WISHLISTADDTOCART'], this.add)

    }
    Wishlist.prototype.addCatalog = function(catalog){
        this.catalog = catalog;
        this.catalog.setWishlist(this);
    }

    Wishlist.prototype.onAddToCartClicked = function(event){
        event.stopPropagation();
        console.log("Wishlist : moving item to Cart");
        var item = {};
        var $target = $($(event.target).data("target"));
        item.id = parseInt($target.data("product-id"));
        item.is_available = $target.data("available");
        item.quantity = 1;
        //this.catalog.addToCart(item);
        this.dispatcher.publish(PUBSUBTOPIC['CARTADDITEM'], item);
    }
    Wishlist.prototype.onAddButtonClicked = function(event){
        event.stopPropagation();
        console.log("Add to wishlist : " );
        
        var item = {};
        var $target = $($(event.target).data("target"));
        console.log($target);
        item.id = parseInt($target.data("product-id"));
        
        if(!isNaN(item.id)){
            //this.addItem(item);
            this.dispatcher.publish(PUBSUBTOPIC['CARTADDITEM'], item);
        }
        else{
            console.log("Item has an invalid ID : " + item.id);
        }
        
    };
    Wishlist.prototype.onRemoveButtonClicked = function(event){
        event.stopPropagation();
        var item = {};
        var target_id = $(event.target).data("target");
        this.$to_remove = $(target_id);
        console.log("Removing WI : " +  target_id);
        item.id = parseInt(this.$to_remove.data("itemid"));
        this.dispatcher.publish(PUBSUBTOPIC['WISHLISTREMOVE'], item);
        //var result = this.removeItem(item.id);
        //result.then(this.onRemoveItemSuccess.bind(this),
        //this.onRemoveItemFailed.bind(this));
        
    };
    Wishlist.prototype.onClearButtonClicked = function(event){
        event.stopPropagation();
        this.clear();
        this.dispatcher.publish(PUBSUBTOPIC['WISHLISTCLEAR'], {});
    };

    Wishlist.prototype.onAddItemSucess = function(response){
            this.count =  response.item_count;
            notification.added = response.added;
            if(response.added){
                notification.message = "L'article a été ajouté à vos Favoris";
            }
            else{
                if (response.duplicated){
                    notification.message = "Cet article est déjà dans vos Favoris";
                }
            }
            console.log("Wishlist : " + notification.message);
            this.notify(notification);
    };

    Wishlist.prototype.onAddItemFailed = function(error){
            notification.added = false;
            notification.message = "L'article n'a pas pu être ajouté à vos Favoris";
            console.log("Error : couldn't add item into the wishlist");
            this.notify(notification);
    };

    Wishlist.prototype.onClearSuccess = function(response){
        this.count =  response.item_count;
        $("#wishlist .content").children().remove();
        this.notify({message: "La liste des Favoris a été vidée"});
    };

    Wishlist.prototype.onClearFailed = function(error){
        that.notify({message: "Erreur : La Liste des Favoris n'a pas pu être vidée"});
        console.log("Error : couldn't clear the wishlist");
    };

    Wishlist.prototype.onRemoveItemSuccess = function(response){
        this.dispatcher.publish(PUBSUBTOPIC['WISHLISTADDFAILED'],
        {
            message: "L'article n'a pas pu être retiré des Favoris",
            count: response.item_count,
            action: this.$to_remove.remove
        } );
        console.log("Wishlist : Remove request sent successfully");
                //this.count =  response.item_count;
                //this.$to_remove.remove();
                //this.$to_remove = {};
                //this.notify({message: "L'article a été retiré des Favoris"});
    };

    Wishlist.prototype.onRemoveItemFailed = function(error){
        this.dispatcher.publish(PUBSUBTOPIC['WISHLISTADDFAILED'],{message: "L'article n'a pas pu être retiré des Favoris"} );
        //this.notify({message: "L'article n'a pas pu être retiré des Favoris"});
        console.log("Wishlist Error : couldn't remove item from the wishlist");
    };


    Wishlist.prototype.addItem = function(topic, item){
        var data = {product_id:item.id};
        var url = '/wishlist/ajax_add_to_wishlist/';
        var settings = {
            type        :'POST',
            url         : '/wishlist/ajax_add_to_wishlist/',
            data        : data,
            dataType    : 'json'
        };

        return ajax(settings).then(this.onAddItemSucess.bind(this), this.onAddItemFailed.bind(this));
    };
    Wishlist.prototype.removeItem = function(itemID){
        var options = {
            type: 'POST',
            url: '/wishlist/ajax_remove_from_wishlist/',
            data: {product_id: itemID},
            dataType:'json'
        };

        return ajax(options);
    };
    Wishlist.prototype.clear = function(topic, item){
        var options = {
            type: 'POST',
            url: '/wishlist/ajax_wishlist_clear/',
            data: {},
            dataType:'json'};

        return ajax(options).then(this.onClearSuccess.bind(this), this.onClearFailed.bind(this));
            
    };

    Wishlist.prototype.get = function(itemID){
        return this.items.find(function(item){
            return item.id === itemID;
        });
    };

    Wishlist.prototype.notify = function(notification){
        console.log("Wishlist changed ...");
        this.$counter.html("<strong>" + this.count + " </strong>");
        if(this.count == 0){
            this.$clear_btn.hide();
        }
        else{
            this.$clear_btn.show();
        }
        this.catalog.notify(notification);
        
    };

    return Wishlist;
})();


var Checkout = (function(){
    function Checkout(){
        this.currentTab = 0;
        this.tabCount = 0;
        this.tabs = {};
        this.tab = {};
        this.nextBtn = {};
        this.prevBtn = {};
        this.submitBtn = {};
        this.paiementChoiceBtn = {};
        this.$inputs = {};
        this.$form = {};

    }
    Checkout.prototype.init = function(){
        this.paiementOpt = 2;
        this.$form = $("#flat-order-form");
        this.tabs = $(".flat-tabcontent-checkout");
        this.tab = $(".flat-tab-checkout");
        this.nextBtn = $("#js-checkout-next-btn");
        this.prevBtn = $("#js-checkout-prev-btn");
        this.submitBtn = $("#js-checkout-submit-btn");
        this.paiementChoiceBtn = $(".choice");
        this.$inputs = this.paiementChoiceBtn.find('[type="radio"]');
        console.log("Checkout Init : we found " + this.$inputs.length + " inputs");
        this.prevBtn.hide();
        this.tabs.hide();
        this.tab.click(this.onTabClicked.bind(this));
        this.nextBtn.click(this.onNextClicked.bind(this));
        this.prevBtn.click(this.onPrevClicked.bind(this));
        //this.submitBtn.click(this.onSubmitClicked.bind(this));
        this.$form.submit(this.onSubmitClicked.bind(this));
        this.paiementChoiceBtn.click(this.inputUpdate.bind(this));
        this.tabCount = this.tab.length;
        this.update();
    };

    Checkout.prototype.inputUpdate = function(event){
        var choice = $(event.target).parents(".choice");
        var input = choice.find('[type="radio"]');
        console.log("Input clicked : Value : ");
        this.paiementChoiceBtn.removeClass("active");
        this.$inputs.removeAttr('checked');
        choice.addClass("active");
        input.attr('checked', 'true');
        this.nextBtn.removeClass("disabled");
        console.log(input);
        console.log(choice);
    };
    Checkout.prototype.onNextClicked = function(event){
        
        
        if(this.currentTab != 1){
            this.tab.removeClass("active");
            this.currentTab = (this.currentTab + 1 ) % this.tabCount;
            this.update();
        }
        else{
            console.log("Checking for checked input");
            if(this.isInputChecked()){
                this.tab.removeClass("active");
                this.currentTab = (this.currentTab + 1 ) % this.tabCount;
                //this.nextBtn.removeClass("disabled");
                this.update();
            }
            else{
                console.log("No valid input found");
                //this.nextBtn.addClass("disabled");
            }
        }
        

    };
    Checkout.prototype.isInputChecked = function(){
        return $('input:checked').length == 1;
    };
    Checkout.prototype.onPrevClicked = function(event){
        this.tab.removeClass("active");
        this.currentTab = (this.currentTab - 1 ) % this.tabCount;
        this.update();
    };
    Checkout.prototype.onSubmitClicked = function(event){
        console.log("Checkout is being submitted")
        //event.stopPropagation();
        //event.preventDefault();
        return true;
    };

    Checkout.prototype.onTabClicked = function(event){
        event.stopPropagation();
        var tab = parseInt($(event.target).data("index"));
        if(tab == 2){
            if(this.isInputChecked()){
                this.currentTab = tab;
                console.log("there is one input checked");
                this.update();
            }
            else
                console.log("there is no input checked");
        }
        else if( (tab != this.currentTab) && (tab < 3) && (tab >= 0)){
            
            this.currentTab = tab;
            this.update();
        }
    };

    Checkout.prototype.update = function(){
        if( (this.currentTab == 1) && !this.isInputChecked()){
            this.nextBtn.addClass("disabled");
        }
        else{
            this.nextBtn.removeClass("disabled");
        }
        this.tab.removeClass("active");
        $(this.tab[this.currentTab]).addClass("active");
        if(this.currentTab > 0){
            this.prevBtn.show();
        }
        else{
            this.prevBtn.hide();
        }
        if(this.currentTab == (this.tabCount - 1)){
            this.nextBtn.hide();
        }
        else{
            this.nextBtn.show();
        }
        this.tabs.hide();
        $(this.tabs[this.currentTab]).show();
        if(this.currentTab == 2){
            this.submitBtn.show();
        }
        else{
            this.submitBtn.hide();
        }
    };
    return Checkout;
})();


var Banner = (function(){
    function Banner(){
        this.banner_texts_sources   = {};
        this.banner_content         = {};
        this.banner_images_sources  = {};
        this.banner_texts           = {};
        this.banner_images          = 
        [
            '/media/assets/ads1.png',
            '/media/assets/ads2.png'
        ];
        this.ads_image              = {};
        this.pos_image              = 0;
        this.total_image            = 0;
        this.pos_text               = 0;
        this.total_text             = 0;
        this.banner_item            = {};
        this.ads_texts              = [
            "Chez <span class=\"flat-link\">LYSHOP</span>, c'est la qualité avant tout",
            "Votre bonheur est notre plaisir",
            "Chez Lyshop vous ne trouverez que des articles originaux",
            "Livraison sur Libreville & Port-gentil",
            "Des Produits de qualités à des prix imbatable"
    ];


    }
    Banner.prototype.init = function(){
        this.banner_texts_sources   = $(".js-banner-texts");
        this.banner_content         = $("#js-banner-content");
        this.banner_item            = $(".banner-item");
        this.banner_images_sources  = $(".js-banner-images");
        this.banner_texts           = this.banner_texts_sources.children(".banner-text");
        this.ads_image              = $("img.ads-image");
        this.total_text             = this.ads_texts.length;
        this.total_image            = this.banner_images.length;
        setInterval(this.playText, 5000, this);
    };

    Banner.prototype.playText = function(that){
        that.pos_text = (that.pos_text + 1) % that.total_text;
        that.pos_image = (that.pos_image + 1) % that.total_image;
        that.banner_item.html(that.ads_texts[that.pos_text]);
        that.ads_image.attr('src', that.banner_images[that.pos_image]);
    };

    return Banner;

})();


/*
var FinancesChart = (function(){
    function FinancesChart(){
        this.canva = {};
        this.data = [];
        this.chart = {};
        this.chartOptions = {};

    };
    FinancesChart.prototype.init = function(){
        this.canva = $("#myChart");
        this.chartOptions = {
            type: 'line',
            data: {
                labels: ["Janvier", "Fevrier", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Decembre"],
                datasets: [{
                    label: 'Nombre de ventes',
                    data: [12, 19, 3, 5, 54, 3, 16, 23, 10, 5, 10, 70],
                    fill: false,
                    borderWidth: 1,
                    borderColor: '#5AC3AE'
                }]
            },
            options: {
                title:{
                    display: true,
                    text: 'Observation Annuelle 2017',
                    position: 'bottom',

                },
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero:true
                        }
                    }]
                }
            }
        };
        this.chart = new Chart(this.canva,this.chartOptions);
        console.log("FinanceChart initialized ");
    };

    return FinancesChart;
})();
Dashboard = {};
*/
Shopping = {};

if(typeof (Storage)!== "undefined"){
    shopStorage  = localStorage;
    //shopStorage.Shopping = shopStorage.Shopping || {} ;

    if(shopStorage.Shopping === undefined){
        var store = {'initialized' : 1, 
                     'cartItems' : [],
                     'cartItemCount': 0,
                     'cartTotal' : 0};
        shopStorage.setItem("Shopping", JSON.stringify(store));
    }
    else{
        console.log ("Storage Shopping already initialized : " + shopStorage.Shopping);
    }
    console.log("This Browser support webstorage");
}
else{
    console.log("This Browser doesn't support webstorage");
}


//Shopping.wishlist.addCatalog(Shopping.catalog);
//Shopping.cart.addCatalog(Shopping.catalog);

//Dashboard.financeChart = new FinancesChart();
//Dashboard.financeChart.init();
