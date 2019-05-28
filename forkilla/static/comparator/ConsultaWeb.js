function buscar(ip){
	var city = $("#city" ).val();
	var category = $("#category" ).val();
	var price = $("#price" ).val();
	alert('Crea');
	//url = 'http://'+ ip + ':8000/api/restaurants/?';

	url = 'https://' + ip + '.herokuapp.com/api/restaurants/?';
	url += (category)? 'category='+category : '';

	url += (city)? '&city='+city : '';

	url += (price)? '&price_average='+price : '';

	alert('escriu');

	$.getJSON( url, function( data ) {
	  var items = [];


		items.push( "<p>For " + ip + ":</p>" );
	  for (var i=0; i < data["count"] ; i++ )
	  {
	  	items.push( "<p><b> -Adress</b>: " + data["results"][i]["address"] + "</p>" );
	  	items.push( "<p><b> -Capacity</b>: " + data["results"][i]["capacity"] + "</p>" );
	  	items.push( "<p><b> -Category</b>: " + data["results"][i]["category"] + "</p>" );
	  	items.push( "<p><b> -City</b>: " + data["results"][i]["city"] + "</p>" );
	  	items.push( "<p><b> -Country</b>: " + data["results"][i]["country"] + "</p>" );
	  	items.push( "<p><b> -Description</b>: " + data["results"][i]["menu_description"] + "</p>" );
	  	items.push( "<p><b> -Name</b>: " + data["results"][i]["name"] + "</p>" );
	  	items.push( "<p><b> -Price average</b>: " + data["results"][i]["price_average"] + "</p>" );
	  	items.push( "<p><b> -Rate</b>: " + data["results"][i]["rate"] + "</p>" );

	  	items.push( "-------------" );

	  }
	  $('#Results').remove();

	  $( "<div/>", {
	    html: items.join( "" ),
		id: "Results"
	  }).appendTo( "body" );
	});
}

function test(c) {
	alert(c);
}

function comparar(){
	var ips = $('#ips').text();

	ips = ips.slice(2, ips.length);
	ips = ips.slice(ips, -1);

	ips = ips.replace(/'/g, '');


	ips = ips.split(',');
	alert('ips: ' + ips);
	ips.forEach(function (arrayItem) {
		alert('Consulta: '+ arrayItem);
		arrayItem = arrayItem.replace(' ', '');
		buscar(arrayItem);
	});
}
