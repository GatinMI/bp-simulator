function dropLanguages(){
	var list = $('#languages-list');
	if (list.css('display') == 'none')
		list.show();
	else list.hide();
}

window.onclick = function(event) {
  if (!event.target.matches('.dropbtn')) {
  	$('#languages-list').hide();
    
  }
}