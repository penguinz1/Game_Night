/* 
source:
https://codepen.io/le0864/pen/pbmoVQ
*/

var focus = document.getElementById("rand-ind");

jQuery(document).ready(function($){

  $('#coin').on('click', function(){
    $('#coin').removeClass();
    setTimeout(function(){
      let num = parseInt(focus.getAttribute("value"));
      if(heads_tails(num)){
        $('#coin').addClass('heads');
        console.log('it is head');
      }
      else{
        $('#coin').addClass('tails');
        console.log('it is tails');
      }
      focus.setAttribute("value", num + 1);
    }, 100);
  });
  
});