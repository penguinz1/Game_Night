/* 
source:
https://codepen.io/le0864/pen/pbmoVQ
*/

var focus = document.getElementById("rand-ind");

// function for a simple coin flip animation
jQuery(document).ready(function($){

  $('#coin').on('click', function(){
    let num = parseInt(focus.value);
    $('#coin').removeClass();
    setTimeout(function(){
      if(heads_tails(num)){
        $('#coin').addClass('heads');
        console.log('it is head');
      }
      else{
        $('#coin').addClass('tails');
        console.log('it is tails');
      }
      focus.value++; // updates random index
    }, 100);
  });
  
});