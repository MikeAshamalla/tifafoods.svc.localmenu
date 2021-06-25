<script>
	jQuery(window).load(function($) {

		var str = `
{"response": 
    {
    "pricedItems": [
        {
            "category": "Drinks: Coffee",
            "subCategory": "",
            "items": [
                {
                    "name": "Espresso",
                    "priceList": [
                        {
                            "size": "Single",
                            "price": "2.75"
                        },
                        {
                            "size": "Double",
                            "price": "2.95"
                        }
                    ]
                },
                {
                    "name": "Latte",
                    "priceList": [
                        {
                            "size": "12 oz",
                            "price": "4.45"
                        },
                        {
                            "size": "16 oz",
                            "price": "5.20"
                        },
                        {
                            "size": "20 oz",
                            "price": "5.95"
                        }
                    ]
                },
                {
                    "name": "Macchiato",
                    "priceList": [
                        {
                            "size": "Single",
                            "price": "3.15"
                        },
                        {
                            "size": "Double",
                            "price": "3.70"
                        }
                    ]
                },
                {
                    "name": "Mocha",
                    "priceList": [
                        {
                            "size": "12 oz",
                            "price": "5.20"
                        },
                        {
                            "size": "16 oz",
                            "price": "6.20"
                        },
                        {
                            "size": "20 oz",
                            "price": "7.20"
                        }
                    ]
                }
            ]
        },
        {
            "category": "Gelato",
            "subCategory": "",
            "items": [
                {
                    "name": "Gelato Cup",
                    "priceList": [
                        {
                            "size": "Small",
                            "price": "5.20"
                        },
                        {
                            "size": "Medium",
                            "price": "6.20"
                        },
                        {
                            "size": "Large",
                            "price": "7.20"
                        }
                    ]
                },
                {
                    "name": "Gelato-Pint",
                    "priceList": [
                        {
                            "size": "",
                            "price": "12.00"
                        }
                    ]
                },
                {
                    "name": "Gelato-Quart",
                    "priceList": [
                        {
                            "size": "",
                            "price": "20.00"
                        }
                    ]
                }
            ]
        },
        {
            "category": "Baked Goods: Cookie & Brownie",
            "subCategory": "",
            "items": [
                {
                    "name": "Tifa Cookie",
                    "priceList": [
                        {
                            "size": "",
                            "price": "2.00"
                        }
                    ]
                }
            ]
        }
    ]
    ,
    "groupPricedItems": 
        [
            {"category": "Gelato",
            "subCategory": "Current Flavors",
            "itemList": ["Dark Chocolate", "Cookie Butter", "Vanilla"],
            "priceList": [{"size": "Small", "price": "4.95"}, {"size": "Medium", "price": "5.95"}, {"size": "Large", "price": "6.95"}, {"size": "Pint", "price": "12.95"}, {"size": "Quart", "price": "19.95"}]
            }
        ]
    }
}
`;


		
		var parsed = JSON.parse(str);
		var pricedItems = parsed.response.pricedItems;
		var groupPricedItems = parsed.response.groupPricedItems;
		

		function addGroupPricedItems(items) {
			groupPricedItems.forEach(function (item, key) {
				if (item.subCategory != '') {
					jQuery('#tfilocalmenu').append('<h2>' + item.subCategory + '</h2>');
				}
				item.itemList.forEach(function (item, key) {
					jQuery('#tfilocalmenu').append('<ul>' + item + '</ul>');
				});
			});
		}


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

	});
</script>
<div id="tfilocalmenu"></div>
