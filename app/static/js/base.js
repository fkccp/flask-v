var ie = !!(document.all)
function $(id) { return document.getElementById(id) }
function c(tag) {return document.createElement(tag)}
function l(o) {console.log(o)}
function sel()
{
	var s = {
			sel:ie?document.selection:window.getSelection()
		};
		s.rg = ie?s.sel.createRange():s.sel.getRangeAt(0);
		s.clear = function()
		{
			if(ie)
			{
				s.sel.clear();
			}
			else
			{
				s.rg.deleteContents();
			}
		};
		s.val = function(t)
		{
			if('undefined' == typeof(t))
			{
				return ie?s.rg.text:s.sel.toString;
			}
			else
			{
				s.clear();
				if(ie)
				{
					s.rg.text = t;
				}
				else
				{
					var fg = s.rg.createContextualFragment(t);
					var lastNode = fg.lastChild;
					s.rg.insertNode(fg);
					s.rg.setStartAfter(lastNode);
					s.rg.setEndAfter(lastNode);
					s.sel.removeAllRanges();
					s.sel.addRange(s.rg);
				}
			}
		};
		s.html = function(t)
		{
			if('undefined' == typeof(t))
			{
				return ie?s.rg.htmlText:s.sel.toString;
			}
			else
			{
				if(ie)
				{
					s.rg.pasteHTML(t);
				}
				else
				{
					s.val(t);
				}
			}
		};
		return s;
}

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


// map
function init_index_map()
{
	var u = function(g)
	{
		g = g.split(',')
		var a = (g[0]*1+g[1]*1)/2, b = (g[0]*1-g[1]*1)/2
		return [a, b]
	}
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
// map end

// editor
function init_editor()
{
	var ori = $('editor'), wrapper = ori.parentNode, _ = c('div')
	ori.style.display = 'none'
	ori.setAttribute('id', '')
	_.innerHTML = '<div id="emotion"><a href="javascript:;">插入表情</a><div tabindex=1></div></div><div id="editor" contenteditable="true">'+ori.value+'</div>'
	wrapper.appendChild(_)

	// gen emos
	var btn = $('emotion'), editor = $('editor'), emo_wrapper = btn.getElementsByTagName('div')[0], cats = ['普通表情', '文艺表情', '2X表情'], _s2 = _s3 = ''
	for(i=0;i<3;i++)
	{
		_s2 += '<span>'+cats[i]+'</span>'
		_s3 += '<ul>'
		for(j=1;j<33;j++)
		{
			var n = j;
			if(n<10) n = '0'+n;
			_s3 += '<li><img src="/static/img/emos/'+i+n+'.gif"></li>'
		}
		_s3 += '</ul>'
	}
	emo_wrapper.innerHTML = _s2 + _s3

	var _spans = emo_wrapper.getElementsByTagName('span'), _uls = emo_wrapper.getElementsByTagName('ul'), lis = emo_wrapper.getElementsByTagName('li'), spans = [], uls = [], z_index = 1, reg = /(\s|^)on(\s|$)/
	for(var i=0;i<3;i++)
	{
		uls[i] = _uls[i]
		spans[i] = _spans[i]

		spans[i].onmouseover = function()
		{
			var index = spans.indexOf(this)
			for(j in spans)
			{
				if(j != i) spans[j].className = spans[j].className.replace(reg, ' ')
			}
			this.className += ' on'
			z_index++
			uls[index].style.zIndex = z_index
		}
	}
	spans[0].className += ' on'
	uls[0].style.zIndex = z_index

	for(i in lis)
	{
		lis[i].onclick = function()
		{
			editor.focus()
			sel().html(this.innerHTML)
			emo_wrapper.style.display = 'none'
		}
	}

	btn.getElementsByTagName('a')[0].onclick = function()
	{
		emo_wrapper.style.display = 'block'
		emo_wrapper.focus()
	}

	emo_wrapper.onblur = function(){ emo_wrapper.style.display = 'none' }

	_ = wrapper
	while(true)
	{
		_ = _.parentElement
		if (_.nodeName.toLowerCase() == 'form' || _ == document) break
	}

	_.onsubmit = function()
	{
		ori.value = editor.innerHTML
	}
}

if($('editor')) init_editor();
// editor end

// reply
function init_reply()
{
	var wrapper = $('reply_tip'), pid_input = $('pid'), btns = document.getElementsByClassName('cmt_reply'), reply_user = $('reply_user'), reply_cnt = $('reply_cnt')
	for(i in btns)
	{
		btns[i].onclick = function()
		{
			var cmt_wrapper = this.parentElement.parentElement,
				user = cmt_wrapper.getElementsByTagName('a')[0].innerHTML,
				cnt = cmt_wrapper.getElementsByTagName('div')[0].innerHTML,
				pid = cmt_wrapper.getAttribute('data-id')
			reply_user.innerHTML = user
			reply_cnt.innerHTML = cnt
			pid_input.value = pid
			wrapper.style.display = 'block'
		}
	}
	$('reply_cancel').onclick = function()
	{
		pid_input.value = 0
		wrapper.style.display = 'none'
	}
}

if(document.getElementsByClassName('cmt_reply').length) init_reply();
// reply end