define(function(require) {
    'use strict';
var $ = require('jquery');
$('.js-custom-input .input-value').on('click', function(event){
    $(this).toggle();
    $('.input-edit-wrapper', $(this).parent()).toggle();
});

/*
$('.js-custom-input .js-edit').on('click', function(event){
    $(this).parent().toggle();
    $(this).siblings('input').toggle();
});
*/

$('.js-custom-input input').on('keyup change', function(event){
    var $el = $(this);
    $el.parent().siblings('.input-value').html($el.val());
});

$('.js-custom-input .js-edit-close').on('click', function(event){
    var $el = $(this).siblings('input');
    $el.parent().siblings('.input-value').html($el.val());
    $(this).parent().toggle();
});

console.info("Styling module loaded");

});
