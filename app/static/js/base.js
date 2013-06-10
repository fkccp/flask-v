function $(id) { return document.getElementById(id) }

function like(obj)
{
	var ret = true
	if(obj.action.indexOf('cmt_like') != -1)
	{
		ret = confirm('确定要赞这条评论吗？将会消耗您1个金币。')
	}
	else if(obj.action.indexOf('bbs/action/like') != -1)
	{
		ret = confirm('确定要赞这篇主题吗？将会消耗您3个金币。')
	}
	return ret
}

function u(g)
{
	g = g.split(',')
	var a = (g[0]*1+g[1]*1)/2, b = (g[0]*1-g[1]*1)/2
	return [a, b]
}

function init_index_map()
{
	var map = new soso.maps.Map($('indexmap'), {
		center: new soso.maps.LatLng(31.777328075530842, 104.154296875),
		zoom: 4
	}), markers = [], info = new soso.maps.InfoWindow({map:map})
	info.maxWidth = 90
	new soso.maps.MapTypeControl({map:map})
	for(i in index_data)
	{
		var g = index_data[i]['geo']
		g = u(g)
		var marker = new soso.maps.Marker({map: map});
		marker.setPosition(new soso.maps.LatLng(g[0], g[1]));
		(function(marker){
			soso.maps.event.addListener(marker, 'click', function(){
			info.open()
			// info.setContent('<div style="margin:10px;">'+index_data[i]['avatar']+'</div>')
			info.setContent('<img style="padding:3px;border:1px solid #999;margin-top:5px;" src="'+index_data[i]['avatar']+'" alt="50" title="'+index_data[i]['name']+'"  />')
			info.setPosition(marker)
		})
		})(marker);
	}

	soso.maps.event.addListener(map, 'click', function(){
		info.close()
	})
}

var seting_map_init_obj = null

var seting_map_init = function(obj) {
	console.log(obj)
	if(seting_map_init_obj == obj) return
	seting_map_init_obj = obj

	var x = 31.743740, y = 110.669955, z = 12, val = obj.value;
	if(val)
	{
		val = val.split(',')
		if(3 == val.length)
		{
			x = val[0], y = val[1], z = val[2]*1
		}
	}

	var map_div = $('setting_map'), setting_map_wrapper = $('setting_map_wrapper'), map = new soso.maps.Map(map_div,{
		center: new soso.maps.LatLng(x, y),
		zoom: z
	});

	obj.parentNode.appendChild(setting_map_wrapper)
	setting_map_wrapper.style.display = 'block'

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

function seting_map_close(){$('setting_map_wrapper').style.display = 'none'}