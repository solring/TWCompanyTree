(function($, undefined) {
"use strict";

  var restart = function(id){
    $('#loading-modal').modal({backdrop: false, keyboard: false});
    $.getJSON( "/authorrank/search_erdos/"+ window.sid + "/" + id + ".json", function(data){
      $('#erdos-score').empty().append($('<div>' + data.score + '</div>'));
    });
  };

  $('document').ready(function() {

    $('#myTab a').click(function (e) {
	  e.preventDefault();
	  $(this).tab('show');
    });
  });
  
  window.result_activated = restart;
}(jQuery));
