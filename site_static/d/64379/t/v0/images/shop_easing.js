$(function() {
	var prod = $('div[id^=tovar_card]');
	var img = prod.find('a.highslide img');
	var pos = img.offset();
	var pos_target = $('#cart_total').offset();
	var bd = $('body');
	prod.find(':submit').click(function() {
		var i = img.clone().css({
			position: 'absolute',
			display: 'none',
			'z-index': 100
		});
		i.attr('src', img.attr('scrolls'));
		bd.append(i);
		i.css({
			left: pos.left,
			top: pos.top,
			display: 'block'
		}).animate({
			left: pos_target.left - i.width() / 2,
			top: pos_target.top,
			'opacity': 0
		}, 1000, function() {
			i.remove();	
		});
	});
})