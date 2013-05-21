var curr_obj = null

var init = function(obj) {
	if(curr_obj == obj) return
	curr_obj = obj
	var x = 31.743740, y = 110.669955, z = 12, val = obj.value;
	if(val)
	{
		val = val.split(',')
		if(3 == val.length)
		{
			x = val[0], y = val[1], z = val[2]*1
		}
	}

	var map = new soso.maps.Map(document.getElementById("setting_map"),{
		center: new soso.maps.LatLng(x, y),
		zoom: z
	});

	var marker = new soso.maps.Marker({
		map: map
	});

	if('' != obj.value)
	{
		marker.setPosition(new soso.maps.LatLng(x, y))
	}

	soso.maps.event.addListener(map, 'click', function(event) {
		if ('' == obj.value) marker.setVisible(true);
		marker.setPosition(event.latLng)
		obj.value = ''+event.latLng.getLat()+','+event.latLng.getLng()+','+map.zoom
	});
}
