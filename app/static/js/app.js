$(document).ready(function(){
	
	$( ".deleteAllChk" ).change(function(event) {
	  var table = $(event.target).closest('table');
	  if(this.checked){
	    $(".deleteCheck", table).prop("checked", true);
	  } else{
	    $(".deleteCheck", table).prop("checked", false);
	  }
	});   

	$('#log_level_select').change(function(){
		url = '/log/' + $(this).val()
		window.location.href = url
	});

	$(function(){
		var url = window.location.href.split('/');
		var level = url[url.length-1]
		console.log(level)
		$('#log_level_select').val(level)
	});


});