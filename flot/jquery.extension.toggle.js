/*
* jQuery Toggle Button
* by Chris Korhonen (sourcebottle.net)
* http://github.com/ckorhonen/jQuery-Toggle-Button
*
* Licensed under the MIT License:
* http://www.opensource.org/licenses/mit-license.php
*/

jQuery.fn.toggleButton = function(settings) {
  settings = jQuery.extend({
    text: "Please Wait...",
    className: "disabled",
    preventClick: true
  }, settings);

  var originalText = $(this).text();
  if(!originalText){
    originalText = $(this).attr('value');
  }
  
  var isDisabled = $(this).hasClass(settings.className);
  
  $(this).toggleClass(settings.className).text(settings.text).attr('value', settings.text);
  
  try{  
    if(!$(this).data('events').change){
      $(this).bind('change',function(e){
        if(!$(e.target).hasClass(settings.className)){
           $(e.target).text(originalText).attr('value',originalText);
        }
      });
    }
  } catch(e){ //if no object data exists 
  }
  
  if(!isDisabled && settings.preventClick){
    $(this).attr('disabled', 'disabled');
  } else {
    $(this).removeAttr('disabled');
  }
  
  $(this).trigger('change');
};