define(['vendor/js.cookie'],function(Cookies) {
    'use strict';
    var lang_cookie = "";
    const LANGUAGE_KEY = 'django_language';
    const DEFAULT_LANGUAGE = "fr";
    function getCookie(cname) {
        var name = cname + "=";
        var decodedCookie = decodeURIComponent(document.cookie);
        var ca = decodedCookie.split(';');
        for(var i = 0; i <ca.length; i++) {
          var c = ca[i];
          while (c.charAt(0) == ' ') {
            c = c.substring(1);
          }
          if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
          }
        }
        return "";
    }

    function get_lang(){
      const current_lang = $('#current-lang').val();
      return current_lang;
    }
    function change_language(element){
        console.log("change language clicked");
        var form = $('#lang-form');
        var $el = $(element);
        if($el.hasClass('active')||$el.hasClass('selected')){
            return;
        }
        var name = $('input[name="language"]', form);
        lang_cookie = $el.data('value');
        name.val($el.data('value'));
        document.cookie = "django_language=";
        document.cookie = "django_language=" + name.val() +";";
        //Cookies.set(LANGUAGE_KEY, name.val());
        form.submit();
    }
    $('.js-lang').on('click', function(event){
        change_language(this);
    });
    console.log("lang.js installed");
    return {get_cookie: getCookie, get_lang: get_lang}
});