/*-----------------------------------------------------------------------------------

	Theme Name: Seiko HTML5 eCommerce Template
	Author: BigSteps
	Author URI: http://themeforest.net/user/bigsteps
	Version: 1.2.0

-----------------------------------------------------------------------------------*/

$(function () {

	"use strict";
  
	var $body = $('body'),
		$window = $(window),
		$document = $(document);

	// detect touch
	var isTouchDevice = 'ontouchstart' in window || navigator.msMaxTouchPoints;
	if (isTouchDevice) {
		$body.addClass('touch');
	}
	// detect Mac
	if (navigator.userAgent.indexOf('Mac') > 0) {
		$body.addClass('mac');
	}
	// detect IE
	var version = detectIE();
	if (version) {
		$body.addClass('ie');
	}

	function detectIE() {
		var ua = window.navigator.userAgent;
		var msie = ua.indexOf('MSIE ');
		if (msie > 0) {
			// IE 10 or older => return version number
			return parseInt(ua.substring(msie + 5, ua.indexOf('.', msie)), 10);
		}
		var trident = ua.indexOf('Trident/');
		if (trident > 0) {
			// IE 11 => return version number
			var rv = ua.indexOf('rv:');
			return parseInt(ua.substring(rv + 3, ua.indexOf('.', rv)), 10);
		}
		var edge = ua.indexOf('Edge/');
		if (edge > 0) {
			// Edge (IE 12+) => return version number
			return parseInt(ua.substring(edge + 5, ua.indexOf('.', edge)), 10);
		}
		// other browser
		return false;
	}

	// disable scroll function
	function preventDefault(e) {
		e = e || window.event;
		if (e.preventDefault) e.preventDefault();
		e.returnValue = false;
	}

	function wheel(e) {
		preventDefault(e);
	}

	function disableScroll() {
		if (window.addEventListener) {
			window.addEventListener('DOMMouseScroll', wheel, false);
		}
		window.onmousewheel = document.onmousewheel = wheel;
	}

	function enableScroll() {
		if (window.removeEventListener) {
			window.removeEventListener('DOMMouseScroll', wheel, false);
		}
		window.onmousewheel = document.onmousewheel = null;
	}
	// END disable scroll function

	// price slider
	function priceSlider() {

		var priceSlider = document.getElementById('priceSlider');

		noUiSlider.create(priceSlider, {
			start: [200, 1500],
			connect: true,
			step: 1,
			range: {
				'min': 0,
				'max': 2000
			}
		});

		var inputPriceMax = document.getElementById('priceMax');
		var inputPriceMin = document.getElementById('priceMin');

		priceSlider.noUiSlider.on('update', function (values, handle) {

			var value = values[handle];

			if (handle) {
				inputPriceMax.innerHTML = value;
			} else {
				inputPriceMin.innerHTML = value;
			}
		});

	}

	// create image gallery for product page
	function productImageGallery() {
		var galleryObj = [];

		function createImageGallery() {
			$('.product-previews-carousel img').each(function () {
				var src = $(this).parent('a').data('zoom-image'),
					type = 'image'; // it's always an image
				var image = {};
				image["src"] = src;
				image["type"] = type;
				galleryObj.push(image);
			});
		}

		createImageGallery();

		function getActiveIndex() {
			var current = 0;
			if ($('.product-previews-carousel a.active').length) {
				current = $('.product-previews-carousel a.active').index();
			}
			return current;
		}

		if ($('.zoom-link').length) {
			$('.zoom-link').on('click', function (e) {
				if ($(this).is('.disable-gallery')) {
					var msrc = $('.main-image img').attr('data-zoom-image');
					$.magnificPopup.open({
						items: {
							src: msrc
						},
						type: 'image'
					});
				} else {
					getActiveIndex();
					$.magnificPopup.open({
						items: galleryObj,
						gallery: {
							enabled: true,
						}
					}, getActiveIndex());
				}
				e.preventDefault();
			});
		}

	}

	// simple gallery
	$.fn.simpleFilters = function () {

		var $gallery = this,
			$galleryitem = $(".gallery-item", $gallery),
			$filter = $(".filters-gallery .filter-label"),
			selectedCategory = "",
			activeStart;

		$filter.each(function () {
			selectedCategory = $(this).attr("data-filter");
			if ($(this).hasClass('active')) {
				$galleryitem.filter(selectedCategory).fadeIn(0).addClass('isvisible');
				activeStart = true;
			} else {
				$galleryitem.fadeIn(0).addClass('isvisible');
			}
		});

		if (!activeStart) $(".filters-gallery li:first-child .filter-label").addClass('active');

		$filter.on('click', function (e) {
			e.preventDefault();
			if ($(this).hasClass('active')) {
				return false;
			} else {
				$filter.removeClass('active');
				$(this).addClass('active')
			}
			selectedCategory = $(this).attr("data-filter");
			if (!selectedCategory) {
				$galleryitem.fadeIn(0).addClass('isvisible');

			} else {
				$galleryitem.filter(':not(' + selectedCategory + ')').fadeOut(0).removeClass('isvisible');
				$galleryitem.filter(selectedCategory).fadeIn(0).addClass('isvisible');
			}
		});
	}

	// back to top button
	function backToTop(button) {
		var $btn = $(button),
			windowH = $window.height();

		if ($btn.parent('.fixed-btns').length) {
			if (!$btn.parent('.fixed-btns').hasClass('demo-mode')) {
				$btn = $btn.parent('.fixed-btns');
			}
		}

		if ($(this).scrollTop() > windowH) {
			$btn.addClass('is-visible')
		}
		$window.scroll(function () {
			($(this).scrollTop() > windowH) ? $btn.addClass('is-visible'): $btn.removeClass('is-visible');
		});
		$btn.on('click', function () {
			$("html, body").animate({
				scrollTop: 0
			}, "slow");
			return false;
		});
	}


	// add to bookmark
	function addToBookmark(link) {
		var $link = $(link);
		var isBookmarked = document.cookie.replace(/(?:(?:^|.*;\s*)seikobookmark\s*\=\s*([^;]*).*$)|^.*$/, "$1");
		if (isBookmarked == 'yes') $link.hide();

		$link.on('click', function (e) {
			var bookmarkURL = window.location.href;
			var bookmarkTitle = document.title;
			if ('addToHomescreen' in window && addToHomescreen.isCompatible) {
				// Mobile browsers
				addToHomescreen({
					autostart: false,
					startDelay: 0
				}).show(true);
			} else if (window.sidebar && window.sidebar.addPanel) {
				// Firefox version < 23
				window.sidebar.addPanel(bookmarkTitle, bookmarkURL, '');
			} else if ((window.sidebar && /Firefox/i.test(navigator.userAgent)) || (window.opera && window.print)) {
				// Firefox 23+ and Opera version < 15
				$(this).attr({
					href: bookmarkURL,
					title: bookmarkTitle,
					rel: 'sidebar'
				}).off(e);
				return true;
			} else if (window.external && ('AddFavorite' in window.external)) {
				// IE Favorites
				window.external.AddFavorite(bookmarkURL, bookmarkTitle);
			} else {
				// Other browsers (mainly WebKit & Blink - Safari, Chrome, Opera 15+)
				alert('Press ' + (/Mac/i.test(navigator.userAgent) ? 'Cmd' : 'Ctrl') + '+D to bookmark this page.');
			}
			document.cookie = 'seikobookmark=yes';
			return false;
		});
	}
	
	// quickView
	function quickView(quickviewlink, modal) {
		var quickviewlink = quickviewlink,
			$modal = $(modal),
			$loader = $('.modalLoader-wrapper', $modal),
			$iframe = $('iframe', $modal),
			windowWidth = $window.width();

		$document.on('click.quickView', quickviewlink, function (e) {
			if (windowWidth > 1199 && !$body.hasClass('touch')) {
				var $this = $(e.target),
					src = $this.attr("href") ? $this.attr("href") : $this.closest('a').attr("href");

				$this.closest('.product-item').addClass('hover');

				$iframe.on('load', function () {
					if ($modal.data('bs.modal')) {
						setTimeout(function () {
							$loader.css({
								'display': 'none'
							});
						}, 500);
						$iframe.animate({
							'opacity': '1'
						}, 300);
					}
				});

				$modal.on('shown.bs.modal', function (e) {
					$('.modal-content', $modal).attr({
						'src': src
					});
					$('iframe', $modal).attr({
						'src': src
					});
				}).on('hidden.bs.modal', function (e) {
					var $this = $(this);
					$this.removeData('bs.modal');
					// clear iframe
					$iframe.empty().attr({
						'src': 'about:blank'
					}).css({
						'opacity': '0'
					});
					$loader.css({
						'display': 'block'
					});
					$('.product-item').removeClass('hover');
				})
				$modal.modal('show');
				e.preventDefault();
			}
		})

	}

	// product page form

	function productOptions(option) {
		var $option = $(option),
			$optionlist = $('ul', $option),
			$optionbtn = $('a', $optionlist),
			$optionselect = $('select', $option);
		$optionlist.find("a[data-value='" + $optionselect.val() + "']").parent().addClass('active');
		$optionbtn.on('click', function (e) {
			$this = $(this);
			if ($this.data('image')) {
				var $image = $('.main-image img');
				var imgSrc = $this.data('image');
				var newImg = document.createElement("img");
				newImg.src = imgSrc;
				newImg.onload = function () {
					$image.attr('src', imgSrc);
					$image.attr('data-zoom-image', imgSrc);
					if ($('.main-image > .zoom').length) {
						$('.main-image > .zoom').data('ezPlus').destroy();
						$('.main-image > .zoom').initProductZoom();
						$('.zoom-link').addClass('disable-gallery');
					}
				}
			}

			if (!$this.parent('li').is('.active')) {
				$optionselect.val($this.attr('data-value'));
				$this.closest('ul').find('li').removeClass('active');
				$this.parent('li').addClass('active');
			}
			e.preventDefault();
		});
	}


	// department button	
	function departmentMenu() {
		var $megamenu = $('.megamenu.department'),
			$departmentbtn = $('.nav-department'),
			$departmentdrop = $('.megamenu.department .nav'),
			slidespeed = 300;

		function closeDepartment() {
			$megamenu.removeClass('opened').css({
				'max-height': '0',
				'overflow': ''
			});
			$("#wrapper").removeClass('overlay');
		}

		if ($body.hasClass('touch')) {
			$departmentbtn.on("click.department", function (e) {
				if (!$megamenu.hasClass('opened')) {
					$megamenu.addClass('opened').css({
						'max-height': $departmentdrop.outerHeight() + 'px'
					});
					if ($megamenu.hasClass('blackout')) {
						$("#wrapper").addClass('overlay');
					}
				} else {
					closeDepartment();
				}
			})
			$departmentdrop.on("click.department", function (e) {
				$megamenu.addClass('opened').css({
					'max-height': $departmentdrop.outerHeight() + 'px',
					'overflow': 'visible'
				});
				if (!$("#wrapper").hasClass('overlay') && $megamenu.hasClass('blackout')) {
					$("#wrapper").addClass('overlay')
				}
			})
			$('#wrapper').on('click.department', function (e) {
				if (!$(e.target).hasClass('nav-department')) {
					if ($megamenu.hasClass('opened')) {
						closeDepartment();
					}
				}

			});
			$megamenu.on('click.department', function (e) {
				if ($(e.target).hasClass('department')) {
					if ($megamenu.hasClass('opened')) {
						closeDepartment();
					}
				}
			});
		} else {
			$departmentbtn.on({
				mouseenter: function () {
					$megamenu.addClass('opened').css({
						'max-height': $departmentdrop.outerHeight() + 'px'
					});
					if ($megamenu.hasClass('blackout')) {
						$("#wrapper").addClass('overlay');
					}
				},
				mouseleave: function () {
					$megamenu.removeClass('opened').css({
						'max-height': '0'
					});
					$("#wrapper").removeClass('overlay');
				}
			})
			$departmentdrop.on({
				mouseenter: function () {
					$megamenu.addClass('opened').css({
						'max-height': $departmentdrop.outerHeight() + 'px',
						'overflow': 'visible'
					});
					if (!$("#wrapper").hasClass('overlay') && $megamenu.hasClass('blackout')) {
						$("#wrapper").addClass('overlay')
					}
				},
				mouseleave: function () {
					$megamenu.removeClass('opened').css({
						'max-height': '0',
						'overflow': ''
					});
					$("#wrapper").removeClass('overlay');
				}
			})
		}
	}


	// tabs
	function productTab(tab) {
		var $tabs = $(tab),
			setCurrent = false;
		$tabs.tabCollapse();
		$('a', $tabs).each(function () {
			$this = $(this);
			if ($this.parent('li').is('.active')) {
				var curTab = $this.attr("href");
				$(curTab).addClass('active');
				setCurrent = true;
			}
		})
		if (!setCurrent) $('li:first-child a', $tabs).tab('show');
		$('a', $tabs).on('click', function (e) {
			var $this = $(this);
			if ($this.parent('.panel-title').length) {
				var href = $this.attr('href'),
					posTab = $this.offset().top - $window.scrollTop();
				setTimeout(function () {
					$('html, body').animate({
						scrollTop: $this.offset().top - posTab
					}, 0);
				}, 0);
				e.preventDefault();
			}
		});
	}

	// product next/prev preview on touch
	function prevnextNav(productnav) {
		var $productnav = $(productnav);
		if ($body.hasClass('touch')) {
			$('> a', $productnav).on("click", function (e) {
				var $this = $(this);
				if (!$this.data('firstclick')) {
					$('> a', $productnav).removeData('firstclick', true);
					$this.data('firstclick', true);
					e.preventDefault();
				}
			}).on("mouseleave", function (e) {
				$('> a', $productnav).removeData('firstclick', true);
			})
		}
	}

	// product view mode
	function viewMode(viewmode) {
		var $grid = $('.grid-view', $(viewmode)),
			$list = $('.list-view', $(viewmode)),
			$products = $('.products-listview, .products-grid');
		if ($('.products-listview').length) {
			$list.addClass('active');
		} else if ($('.products-grid').length) {
			$grid.addClass('active');
		} else return false;
		$grid.on("click", function (e) {
			var $this = $(this);
			$products.addClass('no-animate');
			if (!$this.is('.active')) {
				$list.removeClass('active');
				$this.addClass('active');
				$products.removeClass('products-listview').addClass('products-grid');
			}
			setTimeout(function () {
				$products.removeClass('no-animate');
			}, 500);
			e.preventDefault();
		});
		$list.on("click", function (e) {
			var $this = $(this);
			$products.addClass('no-animate');
			if (!$this.is('.active')) {
				$grid.removeClass('active');
				$this.addClass('active');
				$products.removeClass('products-grid').addClass('products-listview');
			}
			setTimeout(function () {
				$products.removeClass('no-animate');
			}, 500);
			e.preventDefault();
		});
	}

	// tooltip ini
	function tooltipIni() {
		var title;
		$('[data-tooltip]').darkTooltip({
			size: 'small',
			animation: 'fade'
		}).on("mouseenter", function () {
			title = $(this).attr('title');
			$(this).attr('title', '');
		}).on("mouseleave", function () {
			$(this).attr('title', title);
		});
	}

	// icrease/decrease input
	function changeInput() {

		$document.on('click', '.decrease', function (e) {
			var input_el = $(e.target).next('input');
			var v = input_el.val() - 1;
			if (input_el.attr('data-min')) {
				if (v >= input_el.attr('data-min')) input_el.val(v)
			} else {
				input_el.val(v)
			}
			e.preventDefault();
		});

		$document.on('click', '.increase', function (e) {
			var input_el = $(e.target).prev('input');
			var v = input_el.val() * 1 + 1;
			if (input_el.attr('data-max')) {
				if (v <= input_el.attr('data-max')) input_el.val(v)
			} else {
				input_el.val(v)
			}
			e.preventDefault();
		});

	}

	// fullheight page set
	function setFullHeight() {

		if ($('.push-footer').length) $('.push-footer').remove();
		if ($(".block.fullheight").length) {
			$(".block.fullheight").css('height', '');
		}

		var $wrapper = $("body"),
			$footer = $('.page-footer'),
			$content = $(".page-main"),
			footerH = $footer.length ? $footer.height() : 0,
			offsetTop = $content.length ? $content.offset().top : 0,
			wHeight = Math.max($wrapper.height() - footerH - offsetTop, $(".block.fullheight").outerHeight());

		if ($(".block.fullheight").length) {
			$wrapper.css({
				'overflow-y': 'scroll'
			});
			$(".block.fullheight").css('height', wHeight + 'px');
		}

		var footerH = $footer.length ? $footer.outerHeight() : 0,
			footerTop = $footer.length ? $footer.offset().top : 0,
			footerPush = $window.height() - footerH - footerTop;
		if (footerPush > 0) {
			$footer.before('<div class="push-footer"></div>');
			$('.push-footer').css({
				'height': footerPush + 'px'
			});
		}
	}

	// fullwidth page set
	function setFullWidth() {

		var wWidth = $("body").width() - $('.sidebar-wrapper').width();

		$('body:not(.fullwidth) .fullwidth, body:not(fullwidth) .fullboxed, body .boxed').each(function () {
			$(this).css({
				'width': '',
				'margin-left': '',
				'margin-right': ''
			});
		});

		if ($body.hasClass('rtl')) {
			$('body:not(.fullwidth) .fullwidth, body:not(.fullwidth) .fullboxed').each(function () {
				$(this).css({
					'width': wWidth + 'px',
					'margin-right': -wWidth / 2 + 'px',
					'margin-left': ''
				});
			});
		} else {
			$('body:not(.fullwidth) .fullwidth, body:not(.fullwidth) .fullboxed').each(function () {
				$(this).css({
					'width': wWidth + 'px',
					'margin-left': -wWidth / 2 + 'px',
					'margin-right': ''
				});
			});
		}

	}

	// resize events
	$.fn.otherResize = function () {
		setFullWidth();
		if ($(".product-lookbook").length) {
			$('.product-lookbook').lookbookSize();
		}
		if ($(".filter-col.fixed").length) {
			$(".filter-col.fixed").fixedSidebar();
		}
		if ($('.mainSlider').length) {
			$('.mainSlider').swiperUpdate();
		}
		if ($('.gallery.isotope').length) {
			$('.gallery').isotope('layout');
		}
		if ($('.products-grid.isotope').length) {
			$('.products-grid.isotope').isotope('layout');
		}
		if ($(".autosize-text").length) {
			$(".autosize-text").each(function () {
				$this = $(this);
        var fontratio = Math.round($this.attr("data-fontratio")*100)/100;
        if(fontratio > 0) { 
          $this.flowtype({
            fontRatio: fontratio
          });
        }
			});
		}
		setTimeout(function () {
			$('.slick-initialized').slick('setPosition');
		}, 100);
		if ($(".main-image").length) {
			$('.main-image .zoomContainer').remove();
		}
		if ($(".product-creative-slider").length) {
			$('.product-slider-wrapper .zoomContainer').remove();
			setTimeout(function () {
				$('.product-creative-slider .inner-zoom').initCreativeZoom();
			}, 100);
		}
	}

	// slide panel
	function slidePanel() {
		var button = ".slidepanel-toggle",
			$wrapper = $("body");
		$wrapper.on('click', button, function (e) {
			if ($('#toolsPanel').length) {
				$("input[name='slidepanelshow']", $('#toolsPanel')).trigger('click');
			} else $wrapper.toggleClass("open-panel");
			setTimeout(function () {
				$('.slick-initialized').slick('setPosition');
			}, 500);
			$body.otherResize();
			e.preventDefault();
		});
	}

	// collapsed footer block
	$.fn.footerCollapse = function () {
		var $collapsed = this;
		$('.title', $collapsed).on('click', function (e) {
			e.preventDefault;
			$(this).closest('.collapsed-mobile').toggleClass('open');
		})
	}
	
	// select marked category
	$.fn.blockSelectedMark = function () {
		var $block = this;

		function markSelected(block) {
			var $this = block;
			if ($this.find('li.active').length) {
				$this.addClass('selected');
			} else {
				$this.removeClass('selected');
			}
		}
		$block.each(function () {
			markSelected($(this));
		})
		$('li > a', $block).unbind('click.blockSelectedMark');
		$('li > a', $block).on('click.blockSelectedMark', function (e) {
			if ($('.filter-col').hasClass('no-ajax-filter')) return;
			var $this = $(this);
			e.preventDefault();
			$this.parent().toggleClass('active');
			markSelected($this.closest('.sidebar-block'));
		})
	}
	
	// hide shop by if no selected filters
	$.fn.hideShopBy = function () {
		var $content = this,
			$filters = $('.selected-filters', $content);
		if (!$filters.length || $filters.html().trim() === "") $content.closest('.sidebar-block-top').hide();
	}
	
	// collapse filters block
	$.fn.blockCollapse = function () {
		var $collapsed = this,
			slidespeed = 250;

		$('.block-content', $collapsed).each(function () {
			if ($(this).parent().is('.open')) {
				$(this).slideDown(0);
			}
		})
		$('.block-title').unbind('click.blockCollapse');
		$('.block-title', $collapsed).on('click.blockCollapse', function (e) {
			e.preventDefault;
			var $this = $(this),
				$thiscontent = $this.next('.block-content');
			if ($this.parent().is('.open')) {
				$this.parent().removeClass('open');
				$thiscontent.slideUp(slidespeed);
			} else {
				$this.parent().addClass('open');
				$thiscontent.slideDown(slidespeed);
			}
		})
	}
	
	// collapse filters block as accordion for fixed sidebar
	$.fn.blockCollapseAccordion = function () {
		var $collapsed = this,
			slidespeed = 250;
		$('.block-content', $collapsed).each(function () {
			if ($(this).parent().is('.open')) {
				$(this).slideDown(0);
			}
		})
		$('.block-title').unbind('click.blockCollapseAccordion');
		$('.block-title', $collapsed).on('click.blockCollapseAccordion', function (e) {
			e.preventDefault;
			var $this = $(this),
				$thiscontent = $this.next('.block-content');
			if ($this.parent().is('.open')) {
				$this.parent().removeClass('open');
				$thiscontent.slideUp(slidespeed);
			} else {
				$this.closest('.filter-col-content').find('.sidebar-block.collapsed').removeClass('open');
				$this.closest('.filter-col-content').find('.sidebar-block.collapsed .block-content').slideUp(slidespeed);
				$this.parent().addClass('open');
				$thiscontent.slideDown(slidespeed);
			}
			setTimeout(function () {
				$(".filter-col.fixed").fixedSidebar();
			}, slidespeed);
		})
	}
	
	// fixed sidebar
	$.fn.fixedSidebar = function () {
		var $sidebar = this,
			$container = $('.filter-container'),
			$sidebarscroll = $('.fixed-scroll', $sidebar);
		// fixed markers
		var $ymin = $sidebar,
			$ymax = $('.ymax'),
			$fstart = $('.fstart'),
			$fend = $('.fend'),
			delta = 10;

		function checkFixed() {
			var scrollY = $window.scrollTop();
			if (!$sidebar.is('.is-fixed')) {
				if (scrollY > $ymin.offset().top) {
					if ($fend.offset().top < $ymax.offset().top - delta) {
						$sidebar.addClass('is-fixed');
						if ($fend.offset().top > $ymax.offset().top) {
							$sidebar.addClass('is-fixed-bottom');
						}
					}
				}
			} else {
				if (scrollY > $ymin.offset().top) {
					if ($fend.offset().top > $ymax.offset().top) {
						$sidebar.addClass('is-fixed-bottom');
					} else {
						if (scrollY < $fstart.offset().top) {
							$sidebar.removeClass('is-fixed-bottom');
						}
					}
				} else $sidebar.removeClass('is-fixed is-fixed-bottom');
			}

			if ($container.data('hidden')) {
				$container.animate({
					'opacity': '1'
				}, 1000).removeData('hidden');
			}
		}

		function iniFixedSidebar() {
			if ($window.scrollTop() > $ymin.offset().top && !$body.data('checkstart')) {
				$container.data('hidden', true).css({
					'opacity': '0'
				});
				$body.data('checkstart', true);
			} else $body.data('checkstart', true);
			$window.unbind('scroll.fixedsidebar');
			$sidebar.removeClass('is-fixed is-fixed-bottom');
			$container.css({
				'left': '',
				'width': ''
			});
			var windowWidth = $window.width(),
				windowHeight = $window.height();
			if (windowWidth > 991) {
				$sidebarscroll.css({
					'max-height': windowHeight + 'px'
				});
				$container.css({
					'left': $container.offset().left + 'px',
					'width': $container.width() + 'px'
				});
				if (($ymax.offset().top - $fend.offset().top) > 50) {
					$window.on('scroll.fixedsidebar', function (e) {
						checkFixed();
					})
				}
				checkFixed();
			}
		}
		if (!$body.hasClass('touch')) {
			iniFixedSidebar();
			$window.scroll();
			$window.on('resize.fixedsidebar', function () {
				setTimeout(function () {
					iniFixedSidebar();
				}, 2000);
			});
			// hide tooltips on scroll
			$sidebarscroll.on('scroll', function () {
				$('.dark-tooltip').hide();
			})
			$window.on('scroll', function () {
				$('.dark-tooltip').hide();
			})
		}
	}

	// check if filters are in the page
	$.fn.isFilters = function () {
		var $filtercol = this,
			$filtercontent = $('.filter-col-content', this),
			$centercol = $filtercol.next('.aside');
		if (!$filtercol.is(":visible")) $filtercol.show();
		$centercol.css({
			'width': '',
			'float': ''
		});
		if (!$filtercontent.find('.sidebar-block').length) {
			$filtercol.hide();
			$centercol.css({
				'width': '100%',
				'float': 'none'
			});
		}
	}
	
	// mobile slide filters
	$.fn.mobileFilter = function () {
		var $mobilefilter = this,
			$toggleFilter = '.filter-col-toggle';

		$document.on('click', $toggleFilter, function (e) {
			$mobilefilter.toggleClass('active');
			$body.toggleClass('fixed');
			e.preventDefault();
		})

		$document.on('click', '.filter-col', function (e) {
			if ($(e.target).hasClass('active')) {
				$mobilefilter.removeClass('active');
				$body.removeClass('fixed');
				e.preventDefault();
			}
		})
	}

	// mobile menu
	$.fn.mobileMenu = function () {

		var $mobilemenu = $(this),
			$toggleMenu = $('.mobilemenu-toggle'),
			$mobileCaret = $('ul.nav li .arrow', $mobilemenu),
			$mobileLink = $('ul.nav li > a', $mobilemenu);

		$toggleMenu.on('click.mobileMenu', function () {
			$mobilemenu.toggleClass('active');
			$body.toggleClass('fixed');
			return false;
		});
		$mobilemenu.on('click.mobileMenu', function (e) {
			if ($(e.target).is($mobilemenu)) {
				$mobilemenu.toggleClass('active');
				$body.toggleClass('fixed');
				e.preventDefault();
			}
		});

		function mobileEvent() {
			$mobileCaret.on('click.mobileMenu', function (e) {
				e.preventDefault();
				var $parent = $(this).parent();
				if ($parent.hasClass('submenu-open')) {
					$('li.submenu-open ul', $parent).slideUp(200);
					$('li', $parent).removeClass('submenu-open');
					$parent.removeClass('submenu-open');
					$('> ul', $parent).slideUp(200);
					$parent.removeData('firstclick');
				} else {
					$parent.addClass('submenu-open');
					$(' > ul', $parent).slideDown(200);
					$parent.data('firstclick', true);
				}
			});
			if ($mobilemenu.hasClass('dblclick')) {
				$mobileLink.on('click.mobileMenu', function (e) {
					e.preventDefault();
					var $parent = $(this).parent();
					if (!$parent.data('firstclick') && $parent.find('ul').length) {
						$parent.addClass('submenu-open');
						$(' > ul', $parent).slideDown(200);
						$parent.data('firstclick', true);
					} else {
						var href = $(this).attr("href"),
							target = $(this).attr("target") ? $(this).attr("target") : '_self';
						window.open(href, target);
						$parent.removeData('firstclick');
					}
				});
			}
		}

		var windowWidth = $window.width();

		if (windowWidth < 992) {
			mobileEvent();
		}

		var prevWindow = windowWidth;

		$window.on('resize', function () {  
			var currentWindow = window.innerWidth || $window.width();
			if (currentWindow != prevWindow) {   


			setTimeout(function () {
            $mobileLink.unbind('click.mobileMenu');
            $mobileCaret.unbind('click.mobileMenu');
        		if (currentWindow > 991) {
						$body.removeClass('fixed');
						$mobilemenu.removeClass('active');
					} else mobileEvent();
				}, 500);
				prevWindow = currentWindow;
			}
		});
	}

	// minicart	- variant-1
	$.fn.mobileMinicart = function () {

		var $mobilecart = $(this),
			$toggleCart = $('> a', $mobilecart),
			$closeCart = $('.block-title', $mobilecart),
			$dropdown = $('.dropdown-container', $mobilecart);

		function eventsIni() {
			var windowWidth = $window.width();

			if (windowWidth < 992) {
				if (!$mobilecart.data('mobile')) {
					$toggleCart.on('click.mobileMinicart', function (e) {
						$mobilecart.toggleClass('active');
						$body.toggleClass('fixed');
						return false;
					});
					$closeCart.on('click.mobileMinicart', function (e) {
						$mobilecart.removeClass('active');
						$body.removeClass('fixed');
						return false;
					});
					$mobilecart.on('click.mobileMinicart', function (e) {
						if ($(e.target).is($dropdown)) {
							$mobilecart.removeClass('active');
							$body.removeClass('fixed');
							e.preventDefault();
						}
					});
					$mobilecart.data('mobile', true);
				}
			} else {
				$toggleCart.unbind('click.mobileMinicart');
				$closeCart.unbind('click.mobileMinicart');
				$mobilecart.unbind('click.mobileMinicart').removeClass('active');
				$body.removeClass('fixed');
				$mobilecart.removeData('mobile');
			}
		}
		eventsIni();

		$window.on('resize', function () {
			setTimeout(function () {
				eventsIni();
			}, 500);
		});
	}

	// minicart - variant-2
	$.fn.mobileMinicartAlt = function () {  
		var $mobilecart = this,
			$mobilecartscroll = $('.block-minicart', $mobilecart),
			$toggleCart = $('> a', $mobilecart),
			$closeCart = $('.btn-minicart-close', $mobilecart),
			$dropdown = $('.dropdown-container', $mobilecart),
			wHeight = $window.height(),
			$menu = $('.megamenu'),
			$header = $('.page-header');

		var windowWidth = $window.width();

		// Minicart Max Height
		function setMaxHeight(wHeight) {
			var cartH;
			var windowWidth = $window.width();
			if (windowWidth < 992) {
				$dropdown.scrollTop(0);
				if ($header.hasClass('variant-3')) cartH = $window.height() - $header.height();
				else if (!$header.hasClass('is-sticky')) cartH = $window.height() - $toggleCart.offset().top - $toggleCart.height();
				else cartH = $window.height() - $header.height();
			} else {
				cartH = Math.min($window.height() - $header.height(), $mobilecartscroll[0].scrollHeight);
			}
			$dropdown.css({
				'max-height': cartH + 'px'
			});
			$mobilecartscroll.css({
				'max-height': cartH + 'px'
			});
		}

		function eventsIni(wHeight) {  
			if (windowWidth < 992) {
				if (!$mobilecart.data('mobile')) {
				$mobilecartscroll.scrollLock('disable');
				$mobilecart.unbind('.mobileMinicart');
        $toggleCart.unbind('.mobileMinicart');

				$toggleCart.on('click.mobileMinicart', function (e) {
					if ($mobilecart.hasClass('active')) {
						$dropdown.css({
							'max-height': '0'
						});
						$mobilecartscroll.css({
							'max-height': '0'
						});
						$mobilecart.removeClass('active');
						$header.data('cartopen', false);
						return false;
					} else {
						setMaxHeight($window.height());
						$mobilecart.addClass('active');
						$header.data('cartopen', true);
						return false;
					}
				});
				$closeCart.on('click.mobileMinicart', function (e) {
					$dropdown.css({
						'max-height': '0'
					});
					$mobilecartscroll.css({
						'max-height': '0'
					});
					$mobilecart.removeClass('active');
					$header.data('cartopen', false);
					return false;
				});
        $mobilecart.data('mobile', true)
        }
			} else {
				$mobilecartscroll.scrollLock();
				$toggleCart.unbind('click.mobileMinicart');
				$closeCart.unbind('click.mobileMinicart');
				$mobilecart.unbind('click.mobileMinicart');
				$mobilecart.on("mouseenter.mobileMinicart", function () {
					$mobilecartscroll.scrollTop(0);
					$mobilecart.data('open', true);
					setMaxHeight($window.height());
					$header.data('cartopen', true);
				}).on("mouseleave.mobileMinicart", function () {
					$dropdown.css({
						'max-height': ''
					});
					$mobilecartscroll.css({
						'max-height': '0'
					});
					$header.data('cartopen', false);
				});
        $mobilecart.removeData('mobile');
			}
		}

		eventsIni();

		$window.on('resize', function () {
			$mobilecart.removeData('setHeight');
			eventsIni();
		});
	}

	$.fn.expandingSearch = function () {
		var $searchBox = this,
			$submitIcon = $('.exp-icon-search', $searchBox),
			$submitInput = $('.exp-search-input', $searchBox),
			$closeIcon = $('.exp-search-close', $searchBox),
			$navbar = $('.navbar'),
			$menu = $('.megamenu', $navbar),
			isOpen = false,
			$header = $('.page-header'),
			$menu = $('.megamenu', $header);


		$submitIcon.on('click', function (e) {
			if ($menu.css('display') == 'none' || $header.hasClass('variant-7') || $header.hasClass('variant-8')) {
				$(this).closest('form').submit();
			} else {
				if (isOpen == false) {
					$searchBox.addClass('exp-search-open');
					if (!($menu.css('display') == 'none')) {
						var inputW = $searchBox.offset().left - $menu.offset().left + 40
							// for desktop open input until menu start
						if ($body.hasClass('rtl')) {
							inputW = ($menu.offset().left + $menu.width()) - $searchBox.offset().left;
						}
						$searchBox.css({
							'width': inputW + 'px'
						})
					}
					$submitInput.focus();
					$menu.addClass('unvisible');
					isOpen = true;
				} else {
					$(this).closest('form').submit();
				}
			}
		});

		$closeIcon.on('click', function (e) {
			$submitInput.val('');
			$searchBox.removeClass('exp-search-open').css({
				'width': ''
			});
			$menu.removeClass('unvisible');
			isOpen = false;
		});
	}

	// product sharing animation
	function productSharing() {
		var link = 'a.sharing',
			leave = '.product-item-inside, .product-item-inside .social-list';
		$document.on('click', link, function (e) {
			var $el = $(this);
			$el.closest('.product-item').addClass('sharing');
			e.preventDefault();
		})
		$document.on('mouseleave', leave, function (e) {
			var $el = $(this);
			$el.closest('.product-item').removeClass('sharing');
		})
	}
	
	// colorswatch
	function colorSwatch(link) {
		var link = link + ' a';
		$document.on('click', link, function (e) {
			var $el = $(this);
			if ($el.data('image')) {
				var $image = $el.closest('.product-item-inside').find('img.product-image-photo');
				// if inner carousel in product
				if ($el.closest('.product-item-inside').find('.carousel-inside').length) {
					$el.closest('.product-item-inside').find('.carousel-inside').carousel(0);
					$image = $el.closest('.product-item-inside').find('.product-item-photo .item:first-child img');
				}
				var imgSrc = $el.data('image');
				$el.closest('ul.color-swatch').find('li').removeClass('active');
				$el.parent('li').addClass('active');
				var newImg = document.createElement("img");
				newImg.src = $el.data('image');
				newImg.onload = function () {
					$image.attr('src', $el.data('image'))
				}
			}
			e.preventDefault();
		})
	}

	// product stack
	$.fn.ProductStack = function (productstack) {
		var $productstack = this,
			$toggleStack = $(".toggleStack", $productstack),
			$editbtn = $(".action.edit", $productstack),
			$product = $(".products-list li", $productstack);


		$toggleStack.on('click', function (e) {
			$('.productStack').toggleClass('open');
			e.preventDefault();
		})

		$product.on('mouseleave', function (e) {
			var $this = $(this);
			setTimeout(function () {
				$this.find('.actions').removeClass('open');
			}, 200);
		});

		$productstack.on('click', 'a.action.edit', function (e) {
			$('.actions', $(this).closest('li')).toggleClass('open');
			e.preventDefault();
		});

		$window.on('scroll.ProductStack', function () {
			if ($productstack.hasClass('open') && $productstack.hasClass('hide_on_scroll')) {
				$productstack.removeClass('open');
			}
		})
	}

	// fly to cart
	$.fn.FlyToCart = function (options) {

		var options = $.extend($.fn.FlyToCart.defaults, options);
		var $productstack = $(options.productstack);

		$document.on('click.FlyToCart', options.link, function (e) {

			var $el = $(this),
				$flyImg;

			disableScroll();

			var $cart = $('.toggleStack .icon', $productstack),
				cartY = $cart.offset().top + 60,
				cartX = $cart.offset().left + 20;

			if ($productstack.hasClass('disable')) {
				$productstack.removeClass('disable');
				cartY = cartY - 50;
			}
			if (!$productstack.hasClass('open')) {
				$productstack.addClass('open');
				cartY = cartY - $productstack.height();
			} else cartY = cartY - 50;

			if ($el.closest('.product-item-inside').find('.carousel-inside').length) {
				$flyImg = $el.closest('.product-item-inside').find('.product-item-photo .item.active img.product-image-photo');
			} else $flyImg = $el.closest('.product-item-inside').find('img.product-image-photo');

			if ($flyImg) {
				var $cloneImg = $flyImg.clone()
					.offset({
						top: $flyImg.offset().top,
						left: $flyImg.offset().left
					})
					.css({
						'opacity': '0.9',
						'position': 'absolute',
						'width': $flyImg.width(),
						'z-index': '10000'
					})
					.appendTo($body)
					.delay(300)
					.animate({
						'top': cartY,
						'left': cartX,
						'width': 100
					}, 800);

				setTimeout(function () {
					$cart.addClass('bounceIn animated').one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function () {
						$cart.removeClass('bounceIn animated');
						$cloneImg.detach();
					});
				}, 1500);

				$cloneImg.animate({
						'width': 0,
						'height': 0
					},
					300,
					function () {
						$.isFunction(options.complete) && options.complete.call($el);
						enableScroll()
					}
				);
			}
			e.preventDefault()
		});
	}
	$.fn.FlyToCart.defaults = {
		complete: null,
		link: null,
		productstack: null
	};

	// sticky header - hide when scroll down
	$.fn.stickyHeaderSmart = function () {

		var $header = this,
			$body = $('body'),
			$menu = $('.megamenu', $header),
			isScroll = false,
			lastScrollTop = 0,
			delta = 10,
			headerOffset,
			stickyH;

		function setHeigth() {
			$(".fix-space").remove();
			$header.removeClass('animated is-sticky st-visible slideInDown slideOutUp');
			$body.removeClass('hdr-sticky');
			headerOffset = $('.navbar', $header).offset().top;
			stickyH = $header.height() + headerOffset;
			if ($menu.css('display') == 'none' || $header.hasClass('variant-4') || $header.hasClass('variant-5') || $header.hasClass('variant-6') || $header.hasClass('variant-7') || $header.hasClass('variant-8') || $header.hasClass('variant-9')) {
				headerOffset = stickyH + 52;
			}
		}

		setHeigth();


		$window.on('scroll', function () {
			if (!isScroll) {
				isScroll = true;
				setTimeout(function () {
					hasScrolled();
					isScroll = false;
				}, 50)
			}
		});

		var prevWindow = window.innerWidth || $window.width()

		$window.on('resize', function () {
			var currentWindow = window.innerWidth || $window.width();
			if (currentWindow != prevWindow) {
				setHeigth()
				prevWindow = currentWindow;
			}
		});

		function hasScrolled() {
			if ($header.data('cartopen')) return;
			if ($header.hasClass('sticky')) {
				var st = getCurrentScroll();
				if (Math.abs(lastScrollTop - st) <= delta) return;

				if (st > lastScrollTop) {
					if (st > stickyH) {
						// Scroll Down
						if ($header.hasClass('st-visible')) {
							$header.removeClass('st-visible slideInDown').addClass('st-hidden animated slideOutUp');
							$("li.mega-dropdown,li.simple-dropdown", $header).removeClass('hovered');
							$("#wrapper").removeClass('overlay');
						} else {
							$header.addClass('is-sticky st-hidden');
							if (!$(".fix-space").length) {
								$header.after('<div class="fix-space">.</div>');
								$(".fix-space").css({
									'height': stickyH + 'px'
								});
								$("li.mega-dropdown,li.simple-dropdown", $header).removeClass('hovered');
								$("#wrapper").removeClass('overlay');
							}
						}
					}
					$body.removeClass('hdr-sticky');
				} else if (st < lastScrollTop) {
					if (st <= headerOffset) {
						// Scroll Up Start
						if ($header.hasClass('is-sticky')) {
							$(".fix-space").remove();
							$header.removeClass('animated is-sticky st-visible slideInDown slideOutUp');
							$body.removeClass('hdr-sticky');
						}
					} else {
						// Scroll Up
						$header.addClass('is-sticky');
						if (!$(".fix-space").length) {
							$header.after('<div class="fix-space">.</div>');
							$(".fix-space").css({
								'height': stickyH + 'px'
							});
							$("li.mega-dropdown,li.simple-dropdown", $header).removeClass('hovered');
							$("#wrapper").removeClass('overlay');
						}
						$header.removeClass('st-hidden slideOutUp').addClass('st-visible animated slideInDown');
						$body.addClass('hdr-sticky');
					}
				}
				lastScrollTop = st;
			}
		}

		function getCurrentScroll() {
			return window.pageYOffset || document.documentElement.scrollTop;
		}
	}

	// sticky header - always fixed
	$.fn.stickyHeader = function () {

		var $header = this,
			$body = $('body'),
			$menu = $('.megamenu', $header),
			headerOffset,
			stickyH;

		function setHeigth() {
			$(".fix-space").remove();
			$header.removeClass('animated is-sticky slideInDown');
			$body.removeClass('hdr-sticky');
			headerOffset = $('.navbar', $header).offset().top;
			stickyH = $header.height() + headerOffset;
			if ($menu.css('display') == 'none' || $header.hasClass('variant-4') || $header.hasClass('variant-5') || $header.hasClass('variant-6') || $header.hasClass('variant-7') || $header.hasClass('variant-8') || $header.hasClass('variant-9')) {
				headerOffset = stickyH + 52;
			}
		}

		setHeigth();

		var prevWindow = window.innerWidth || $window.width()

		$window.on('resize', function () {
			var currentWindow = window.innerWidth || $window.width();
			if (currentWindow != prevWindow) {
				setHeigth()
				prevWindow = currentWindow;
			}
		});

		$window.scroll(function () {
			if ($header.data('cartopen')) return;
			var st = getCurrentScroll();
			if (st > headerOffset) {
				if (!$(".fix-space").length) {
					$header.after('<div class="fix-space"></div>');
					$(".fix-space").css({
						'height': $header.height() + 'px'
					});
				}
				$header.addClass('is-sticky animated slideInDown');
				$body.addClass('hdr-sticky');
			} else {
				$(".fix-space").remove();
				$header.removeClass('animated is-sticky slideInDown');
				$body.removeClass('hdr-sticky');
			}
		});

		function getCurrentScroll() {
			return window.pageYOffset || document.documentElement.scrollTop;
		}
	}

	// truncated list megamenu
	function showHideLists(list) {
		var thisBtnsList = list; 
    var num = thisBtnsList.children().length;
    var numVis = thisBtnsList.closest('.truncateList').data('listItems');
    if (num > numVis) {
  		var showBtn = thisBtnsList.prev().find('.view-all');
      var bShowEm = showBtn.data('bShowEm') || false;
      showItems(thisBtnsList, bShowEm, numVis);
      bShowEm ^= true;
      showBtn.data('bShowEm', bShowEm);
      if (bShowEm) {
        showBtn.removeClass('disabled');
      } else {
        showBtn.addClass('disabled');

      }    
    } else {
      thisBtnsList.closest('.truncateList').find('.view-all').hide()
    }
	}

	function showItems(list, bShowAll, numVisible) {
		if (bShowAll) {
			list.find("> li:gt(" + (numVisible - 1) + ")").fadeIn(300);
		} else {
			list.find("> li:lt(" + numVisible + ")").show();
			list.find("> li:gt(" + (numVisible - 1) + ")").fadeOut(300);
		}

	}
	if ($('.truncateList').length) {
		$('.truncateList').each(function () {
			showHideLists($(this).find('ul.category-links'));
		})
		$('.truncateList .view-all').on('click', function (e) {
			showHideLists($(this).parent().next('ul.category-links'));
			e.preventDefault();
		})
	}
	// END truncated list megamenu

	// lookbook
	$.fn.lookbookSize = function () {
		this.each(function () {
			var $this = $(this),
				$photo = $this.find('.product-item-photo'),
				$photohover = $photo.find('a'),
				$info = $this.find('.product-item-info');
			$photo.css({
				'height': ''
			});
			$info.css({
				'height': ''
			});
			$this.removeData('setSize');
			$photohover.on('mouseenter', function (e) {
				var $this = $(this).closest('.product-lookbook').addClass('hovered');
				if (!$this.data('setSize')) {
					var $photo = $this.find('.product-item-photo'),
						$info = $this.find('.product-item-info');
					var maxH = Math.max($photo.outerHeight(), $info.outerHeight());
					$photo.css({
						'height': maxH + 'px'
					});
					$info.css({
						'height': maxH + 'px'
					});
					$this.data('setSize', true);
				}
			})
			$this.on('mouseleave', function (e) {
				$(this).removeClass('hovered');
			})
		})
		$('.lookbook-open', this).on('click', function (e) {
			var modalcontent = $(this).closest('.product-lookbook'),
				$modal = $('#modalLookbook'),
				$modalcontainer = $('.modal-body', $modal);
			$('.product-lookbook', $modal).remove();
			modalcontent.clone().appendTo($modalcontainer);
			$modal.modal('show');
		});
	}

	// banner hover color change
	$('.banner')
		.on('mouseenter', function () {
			$('[data-hcolor]:not(.banner-btn)', $(this)).each(function () {
				var color = $(this).attr("data-hcolor");
				$(this).find('span.text').css({
					'color': color
				});
			})
		})
		.on('mouseleave', function () {
			$('[data-hcolor]:not(.banner-btn)', $(this)).each(function () {
				$(this).find('span.text').css({
					'color': ''
				});
			})
		})

	// banner hover color change
	$('.banner-btn[data-hcolor]')
		.on('mouseenter', function () {
			var color = $(this).attr("data-hcolor");
			$(this).find('span.text').css({
				'color': color
			});
		})
		.on('mouseleave', function () {
			$(this).find('span.text').css({
				'color': ''
			});
		})

	// Modal Show
	if ($('#modal1').length) {
		var modal = $('#modal1');
		var pause = 0;
		if (modal.attr('data-pause') > 0) {
			pause = modal.attr('data-pause')
		}
		setTimeout(function () {
			modal.modal('show');
		}, pause);
	}

	// modal interval
	if ($('.modal-countdown').length) {
		var counter;
		$('.modal-countdown').on('hidden.bs.modal', function () {
			var $modal = $(this);
			if ($modal.attr('data-interval') > 0) {
				$('.count', $modal).html('').fadeOut();
				clearInterval(counter);
			}
		});
		$('.modal-countdown').on('shown.bs.modal', function () {
			var interval = 0,
				$modal = $(this);
			if ($modal.attr('data-interval') > 0) {
				interval = $modal.attr('data-interval')
			}
			var count = interval / 1000;
			if (count > 0) {
				$('.modal-countdown', $modal).show();
				$('.count', $modal).html(count).fadeIn();
				counter = setInterval(
					function modalCount() {
						if (count > 0) {
							count -= 1;
							$('.count', $modal).html(count);
						} else {
							$modal.modal('hide').removeData('bs.modal');
							clearInterval(counter)
						}
					}, 1000);
			}
		});
	}


	// timeout for resize event
	function debouncer(func, timeout) {
		var timeoutID, timeout = timeout || 500;
		return function () {
			var scope = this,
				args = arguments;
			clearTimeout(timeoutID);
			timeoutID = setTimeout(function () {
				func.apply(scope, Array.prototype.slice.call(args));
			}, timeout);
		}
	}

	//Carousel Inside
	$.fn.insideCarousel = function () {
		var $carousel = this,
			next = '.carousel-control.next',
			prev = '.carousel-control.prev';

		$carousel.carousel({
			interval: false
		})
		$document.on('click', next, function () {
			$(this).parent().carousel('next');
		});
		$document.on('click', prev, function () {
			$(this).parent('.carousel-inside').carousel('prev');
		});
	}

	// ini carousel via data params
	if($(".data-carousel").length) {
    $(".data-carousel").slick();   
  }

	// featured carousel
	if ($(".featured-products.products-carousel").length) {
		var $this = $(".featured-products.products-carousel"),
			arrowsplace = $this.prev('.title');
		$this.slick({
			rows: 1,
			appendArrows: arrowsplace,
			slidesToShow: 4,
			slidesToScroll: 4,
			speed: 500,
			infinite: false,
			swipe: false,
			responsive: [{
				breakpoint: 1401,
				settings: {
					slidesToShow: 3,
					slidesToScroll: 3
				}
            }, {
				breakpoint: 1201,
				settings: {
					slidesToShow: 3,
					slidesToScroll: 3
				}
            }, {
				breakpoint: 993,
				settings: {
					slidesToShow: 2,
					slidesToScroll: 2
				}
            }, {
				breakpoint: 769,
				settings: {
					slidesToShow: 2,
					slidesToScroll: 2
				}
            }, {
				breakpoint: 481,
				settings: {
					slidesToShow: 1,
					slidesToScroll: 1
				}
            }]
		});
	}

	// sale carousel
	if ($(".sale-products.products-carousel").length) {
		var $this = $(".sale-products.products-carousel"),
			arrowsplace = $this.prev('.title');
		$this.slick({
			rows: 2,
			slidesPerRow: 1,
			appendArrows: arrowsplace,
			slidesToShow: 3,
			slidesToScroll: 3,
			speed: 500,
			infinite: false,
			responsive: [{
				breakpoint: 1401,
				settings: {
					slidesToShow: 2,
					slidesToScroll: 2
				}
            }, {
				breakpoint: 1201,
				settings: {
					rows: 1,
					slidesPerRow: 1,
					slidesToShow: 2,
					slidesToScroll: 2
				}
            }, {
				breakpoint: 993,
				settings: {
					slidesToShow: 1,
					slidesToScroll: 1
				}
            }, {
				breakpoint: 769,
				settings: {
					slidesToShow: 1,
					slidesToScroll: 1
				}
            }, {
				breakpoint: 481,
				settings: {
					slidesToShow: 1,
					slidesToScroll: 1
				}
            }]
		});
	}

	// from blog carousel
	if ($(".blog-carousel").length) {
		var $this = $(".blog-carousel"),
			arrowsplace = $this;

		var $carouseltitle = $this.prev('.title');

		if ($this.parent().hasClass('collapsed-content')) {
			$carouseltitle = $this.parent().prev('.title');
		}
		if ($carouseltitle.find('.carousel-arrows').length) {
			arrowsplace = $carouseltitle.find('.carousel-arrows');
		}
		$this.slick({
			rows: 1,
			appendArrows: arrowsplace,
			slidesToShow: 2,
			slidesToScroll: 2,
			speed: 500,
			infinite: false,
			responsive: [{
				breakpoint: 1401,
				settings: {
					slidesToShow: 2,
					slidesToScroll: 2
				}
            }, {
				breakpoint: 1201,
				settings: {
					slidesToShow: 1,
					slidesToScroll: 1
				}
            }, {
				breakpoint: 993,
				settings: {
					slidesToShow: 2,
					slidesToScroll: 1
				}
            }, {
				breakpoint: 769,
				settings: {
					slidesToShow: 2,
					slidesToScroll: 1
				}
            }, {
				breakpoint: 481,
				settings: {
					slidesToShow: 1,
					slidesToScroll: 1
				}
            }]
		});
	}

	// deal carousel
	if ($(".deal-carousel").length) {
		var $this = $(".deal-carousel"),
			arrowsplace = $this;

		var $carouseltitle = $this.prev('.title');

		if ($this.parent().hasClass('collapsed-content')) {
			$carouseltitle = $this.parent().prev('.title');
		}
		if ($carouseltitle.find('.carousel-arrows').length) {
			arrowsplace = $carouseltitle.find('.carousel-arrows');
		}
		$this.slick({
			rows: 1,
			appendArrows: arrowsplace,
			slidesToShow: 1,
			slidesToScroll: 1,
			speed: 500,
			infinite: false,
			swipe: false,
			responsive: [{
				breakpoint: 993,
				settings: {
					slidesToShow: 2,
					slidesToScroll: 1
				}
            }, {
				breakpoint: 481,
				settings: {
					slidesToShow: 1,
					slidesToScroll: 1
				}
            }]
		});
	}
	// deal carousel
	if ($(".deal-carousel-2").length) {
		var $this = $(".deal-carousel-2"),
			arrowsplace = $this;

		var $carouseltitle = $this.prev('.title');

		if ($this.parent().hasClass('collapsed-content')) {
			$carouseltitle = $this.parent().prev('.title');
		}
		if ($carouseltitle.find('.carousel-arrows').length) {
			arrowsplace = $carouseltitle.find('.carousel-arrows');
		}
		$this.slick({
			rows: 1,
			appendArrows: arrowsplace,
			slidesToShow: 2,
			slidesToScroll: 1,
			speed: 500,
			infinite: false,
			swipe: false,
			responsive: [{
				breakpoint: 993,
				settings: {
					slidesToShow: 2,
					slidesToScroll: 1
				}
            }, {
				breakpoint: 481,
				settings: {
					slidesToShow: 1,
					slidesToScroll: 1
				}
            }]
		});
	}
	// testimonials single carousel
	if ($(".testimonial-single-slider").length) {
		var $this = $(".testimonial-single-slider");
		$this.slick({
			rows: 1,
			slidesToShow: 1,
			slidesToScroll: 1,
			speed: 500,
			infinite: false
		});
	}

	// testimonials carousel
	if ($(".testimonials-carousel").length) {
		var $this = $(".testimonials-carousel"),
			arrowsplace = $this;

		var $carouseltitle = $this.prev('.title');

		if ($this.parent().hasClass('collapsed-content')) {
			$carouseltitle = $this.parent().prev('.title');
		}
		if ($carouseltitle.find('.carousel-arrows').length) {
			arrowsplace = $carouseltitle.find('.carousel-arrows');
		}
		$this.slick({
			rows: 2,
			appendArrows: arrowsplace,
			slidesToShow: 2,
			slidesToScroll: 2,
			speed: 500,
			infinite: false,
			responsive: [{
				breakpoint: 1700,
				settings: {
					slidesToShow: 1,
					slidesToScroll: 1
				}
            }, {
				breakpoint: 1201,
				settings: {
					slidesToShow: 1,
					slidesToScroll: 1
				}
            }, {
				breakpoint: 993,
				settings: {
					rows: 2,
					slidesToShow: 2,
					slidesToScroll: 1
				}
            }, {
				breakpoint: 769,
				settings: {
					rows: 2,
					slidesToShow: 2,
					slidesToScroll: 1
				}
            }, {
				breakpoint: 481,
				settings: {
					rows: 2,
					slidesToShow: 1,
					slidesToScroll: 1
				}
            }]
		});
	}

	// product vertical carousel
	if ($(".product-vertical-carousel").length) {

		var $this = $(".product-vertical-carousel");
		arrowsplace = $this;

		var $carouseltitle = $this.prev('.title');

		if ($this.parent().hasClass('collapsed-content')) {
			$carouseltitle = $this.parent().prev('.title');
		}
		if ($carouseltitle.find('.carousel-arrows').length) {
			arrowsplace = $carouseltitle.find('.carousel-arrows');
		}
		if ($this.closest('.col-sm-12').length) {
			$this.slick({
				arrows: true,
				appendArrows: arrowsplace,
				vertical: true,
				slidesToShow: 3,
				slidesToScroll: 1,
				speed: 500,
				responsive: [{
					breakpoint: 993,
					settings: {
						vertical: false,
						slidesToShow: 2,
						slidesToScroll: 1
					}
                }, {
					breakpoint: 668,
					settings: {
						vertical: false,
						slidesToShow: 1,
						slidesToScroll: 1
					}
                }]
			})
		} else {
			$this.slick({
				arrows: true,
				appendArrows: arrowsplace,
				vertical: true,
				slidesToShow: 3,
				slidesToScroll: 1,
				speed: 500
			})
		}
	}

	// category carousel
	if ($(".category-slider").length) {
		var $this = $(".category-slider"),
			arrowsplace = $this;

		var $carouseltitle = $this.prev('.title');

		if ($this.parent().hasClass('collapsed-content')) {
			$carouseltitle = $this.parent().prev('.title');
		}
		if ($carouseltitle.find('.carousel-arrows').length) {
			arrowsplace = $carouseltitle.find('.carousel-arrows');
		}
		$this.slick({
			rows: 1,
			appendArrows: arrowsplace,
			slidesToShow: 4,
			slidesToScroll: 4,
			speed: 500,
			infinite: false,
			responsive: [{
				breakpoint: 1401,
				settings: {
					slidesToShow: 4,
					slidesToScroll: 4
				}
            }, {
				breakpoint: 1201,
				settings: {
					slidesToShow: 4,
					slidesToScroll: 4
				}
            }, {
				breakpoint: 993,
				settings: {
					slidesToShow: 3,
					slidesToScroll: 3
				}
            }, {
				breakpoint: 769,
				settings: {
					slidesToShow: 2,
					slidesToScroll: 2
				}
            }, {
				breakpoint: 481,
				settings: {
					slidesToShow: 2,
					slidesToScroll: 2
				}
            }]
		});
	}

	// product-creative carousel
	$.fn.initCreativeZoom = function () {
		var $this = this;
		$this.ezPlus({
			zoomType: 'inner',
			cursor: 'crosshair',
			zIndex: 2,
			zoomContainerAppendTo: '.product-slider-wrapper',
			borderSize: 0,
			zoomWindowFadeIn: 500,
			zoomWindowFadeOut: 0
		})
	}

	if ($(".product-creative-slider").length) {

		var $this = $(".product-creative-slider"),
			arrowsplace = $this;

		$this.on('init', function (event, slick) {
			$('.product-creative-slider .inner-zoom').initCreativeZoom();
		});

		$body.on('click', '.product-creative-slider-control button', function (e) {
			if (!$(e.target).hasClass('.slick-disabled')) {
				$('.product-slider-wrapper .zoomContainer').remove();
				setTimeout(function () {
					$('.product-creative-slider .inner-zoom').initCreativeZoom();
				}, 500);
			}
		});

		if ($this.parent().find('.product-creative-slider-control').length) {
			arrowsplace = $this.parent().find('.product-creative-slider-control');
		}

		$this.slick({
			rows: 1,
			appendArrows: arrowsplace,
			slidesToShow: 3,
			slidesToScroll: 1,
			speed: 500,
			infinite: false, //not change if ez-plus is used
			swipe: false,
			responsive: [{
				breakpoint: 481,
				settings: {
					slidesToShow: 1,
					slidesToScroll: 1
				}
            }]
		});
	}

	// product single carousel

	$.fn.initProductZoom = function () {
		var $this = this,
			zoompos = $body.is('.rtl') ? 11 : 1;
		if (!$body.is('.touch')) {
			$this.ezPlus({
				zIndex: 1002,
				zoomWindowPosition: zoompos,
				zoomContainerAppendTo: '.page-main',
				gallery: 'previewsGallery',
				galleryActiveClass: 'active'
			});
		} else {
			$this.ezPlus({
				zoomType: 'lens',
				zIndex: 1002,
				zoomContainerAppendTo: '.main-image',
				gallery: 'previewsGallery',
				galleryActiveClass: 'active'
			});
		}
	}

	if ($(".main-image").length) {
		$('.main-image > .zoom').initProductZoom();
	}

	// product previews carousel
	if ($(".product-previews-carousel").length) {

		var $this = $(".product-previews-carousel");

		$this.slick({
			slidesToShow: 3,
			slidesToScroll: 1,
			dots: false,
			focusOnSelect: true,
			infinite: false
		});

		$this.on('click', '.slick-slide', function () {
			$('.zoom-link').removeClass('disable-gallery');
		})
	}


	// brand carousel
	if ($(".brand-carousel").length) {
		var $this = $(".brand-carousel"),
			arrowsplace = $this.prev('.title');
		$this.slick({
			rows: 2,
			appendArrows: arrowsplace,
			slidesToShow: 4,
			slidesToScroll: 2,
			speed: 500,
			infinite: false,
			responsive: [{
				breakpoint: 1401,
				settings: {
					slidesToShow: 4,
					slidesToScroll: 2
				}
            }, {
				breakpoint: 1201,
				settings: {
					slidesToShow: 4,
					slidesToScroll: 2
				}
            }, {
				breakpoint: 993,
				settings: {
					slidesToShow: 4,
					slidesToScroll: 2
				}
            }, {
				breakpoint: 769,
				settings: {
					slidesToShow: 4,
					slidesToScroll: 2
				}
            }, {
				breakpoint: 481,
				settings: {
					slidesToShow: 2,
					slidesToScroll: 2
				}
            }]
		});
	}


	// instagram feed

	function doStuff() {
		if ($(".instagramm-feed-full").has('a').length) {
			startInstagramCarousel();
			clearInterval(timer);
		}
	}

	function startInstagramCarousel() {
		$(".instagramm-feed-full").find('a').each(function () {
			$(this).attr('target', '_blank');
		});
		var $slider = $(".instagramm-feed-full").slick({
			speed: 700,
			slidesToShow: 10,
			slidesToScroll: 2,
			cssEase: 'linear',
			responsive: [{
				breakpoint: 993,
				settings: {
					slidesToShow: 6,
					slidesToScroll: 2
				}
	}, {
				breakpoint: 769,
				settings: {
					slidesToShow: 4,
					slidesToScroll: 2
				}
	}, {
				breakpoint: 481,
				settings: {
					slidesToShow: 2,
					slidesToScroll: 2
				}
	}]
		});
		var scroll,
			speed = 0;
		var stop = function () {
			clearInterval(scroll);
		}
		var rw = function () {
			stop();
			$slider.slick("slickPrev");
			scroll = setInterval(function () {
				$slider.slick("slickPrev");
			}, speed);
		};
		var fw = function () {
			stop();
			$slider.slick("slickNext");
			scroll = setInterval(function () {
				$slider.slick("slickNext");
			}, speed);
		}
		$("body").on("mouseenter", ".instagramm-feed-full .slick-next", fw)
			.on("mouseenter", ".instagramm-feed-full .slick-prev", rw)
			.on("mouseleave", ".instagramm-feed-full .slick-next, .instagramm-feed-full .slick-prev", stop);
	}

	if ($("#instafeed").length) {

		var userFeed = new Instafeed({
			get: 'user',
			userId: 'self',
			accessToken: '3489650088.1d65fda.fffa13214cd847439dfb6e8639f98b2b',
			limit: 20,
			resolution: 'low_resolution',
			sortBy: 'most-recent'
		});
		userFeed.run();

		var timer = setInterval(doStuff, 100);

	}
	// end instagram feed
  
  
	// Tools Panel

	if ($("#toolsPanel").length) {
		$("#toolsPanel").toolsPanel();
	}



	// Countdown

	$('.countdown').each(function () {
		var countdown = $(this);
		var promoperiod;
		if (countdown.attr('data-promoperiod')) {
			promoperiod = new Date().getTime() + parseInt(countdown.attr('data-promoperiod'),10);
		}
		if (countdown.attr('data-promodate')) {
			promoperiod = countdown.attr('data-promodate');
		}
		countdown.countdown(promoperiod, function (event) {
			countdown.html(event.strftime('<span><span>%D</span>DAYS</span>' + '<span><span>%H</span>HRS</span>' + '<span><span>%M</span>MIN</span>' + '<span><span>%S</span>SEC</span>'));
		})
	});


	// flowtype - make banner text responsive

	$.fn.flowtype = function (options) {

		var settings = $.extend({
				maximum: 9999,
				minimum: 1,
				maxFont: 9999,
				minFont: 1,
				fontRatio: 10
			}, options),

			changes = function (el) {
				var $el = $(el),
					elw = $el.width(),
					width = elw > settings.maximum ? settings.maximum : elw < settings.minimum ? settings.minimum : elw,
					fontBase = width / settings.fontRatio,
					fontSize = fontBase > settings.maxFont ? settings.maxFont : fontBase < settings.minFont ? settings.minFont : fontBase;
				$el.css('font-size', fontSize + 'px');
			};

		return this.each(function () {
			var that = this;
			var timer;
			var cachedWidth = $window.width();
			$window.resize(function () {
				var newWidth = $window.width();
				if (newWidth !== cachedWidth) {
					$('.banner-caption', that).addClass('calc');
					clearTimeout(timer);
					timer = setTimeout(doneResizing, 500);
					cachedWidth = newWidth;
				}
			});
			changes(this);

			function doneResizing() {
				changes(that);
				$('.banner-caption', that).removeClass('calc');
			}
		});
	};

	// Journal Slide - Layout 3

	$.fn.journalSlide = function () {

		var $journal = $(this),
			$panelLeft = $('.journal-category-left', $journal),
			$panelRight = $('.journal-category-right', $journal),
			$panelLeftTitul = $('.journal-category-left .journal-category-inner', $journal),
			$panelRightTitul = $('.journal-category-right .journal-category-inner', $journal),
			$logoCenter = $('.logo-center', $journal),
			$productstack = $('.productStack');

		function hideStack() {
			if ($productstack.length && $productstack.is('.open') && $productstack.is('.hide_on_scroll')) {
				$productstack.removeClass('open');
			}
		}

		$body.css({
			'overflow-y': 'auto'
		})

		$panelLeftTitul.on('click', '.toggle-panel', function () {
			$panelLeft.toggleClass('journal-category-left-active');
			$panelRight.toggleClass('journal-category-right-hidden');
			$logoCenter.toggleClass('logo-hidden');
			$('.page-header').removeClass('open');
			$('.toggleHeader').removeClass('open');
			$(this).toggleClass('open');
			hideStack();
		});

		$panelRightTitul.on('click', '.toggle-panel', function () {
			$panelRight.toggleClass('journal-category-right-active');
			$panelLeft.toggleClass('journal-category-left-hidden');
			$logoCenter.toggleClass('logo-hidden');
			$('.page-header').removeClass('open');
			$('.toggleHeader').removeClass('open');
			$(this).toggleClass('open');
			hideStack();
		});

		$panelLeftTitul.on('click', '.toggle-panel-mobile', function () {
			var $this = $(this);
			if ($panelLeft.hasClass('open')) {
				var category_content = $this.closest('.journal-category-left').find('.journal-category-inner-left').detach();
				$this.closest('.journal-category-left').prepend(category_content);
			} else {
				var category_content = $this.closest('.journal-category-left').find('.journal-category-inner-left').detach();
				$this.closest('.journal-category-left').append(category_content);
			}
			$panelLeft.toggleClass('open');
			$panelRight.removeClass('open');
			$this.toggleClass('open');
			if ($panelLeft.hasClass('open')) {
				$('html,body').animate({
					scrollTop: $this.offset().top
				}, 500);
			} else {
				$('html,body').animate({
					scrollTop: $panelLeft.offset().top
				}, 500);
			}
			hideStack();
		});

		$panelRightTitul.on('click', '.toggle-panel-mobile', function () {
			var $this = $(this);
			$panelRight.toggleClass('open');
			$panelLeft.removeClass('open');
			$this.toggleClass('open');
			if ($panelRight.hasClass('open')) {
				$('html,body').animate({
					scrollTop: $this.offset().top
				}, 500);
			} else {
				$('html,body').animate({
					scrollTop: $panelRight.offset().top
				}, 500);
			}
			hideStack();
		});

		$('.journal-category').on('scroll', function () {
			hideStack();
			$('.page-header').removeClass('open');
			$('.toggleHeader').removeClass('open');
		})
	};

	// Megamenu
  if ($(".megamenu").length) {
	  $(".megamenu").megaMenu();
  }
	// isotope gallery
	function isotopeGallery(gallery) {
		var $gallery = $(gallery);

		// isotope gallery
		var currentFilter;
		var activeStart;

		$gallery.imagesLoaded(function () {
			$gallery.isotope({
				itemSelector: '.gallery-item',
				layoutMode: 'fitRows',
				filter: function () {
					var $this = $(this);
					var filterResult = currentFilter ? $this.is(currentFilter) : true;
					return filterResult;
				}
			});
		});

		//filters gallery

		$('.filters-gallery .filter-label').each(function () {
			var $this = $(this);
			if ($this.hasClass('active')) {
				activeStart = true;
				currentFilter = $this.attr('data-filter');
				$gallery.isotope();
			}
		});

		if (!activeStart) $(".filters-gallery li:first-child .filter-label").addClass('active');

		$('.filters-gallery').on('click', '.filter-label', function (e) {
			e.preventDefault();
			var $this = $(this);
			if ($this.hasClass('active')) return false;
			else {
				$('.filters-gallery .filter-label').removeClass('active');
				$this.addClass('active')
			}
			currentFilter = $this.attr('data-filter');
			$gallery.isotope();
		});
	};

	//product grid gallery
	function productGallery(gallery) {

		var currentFilter,
			activeStart,
			$productgallery = $(gallery);
		$productgallery.imagesLoaded(function () {
			$productgallery.isotope({
				itemSelector: '.product-item',
				layoutMode: 'fitRows',
				filter: function () {
					var $this = $(this);
					var filterResult = currentFilter ? $this.is(currentFilter) : true;
					return filterResult;
				}
			});
		});
		//filters product grid
		$('.filters-product .filter-label').each(function () {
			var $this = $(this);
			var filtered = $this.data('filter'),
				count;
			if (filtered == null) {
				count = $productgallery.find('.product-item').length;
			} else count = $productgallery.find(filtered).length;
			$this.find('.count').html(count);
			if ($this.hasClass('active')) {
				activeStart = true;
				currentFilter = $this.attr('data-filter');
				$productgallery.isotope();
			}
		});
		if (!activeStart) $(".filters-product li:first-child .filter-label").addClass('active');
		$('.filters-product').on('click', '.filter-label', function (e) {
			e.preventDefault();
			var $this = $(this);
			if ($this.hasClass('active')) return false;
			else {
				$('.filters-product .filter-label').removeClass('active');
				$this.addClass('active')
			}
			currentFilter = $this.attr('data-filter');
			$productgallery.isotope();
		});

	}

	//product grid gallery
	function productHoverHeight(product) {
		var product = product;
		$document.on('mouseenter', product, function (e) {
				var $this = $(this);
				var $previews = $this.find('.product-item-gallery-previews');
				var $slick = $this.closest('.slick-list');
				var $inside = $('.product-item-details', $this);
				if (!$this.data('setHeight')) {
					$this.css({
						'height': $(this).find('.product-item-info').outerHeight() + 'px'
					}).data('setHeight', true);
				}
				if (!$this.hasClass('hovered')) {
					$this.addClass('hovered');
					if ($previews.length) {
						$this.addClass('with-previews');
						$inside.css({
							'max-width': $inside.outerWidth() + 'px'
						})
					}
					if ($slick.length) {
						$slick.addClass('out-space')
					}
				}
			})
			.on('mouseleave', product, function (e) {
				var $this = $(this);
				var $previews = $this.find('.product-item-gallery-previews');
				var $slick = $this.closest('.slick-list');
				var $inside = $('.product-item-details', $this);
				$inside.css({
					'max-width': ''
				})
				$this.removeClass('hovered');
				if ($slick.length) {
					$slick.removeClass('out-space')
				}
			})
		$document.on('click', '.product-item-gallery-previews a', function (e) {
			var src = $(this).find('img').attr('data-image');
			var $mainimg = $(this).closest('.product-item').find('.product-item-gallery-main img');
			$mainimg.attr('src', src);
			e.preventDefault();
		})
		$window.on('resize', function () {
			$(product).removeData('setHeight').css({
				'height': ''
			});
		});
	}

	//product grid gallery
	function headerCollapse() {
		$('.collapsed-links-wrapper').on('mouseenter', function (e) {
			if (!$('.page-header').hasClass('is-sticky')) {
				var $this = $(this);
				$this.css({
					'width': $this.find('.collapsed-links').get(0).scrollWidth + 25 + 'px'
				})
				$('.header-right-links').addClass('hovered');
			}
		});
		$('.collapsed-links-wrapper').on('mouseleave', function (e) {
			if (!$('.page-header').hasClass('is-sticky')) {
				$('.header-right-links').removeClass('hovered');
				$('.collapsed-links-wrapper').css({
					'width': ''
				})
			}
		});
	}


	// swiper slider
	$.fn.thumbsPreview = function (options) {
		var options = $.extend({}, $.fn.thumbsPreview.defaults, options);
		return this.each(function () {
			var $this = $(this);

			var $pagination_container = $this.find('.swiper-pagination'),
				$pagination_thumbs = $this.find('.swiper-pagination-thumbs'),
				$pagination_dot = $pagination_container.children('span'),
				toltal_slides = $pagination_dot.length,
				$thumbs_wrapper = $pagination_thumbs.children('.thumbs-wrapper'),
				$thumbs_preview = $thumbs_wrapper.children('.thumbs'),
				$thumbs_preview_item = $thumbs_preview.children('span'),
				border_width = 2,
				r_pagination_thumbs = 60;


			var w_pagination_thumbs = options.thumb_width + 2 * border_width,
				h_pagination_thumbs = options.thumb_height + 2 * border_width,
				t_pagination_thumbs = $pagination_container.position().top - $pagination_container.outerHeight() / 2 - h_pagination_thumbs / 2,
				l_pagination_thumbs = $pagination_container.position().left - w_pagination_thumbs - 5;

			$pagination_thumbs.css({
				width: w_pagination_thumbs + 'px',
				height: h_pagination_thumbs + 'px',
				top: t_pagination_thumbs + 'px',
				left: l_pagination_thumbs + 'px'
			});

			$thumbs_preview_item.css({
				width: options.thumb_width + 'px',
				height: options.thumb_height + 'px'
			});

			$thumbs_preview.css('height', toltal_slides * options.thumb_height + 'px');

			$thumbs_wrapper.css({
				width: options.thumb_width + 'px',
				height: options.thumb_height + 'px'
			});

			$pagination_container.on('mouseenter', function () {
				$(this).data('firsthover', true);
			}).on('mouseleave', function () {
				$(this).removeData('firsthover');
			})

			$pagination_dot.on('mouseenter', function () {
				var $this = $(this),
					idx = $this.index();
				var new_top = $this.parent().position().top + $this.position().top - h_pagination_thumbs / 2 + 10;
				var tempspeed = options.speed;
				if ($pagination_container.data('firsthover')) tempspeed = 0;
				$pagination_thumbs.stop(true)
					.fadeIn(200)
					.animate({
						top: new_top + 'px'
					}, {
						duration: tempspeed,
						queue: false
					});
				$thumbs_preview.stop(true)
					.animate({
						top: -idx * options.thumb_height + 'px'
					}, tempspeed);
			}).on('mouseleave', function () {
				$pagination_container.removeData('firsthover');
				$pagination_thumbs.stop(true).fadeOut(200);
			})

		});
	};
	$.fn.thumbsPreview.defaults = {
		speed: 100,
		thumb_width: 200,
		thumb_height: 100
	};
	$.fn.swiperUpdate = function () {
		var $slider = this;
		var swiper = new Swiper('.mainSlider .swiper-container', {
			pagination: '.swiper-pagination',
			paginationClickable: true,
			//nextButton: '.swiper-button-next',
			//prevButton: '.swiper-button-prev',
			effect: 'fade',
			loop: true,
			autoplay: 10000,
			autoplayDisableOnInteraction: false,
			simulateTouch: false,
			onPaginationRendered: function (swiper) {
				if ($slider.attr('data-thumb') == 'true') {
					var $thumb = $('.thumbs').html('');
					$('.swiper-slide:not(.swiper-slide-duplicate)', $slider).each(function () {
						var preview;
						if ($(this).attr('data-thumb')) {
							preview = '<span><img src=' + $(this).attr('data-thumb') + ' alt=""></span>';
						} else if ($(this).find('figure img').length) {
							preview = '<span><img src=' + $(this).find('figure img').attr('src') + ' alt=""></span>';
						} else if ($(this).css('background-image')) {
							var bg = $(this).css('background-image');
							bg = bg.replace('url(', '').replace(')', '').replace(/\"/gi, "");
							preview = '<span><img src=' + bg + ' alt=""></span>';
						}
						$thumb.append(preview);
					})
					var thumb_width = 200,
						thumb_height = 100;
					if ($slider.attr('data-thumb-width')) thumb_width = +$slider.attr('data-thumb-width');
					if ($slider.attr('data-thumb-height')) thumb_height = +$slider.attr('data-thumb-height');
					$slider.thumbsPreview({
						thumb_width: thumb_width,
						thumb_height: thumb_height,
						speed: 250
					});
				}
			},
			onSlideChangeStart: function (swiper) {
				$('.sliderLoader').hide();
				$('.mainSlider .swiper-container').css({
					'opacity': 1,
					'min-height': '0'
				});
				$('.mainSlider [data-animate]').data('stop', true);
				$('.mainSlider [data-animate]').each(function () {
					var el = $(this);
					var effect = el.attr('data-animate');
					el.removeClass('animated').removeClass(effect).addClass('block-animate');
				});
			},
			onSlideChangeEnd: function (swiper) {
				$('.mainSlider [data-animate]').each(function () {
					var el = $(this);
					var effect = el.attr('data-animate');
					el.finish().removeClass('animated').removeClass(effect).addClass('block-animate');
				});
				if ($('.mainSlider video').length) {
					$(".mainSlider video").each(function () {
						$(this).get(0).pause();
					});
				}
				if ($('.mainSlider .swiper-slide-active video').length) {
					$('.mainSlider .swiper-slide-active video')[0].play();
				}
				$('.mainSlider .swiper-slide-active [data-animate]').each(function () {
					var el = $(this);
					var delay = 0;
					var dataDelay = el.attr('data-delay');
					if (dataDelay) {
						delay += Number(dataDelay)
					}
					el.removeData('stop');
					if (!el.hasClass('animated')) {
						el.addClass('block-animate');
						var effect = el.attr('data-animate');
						setTimeout(function () {
							if (!el.data('stop')) {
								el.removeClass('block-animate').addClass(effect + ' animated');
							} else return false;
						}, delay);
					}
				});
			}
		});
	}

	function swiperSlider(slider) {

		var $slider = $(slider);

		function SliderSize(slider) {
			var $slidercontainer = $('.swiper-container', slider),
				scrHeight = window.innerHeight ? window.innerHeight : $window.height(),
				sliderHeightOff = $slidercontainer.offset().top;

			scrHeight = scrHeight - sliderHeightOff;
			$slidercontainer.css('height', scrHeight);
		}

		if ($slider.is('.fullscreen')) {
			SliderSize($slider);
		}

		$window.on('resize.mainSlider', function () {
			if ($slider.is('.fullscreen')) {
				SliderSize($('.mainSlider.fullscreen'));
			}
		});

		$slider.on('click', '[data-href]', function (event) {
			event.preventDefault();
			var href = $(this).attr("data-href"),
				target = $(this).attr("data-target") ? $(this).attr("data-target") : '_self';
			window.open(href, target);
		});

		var $textBlock = $("div[class^='text'],div[class*=' text'],div.caption,.button", $slider);

		$textBlock.each(function () {
			var $this = $(this),
				thisInlineStyle = '';

			var thisStyle = $this.data();

			$.each(thisStyle, function (index, value) {
				if (index == 'fontcolor') {
					thisInlineStyle += 'color:' + $this.data('fontcolor') + ';'
				}
				if (index == 'fontfamily') {
					thisInlineStyle += 'font-family:' + $this.data('fontfamily') + ';'
				}
				if (index == 'fontsize') {
					thisInlineStyle += 'font-size:' + $this.data('fontsize') + 'vw;'
				}
				if (index == 'fontline') {
					thisInlineStyle += 'line-height:' + $this.data('fontline') + 'em;'
				}
				if (index == 'fontweight') {
					thisInlineStyle += 'font-weight:' + $this.data('fontweight') + ';'
				}
				if (index == 'ypos') {
					var ypos = $this.data('ypos');
					if (ypos == 'center') {
						$this.addClass('vertical-align')
					} else thisInlineStyle += 'top:' + $this.data('ypos') + '%;'
				}
				if (index == 'xpos') {
					var xpos = $this.data('xpos');
					if (xpos == 'center') {
						$this.addClass('horisontal-align')
					} else if (xpos == 'left') {
						thisInlineStyle += 'left:0;right:auto;'
					} else if (xpos == 'right') {
						thisInlineStyle += 'left:auto;right:0;'
					} else thisInlineStyle += 'left:' + $this.data('xpos') + '%;'
				}
				if (index == 'otherstyle') {
					thisInlineStyle += $this.data("otherstyle");
				}
			});
			$this.attr('style', thisInlineStyle);
		})

		$slider.swiperUpdate()
	}

	/* ---------------------- */
	/* Initialize All Scripts */
	/* ---------------------- */
	
	setFullWidth();
	setFullHeight();
	slidePanel();

	// header
	if ($(".page-header.sticky.always").length) {
		$(".page-header.sticky.always").stickyHeader();
	}
	if ($(".page-header.sticky.smart").length) {
		$(".page-header.sticky.smart").stickyHeaderSmart();
	}
	if ($(".page-header.variant-9").length) {
		headerCollapse()
	}
	// expanding  search 
	$(".exp-search").expandingSearch();
	// department megamenu
	if ($('.megamenu.department').length) {
		departmentMenu();
	}
	// mobile menu	
	$(".mobilemenu").mobileMenu();
	if ($(".filter-col").length) {
		$(".filter-col").isFilters();
		$(".filter-col").mobileFilter();
	}
	// mobile cart
	if ($(".header-cart.variant-1").length) {
		$(".header-cart.variant-1").mobileMinicart();
	}
	if ($(".header-cart.variant-2").length) {
	  $(".header-cart.variant-2").mobileMinicartAlt();
	}
	// footer
	$(".collapsed-mobile").footerCollapse();
	$(".sidebar-block").blockSelectedMark();
	$(".sidebar-block-top").hideShopBy();
	if ($(".filter-col.fixed").length) {
		$(".filter-col.fixed").fixedSidebar();
		$(".sidebar-block").blockCollapseAccordion();
	} else {
		$(".sidebar-block").blockCollapse();
	}
	// product
	productHoverHeight('.product-variant-4 .product-item, .product-variant-5 .product-item');
	colorSwatch('.color-swatch');
	if ($('.dark-tooltip').length) {
    tooltipIni();
  }
  if ($('.product-tab').length) {
	  productTab('.product-tab');
  }
	prevnextNav('.product-nav');
	viewMode('.view-mode');
	changeInput();
	productSharing();
	productOptions('.product-size');
	productOptions('.product-color');
	quickView('.quick-view-link', '#quickView');
	$('.carousel-inside').insideCarousel();
	$('.productStack').ProductStack();
	$('.product-item').FlyToCart({
		link: '.add-to-cart',
		productstack: '.productStack',
		complete: function () {
			// add yout action here 
		}
	});
	if ($('#priceSlider').length) {
		priceSlider();
	}
	// product page
	if ($('.product-block').length) {
		productImageGallery()
	}
	// lookbook page
  if ($('.product-lookbook').length) {
    $('.product-lookbook').imagesLoaded(function () {
      $('.product-lookbook').lookbookSize();
    });
  }
	// journal layout
	if ($(".journal").length) {
		$(".journal").journalSlide();
	}
	// gallery

	if ($('.gallery.simple').length) {
		$('.gallery.simple').simpleFilters();
	}    
  if ($('.products-grid.isotope').length) {
	  productGallery('.products-grid.isotope');
  }
  if ($('.gallery.isotope').length) {
	  isotopeGallery('.gallery.isotope');
  }

	//magnific popup for gallery
	if ($('.zoomimage').length) {
		$('.zoomimage').magnificPopup({
			type: 'image',
			gallery: {
				enabled: true
			}
		});
	}
	//magnific popup for video
	if ($('.video-link').length) {
		$('.video-link').magnificPopup({
			type: 'iframe',
			mainClass: 'mfp-fade',
			removalDelay: 160,
			preloader: false,
			fixedContentPos: false
		});
	}

	// slider 
	if ($('.mainSlider').length) {
		setTimeout(function () {
			swiperSlider('.mainSlider');
		}, 500);
	}

	// other
	addToBookmark('.bookmark');
	backToTop('.back-to-top');
	$(".autosize-text").each(function () {
		$this = $(this);
		var fontratio = Math.round($this.attr("data-fontratio")*100)/100;
    if(fontratio > 0) { 
      $this.flowtype({
        fontRatio: fontratio
      });
    }
	});
	//parallax
	if ($('block.parallax').length) {
		$('block.parallax').parallax({
			iosFix: false, // enable on IOS device
			androidFix: false // enable on Andriod device
		});
	}
	// loading button
	$('.btn-loading').on('click', function () {
		var $this = $(this);
		$this.button('loading');
		setTimeout(function () {
			$this.button('reset');
		}, 10000);
	});
	// set background image inline
	if ($('[data-bg]').length) {
		$('[data-bg]').each(function () {
			var $this = $(this),
				bg = $this.attr('data-bg');
			$this.css({
				'background-image': 'url(' + bg + ')'
			});
		})
	}
  
  
	// Remove Loader
	$body.addClass('loaded');
  
	var prevWindow = window.innerWidth || $window.width();

	
	/* ---------------------- */
	/*  Resize handle events  */
	/* ---------------------- */
	
	$window.on('resize', function () {
		setTimeout(function () {
			setFullHeight();
			var currentWindow = window.innerWidth || $window.width();
			if (currentWindow != prevWindow) {
				$body.otherResize();
				prevWindow = currentWindow;
			}
		}, 500);
	});
})