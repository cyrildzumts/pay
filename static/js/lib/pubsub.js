/*export {
    Dispatcher,
    Subscriber,
    Publisher
};
*/
var generate_id = (function(){
    var id = 1;
    return function(){
        return id++;
    };
})();

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
     CARDADDITEM        : '/card/add',
     CARDADDITEMFAILED  : '/card/add/failed',
     CARDREMOVEITEM     : '/card/remove',
     CARDREMOVEITEMFAILED : '/card/remove/failed',
     CARDCLEAR          : '/card/clear',
     WISHLISTADD        : '/wishlist/add',
     WISHLISTREMOVE     : '/wishlist/remove',
     WISHLISTCLEAR      : '/wishlist/clear',
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
        if(!this.topic_pool.hasOwnProperty(topic)){
            console.log("New data publish for an undefined topic " + topic);
            console.log("Published Data : " + Data);
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
    };
    Subscriber.prototype.set_callback = function(callback){
        this.callback = callback;
    }
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



function pub_sub_test(){

    var dispatcher = new Dispatcher();
    var publisher  = new Publisher();
    var subscriber_1 = new Subscriber();
    var subscriber_2 = new Subscriber();

    var topic_1 = 10;
    var topic_2 = 20;

    var data = {content: "Data for topic 10"};
    var data2 = {content: "Data for topic 20"};


    subscriber_1.register(dispatcher);
    subscriber_2.register(dispatcher);
    publisher.register(dispatcher);
    publisher.set_topic(topic_1);

    subscriber_1.register_to_topic(topic_1);
    subscriber_1.register_to_topic(topic_2);
    subscriber_2.register_to_topic(topic_1);

    publisher.publish(data);
    publisher.set_topic(topic_2);
    publisher.publish(data2);


}


