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