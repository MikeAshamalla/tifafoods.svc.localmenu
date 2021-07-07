//<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
//<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>
//  <script>
function getURLParam(name) {
    var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
    if (results==null) {
       return null;
    }
    else {
       return results[1] || 0;
    }
}

function addLocalFlavorItems(items) {
	var htmlOut = '';

	htmlOut += '<h2 class="card-subtitle mb-2 text-muted">Current Local Flavors<\/h2><ul>';
	items.forEach(function (item, key) {
		htmlOut += '<li>' + item + '<\/li>';
	});
htmlOut += '<\/ul>'
	return htmlOut;
}

function displayItems(data) {
	var pricedItems = data.response.pricedItems;
	var groupPricedItems = data.response.groupPricedItems;
	var htmlOut = '';
	
	pricedItems.forEach(function (catItem, catKey) {
	htmlOut += '<div class="card" style="margin-bottom:15px"><div class="card-body">';
		htmlOut += '<h1 class="card-title">' + catItem.category + '<\/h1>';
		if (catItem.subCategory != '') {
			htmlOut += '<h2 class="card-subtitle mb-2 text-muted">' + catItem.subCategory + '<\/h2>';
		}
		if (catItem.localFlavors.length > 0) {
			htmlOut += addLocalFlavorItems(catItem.localFlavors);
		}      
  htmlOut += '<ul class="list-group list-group-flush">'
		catItem.items.forEach(function (item, key) {
			var ulLine = '<strong>' + item.name + '<\/strong>&nbsp;&nbsp;&nbsp;';
			item.priceList.forEach(function (priceListItem, priceListKey) {
				ulLine += '';
				if (priceListItem.size != '') {
					ulLine += '<strong>' + priceListItem.size + '<\/strong>-';
				}
				ulLine += '$' + priceListItem.price + '<\/span>&nbsp;&nbsp;&nbsp;';
			});
			htmlOut += '<li class="list-group-item">' + ulLine + '<\/li>';
		})
		htmlOut += '<\/ul><\/div><\/div>';
	});
	return htmlOut;	
}

jQuery(window).load(function($) {

	alert('tfiloc = ' + getURLParam('tfiloc'));
	
	jQuery('#tfilocalmenu').html('<div style="text-align: center"><img src="https://tifachocolateandgelato.com/wp-content/uploads/2021/07/spinner.gif"\/><\/div>');

	var jqxhr = jQuery.getJSON('https://1jf6x7kd5a.execute-api.us-west-2.amazonaws.com/Prod/tifafoods_svc_localmenu?location=F00000-1')
		.done(function( data ) {
			jQuery('#tfilocalmenu').html('<div class="card-deck">' + displayItems(data) + '<\/div>');
  });

});
// </script>
// <div id="tfilocalmenu"></div>
