/* To avoid CSS expressions while still supporting IE 7 and IE 6, use this script */
/* The script tag referencing this file must be placed before the ending body tag. */

/* Use conditional comments in order to target IE 7 and older:
	<!--[if lt IE 8]><!-->
	<script src="ie7/ie7.js"></script>
	<!--<![endif]-->
*/

(function() {
	function addIcon(el, entity) {
		var html = el.innerHTML;
		el.innerHTML = '<span style="font-family: \'icomoon-reg\'">' + entity + '</span>' + html;
	}
	var icons = {
		'icon-external-link': '&#xf08e;',
		'icon-trash-alt': '&#xe917;',
		'icon-clipboard': '&#xe95a;',
		'icon-heart-1': '&#xe926;',
		'icon-heart': '&#xe902;',
		'icon-vk': '&#xe956;',
		'icon-check2': '&#xe951;',
		'icon-th': '&#xf00a;',
		'icon-th-list': '&#xf00b;',
		'icon-filter': '&#xe94b;',
		'icon-check-square': '&#xe935;',
		'icon-dollar-1': '&#xe92b;',
		'icon-bar-chart': '&#xe924;',
		'icon-balance': '&#xe925;',
		'icon-angle-down': '&#xe920;',
		'icon-angle-up': '&#xe921;',
		'icon-angle-right': '&#xe922;',
		'icon-angle-left': '&#xe923;',
		'icon-pencil': '&#xe90e;',
		'icon-fancy': '&#xe943;',
		'icon-tool-layout-1': '&#xe93b;',
		'icon-settings': '&#xe93c;',
		'icon-tool-layout': '&#xe93d;',
		'icon-tool-header': '&#xe93e;',
		'icon-tool-color': '&#xe93f;',
		'icon-tool-round': '&#xe940;',
		'icon-tool-side': '&#xe941;',
		'icon-dollar-bills': '&#xe91e;',
		'icon-left-arrow-circular': '&#xe937;',
		'icon-right-arrow-circular': '&#xe91f;',
		'icon-star-fill': '&#xe952;',
		'icon-star': '&#xe91c;',
		'icon-star-half': '&#xe91d;',
		'icon-close-envelope': '&#xe915;',
		'icon-facebook-logo': '&#xe916;',
		'icon-skype-logo': '&#xe918;',
		'icon-twitter-logo': '&#xe919;',
		'icon-vimeo': '&#xe91a;',
		'icon-youtube-logo': '&#xe91b;',
		'icon-user': '&#xe900;',
		'icon-eye': '&#xe901;',
		'icon-magnify': '&#xe903;',
		'icon-scale-arrows': '&#xe904;',
		'icon-share': '&#xe905;',
		'icon-cart-1': '&#xe906;',
		'icon-undo': '&#xe907;',
		'icon-money': '&#xe908;',
		'icon-plane': '&#xe909;',
		'icon-gift': '&#xe90a;',
		'icon-help': '&#xe90b;',
		'icon-location': '&#xe90c;',
		'icon-dollar': '&#xe90d;',
		'icon-raketa': '&#xe90f;',
		'icon-cart': '&#xe910;',
		'icon-diamant': '&#xe911;',
		'icon-like2': '&#xe912;',
		'icon-plane-1': '&#xe913;',
		'icon-grid': '&#xe958;',
		'icon-pictures': '&#xe959;',
		'icon-like': '&#xe94f;',
		'icon-close-2': '&#xe944;',
		'icon-chat': '&#xe927;',
		'icon-minus': '&#xe94c;',
		'icon-close-1': '&#xe932;',
		'icon-close': '&#xe933;',
		'icon-menu': '&#xe931;',
		'icon-headset-mic': '&#xe92e;',
		'icon-plus': '&#xe94a;',
		'icon-arrow-right': '&#xe946;',
		'icon-arrow-left': '&#xe947;',
		'icon-arrow-down': '&#xe948;',
		'icon-arrow-up': '&#xe949;',
		'icon-instagram': '&#xe955;',
		'icon-google': '&#xe93a;',
		'icon-linkedin': '&#xe938;',
		'icon-pinterest': '&#xe939;',
		'icon-dots-three-horizontal': '&#xe934;',
		'icon-copy': '&#xe95b;',
		'icon-rtl': '&#xe957;',
		'icon-play': '&#xe953;',
		'icon-film': '&#xe954;',
		'icon-check': '&#xe950;',
		'icon-zoomout': '&#xe94d;',
		'icon-zoomin': '&#xe94e;',
		'icon-sync': '&#xe945;',
		'icon-alert': '&#xe936;',
		'icon-calendar': '&#xe92f;',
		'icon-clock': '&#xe930;',
		'icon-airplane': '&#xe92c;',
		'icon-truck': '&#xe92d;',
		'icon-right-quote': '&#xe929;',
		'icon-left-quote': '&#xe92a;',
		'icon-comment': '&#xe928;',
		'icon-home': '&#xe914;',
		'icon-phone': '&#xe942;',
		'icon-undo-1': '&#xe967;',
		'icon-equalizer': '&#xe992;',
		'icon-bin': '&#xe9ac;',
		'icon-star-empty': '&#xe9d7;',
		'icon-spinner': '&#xe97b;',
		'icon-spinner-1': '&#xe981;',
		'0': 0
		},
		els = document.getElementsByTagName('*'),
		i, c, el;
	for (i = 0; ; i += 1) {
		el = els[i];
		if(!el) {
			break;
		}
		c = el.className;
		c = c.match(/icon-[^\s'"]+/);
		if (c && icons[c[0]]) {
			addIcon(el, icons[c[0]]);
		}
	}
}());
