var $ = require('jquery-browserify');

var preferences = $('form.preferences');
var chat_list = $('nav.chat_list');

var swap = function (from, to) {
  from.fadeOut(function(){
    to.fadeIn();
  });
};

var show_preferences = function (){
  swap(chat_list, preferences);
};

var show_chat_list = function () {
  swap(preferences, chat_list);
};

$('#preferences').click(show_preferences);

preferences.find('button[type=reset]').click(show_chat_list);

preferences.find('button[type=submit]').click(function(e){
  e.preventDefault();
  $(this).attr('disabled');
  $(this).html('Salvando…');
  var nickname = preferences.find('input[name=nickname]').val();
  var url = preferences.attr('action');
  $.ajax({
    url: url,
    dataType: 'json',
    type: 'POST',
    data: {nickname: nickname},
    success: function(data) {
      $(this).removeAttr('disabled').html('salvar');
      show_chat_list();
    }.bind(this),
    error: function(xhr, status, err){
      $(this).removeAttr('disabled')
      $(this).html('Salvar');
      console.error(url, status, err.toString());
    }.bind(this)
  });
});
