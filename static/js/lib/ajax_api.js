define(['require', 'lang'], function(require, Locale) {
    'use strict';
    var $ = require('jquery');
    /**
       * 
       * @param {*} options is a JSON defining the following data :
       * type - string
       * url - string
       * data - json
       * dataType - string
       * Example : 
       * type: 'POST',
         url : '/cart/add_to_cart/',
        data: {product_id: 102, quantity: 4},
        dataType: 'json'
  
        A future object is returned
    */

      function ajax_api(options, url_contain_lang, debug){
        if(debug){
          console.debug("ajax_api options - ", options);
        }
        if(!url_contain_lang){
          options.url = '/' + Locale.get_lang() + options.url;
        }
        
        return new Promise(function(resolve, reject){
            $.ajax(options).done(resolve).fail(reject);
        });
      }
    console.log("Ajax API ready");
    return ajax_api;
  });