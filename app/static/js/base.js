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
	a = (g[0]*1+g[1]*1)/2
	b = (g[0]*1-g[1]*1)/2
	return ''+a+','+b
}

function init_index_map()
{
	var map = new soso.maps.Map($('indexmap'), {
		center: new soso.maps.Latlng(0, 0),
		zoom: 10
	}), markers = []
	for(i in index_data)
	{
		var g = index_data[i]['geo']
		g = u(g)
		console.log(g)
		var marker = new soso.maps.Marker({map: map})
		marker.setPosition(new soso.maps.LatLng(g[0], g[1]))		
	}
}