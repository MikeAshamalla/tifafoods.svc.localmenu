<script>
	function addGroupPricedItems(items) {
		items.forEach(function (item, key) {
			if (item.subCategory != '') {
				jQuery('#tfilocalmenu').append('<h2>' + item.subCategory + '</h2>');
			}
			item.itemList.forEach(function (item, key) {
				jQuery('#tfilocalmenu').append('<ul>' + item + '</ul>');
			});
		});
	}

	function displayItems(data) {
		var pricedItems = data.response.pricedItems;
		var groupPricedItems = data.response.groupPricedItems;	
		
		jQuery('#tfilocalmenu').html('');
		pricedItems.forEach(function (item, key) {
			jQuery('#tfilocalmenu').append('<h1>' + item.category + '</h1>');
			if (item.category == 'Gelato') {
				addGroupPricedItems(groupPricedItems);
			}
			if (item.subCategory != '') {
				jQuery('#tfilocalmenu').append('<h2>' + item.subCategory + '</h2>');
			}
			jQuery('#tfilocalmenu').append('<figure class="wp-block-table is-style-stripes"><table><tbody>');
			item.items.forEach(function (item, key) {
				var ulLine = '<td><strong>' + item.name + '</strong></td>';
				item.priceList.forEach(function (item, key) {
					ulLine += '<td>';
					if (item.size != '') {
						ulLine += '<strong>' + item.size + '</strong>-';
					}
					ulLine += '$' + item.price + '</td>';
				});
				jQuery('#tfilocalmenu').append('<tr>' + ulLine + '</tr>');
			})
			jQuery('#tfilocalmenu').append('</tbody></table></figure>');
		});		
	}

	jQuery(window).load(function($) {

		jQuery('#tfilocalmenu').html('<div style="text-align: center"><img src="https://tifachocolateandgelato.com/wp-content/uploads/2021/07/spinner.gif"/></div>');

		var jqxhr = jQuery.getJSON('https://1jf6x7kd5a.execute-api.us-west-2.amazonaws.com/Prod/tifafoods_svc_localmenu?location=F00000-1')
			.done(function( data ) {
	    displayItems(data);
	  });

	});
</script>
<div id="tfilocalmenu"></div>
