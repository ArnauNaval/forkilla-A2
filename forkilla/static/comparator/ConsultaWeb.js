function buscar(ip){
	var city = $("#city" ).val();
	var category = $("#category" ).val();
	var price = $("#price" ).val();

	url = 'https://' + ip + '.herokuapp.com/api/restaurants/?';
	url += (category)? 'category='+category : '';

	url += (city)? '&city='+city : '';

	url += (price)? '&price_average='+price : '';


	$.getJSON( url, function( data ) {
		var items = [];
		var tmp = [];

		items.push( "<p>For " + ip + ":</p>" );
		if(data["count"] == 0){
			items.push("<p>There is no data with this specifications</p>")
			items.push( "-------------" );
		}
		else{
			for (var i=0; i < data["count"] ; i++ ){
				var nose = [];

				nose.push( "<p><b> -Adress</b>: " + data["results"][i]["address"] + "</p>" );
				nose.push( "<p><b> -Capacity</b>: " + data["results"][i]["capacity"] + "</p>" );
				nose.push( "<p><b> -Category</b>: " + data["results"][i]["category"] + "</p>" );
				nose.push( "<p><b> -City</b>: " + data["results"][i]["city"] + "</p>" );
				nose.push( "<p><b> -Country</b>: " + data["results"][i]["country"] + "</p>" );
				nose.push( "<p><b> -Description</b>: " + data["results"][i]["menu_description"] + "</p>" );
				nose.push( "<p><b> -Name</b>: " + data["results"][i]["name"] + "</p>" );
				nose.push( "<p><b> -Price average</b>: " + data["results"][i]["price_average"] + "</p>" );
				nose.push( "<p><b> -Rate</b>: " + data["results"][i]["rate"] + "</p>" );

				nose.push( "-------------" );

				tmp.push([parseInt(data["results"][i]["price_average"]), nose]);
			}
		}

		tmp.sort(Comparator);

		for(var i = 0; i<tmp.length; i++)
		{
			for(var j=0; j<tmp[0][1].length; j++)
			{
				items.push(tmp[i][1][j]);
			}
		}


	  $( "<div/>", {
	    html: items.join( "" ),
		id: "Results"
	  }).appendTo( "body" );
	});
}

function buscarCheapest(ips){
	var city = $("#city" ).val();
	var category = $("#category" ).val();
	var price = $("#price" ).val();
	var items = [];
	var tmp = [[999999999999,'']];

	$.ajaxSetup({
    	async: false
	});

	ips.forEach(function (ip) {
		ip = ip.replace(' ', '');


		url = 'https://' + ip + '.herokuapp.com/api/restaurants/?';
		url += (category)? 'category='+category : '';

		url += (city)? '&city='+city : '';

		url += (price)? '&price_average='+price : '';


		$.getJSON( url, function( data ) {

			if(data["count"] > 0){

				for (var i=0; i < data["count"] ; i++ ){
					var nose = [];

					if(parseInt(data["results"][i]["price_average"]) < tmp[0][0])
					{

						tmp.pop();

						nose.push( "<p><b> -Adress</b>: " + data["results"][i]["address"] + "</p>" );
						nose.push( "<p><b> -Capacity</b>: " + data["results"][i]["capacity"] + "</p>" );
						nose.push( "<p><b> -Category</b>: " + data["results"][i]["category"] + "</p>" );
						nose.push( "<p><b> -City</b>: " + data["results"][i]["city"] + "</p>" );
						nose.push( "<p><b> -Country</b>: " + data["results"][i]["country"] + "</p>" );
						nose.push( "<p><b> -Description</b>: " + data["results"][i]["menu_description"] + "</p>" );
						nose.push( "<p><b> -Name</b>: " + data["results"][i]["name"] + "</p>" );
						nose.push( "<p><b> -Price average</b>: " + data["results"][i]["price_average"] + "</p>" );
						nose.push( "<p><b> -Rate</b>: " + data["results"][i]["rate"] + "</p>" );

						tmp.push([parseInt(data["results"][i]["price_average"]), nose]);
					}
				}
			}
		});
	});

	items.push("<h1> Cheapest restaurant: </h1>");

	for(var j=0; j<tmp[0][1].length; j++)
	{
		items.push(tmp[0][1][j]);
	}

	$( "<div/>", {
	html: items.join( "" ),
	id: "Results"
	}).appendTo( "body" );

	$.ajaxSetup({
    	async: true
	});

}

function Comparator(a, b) {
   if (a[0] < b[0]) return -1;
   if (a[0] > b[0]) return 1;
   return 0;
 }


function comparar(){
	var ips = $('#ips').text();

	ips = ips.slice(2, ips.length);
	ips = ips.slice(ips, -1);

	ips = ips.replace(/'/g, '');

	ips = ips.split(',');

	while($('#Results').length>0){
		$('#Results').remove();
	}

	ips.forEach(function (arrayItem) {
		arrayItem = arrayItem.replace(' ', '');
		buscar(arrayItem);
	});
}

function cheapest(){
	var ips = $('#ips').text();

	ips = ips.slice(2, ips.length);
	ips = ips.slice(ips, -1);

	ips = ips.replace(/'/g, '');

	ips = ips.split(',');

	while($('#Results').length>0){
		$('#Results').remove();
	}

	buscarCheapest(ips);
}