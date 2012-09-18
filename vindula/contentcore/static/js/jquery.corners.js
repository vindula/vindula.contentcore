/**
 * jQuery Corners - A jQuery rounded corners plugin
 *
 * @version 1.0.0
 * @date 2008-06-02
 *
 * @version 1.1.0
 * @date 2008-07-30
 * 
 * Copyright (c) 2008 Trey Shugart (shugartweb.com/jquery/)
 * 
 * Dual licensed under: 
 *  MIT - (http://www.opensource.org/licenses/mit-license.php) 
 *  GPL - (http://www.gnu.org/licenses/gpl.txt)
 * 
 * Another rounded corners plugin. Can be used with transparent (png or gif) images as corner backgrounds and
 * is extensible enough to take on almost any style you want to give it. Will expand and contract gracefully.
 */
$ = jQuery.noConflict();
;(function($) {
	
	/**
	 * Wraps any element with a cross-browser, fully cusomizable box (including corners), that can be safely animated without breaking
	 * 
	 * @param {Object} settings
	 */
	$.fn.corners = function(settings) {
		$$ = $(this);
		
		var settings = $.extend({
			// default classes can be separated with a space
			classContainer: 'corners',
			classTop: 'corners-top',
			classTopLeft: 'corners-top-left',
			classTopCenter: 'corners-top-center',
			classTopRight: 'corners-top-right',
			classLeft: 'corners-left',
			classRight: 'corners-right',
			classContent: 'corners-content',
			classBottom: 'corners-bottom',
			classBottomLeft: 'corners-bottom-left',
			classBottomCenter: 'corners-bottom-center',
			classBottomRight: 'corners-bottom-right',
			// style attributes in regular xhtml style attribute syntax
			styleContainer: 'position: relative;',
			styleTop: 'position: relative;',
			styleTopLeft: 'position: absolute; left: 0; top: 0;',
			styleTopCenter: '',
			styleTopRight: 'position: absolute; right: 0; top: 0;',
			styleLeft: 'position: relative;',
			styleRight: '',
			styleContent: '',
			styleBottom: 'position: relative;',
			styleBottomLeft: 'position: absolute; left: 0; top: 0;',
			styleBottomCenter: '',
			styleBottomRight: 'position: absolute; right: 0; top: 0;'
		}, settings);
		
		return $$.each(function(index, element) {
			var el = $(element);
			// remove all script tags since they would have already been executed, and if left alone, will
			// be executed a second time around
			el.find('script').remove();
			// we create html this way as to avoid the overhead involved in using jQuery for every little bit
			// since we don't actually need to reference these elements
			var html = ''
				+ '<div class="' + settings.classContainer + '"' + applyStyle(settings.styleContainer) + '>'
					+ '<div class="' + settings.classTop + '"' + applyStyle(settings.styleTop) + '>'
						+ '<div class="' + settings.classTopLeft + '"' + applyStyle(settings.styleTopLeft) + '></div>'
						+ '<div class="' + settings.classTopCenter + '"' + applyStyle(settings.styleTopCenter) + '></div>'
						+ '<div class="' + settings.classTopRight + '"' + applyStyle(settings.styleTopRight) + '></div>'
					+ '</div>'
					+ '<div class="' + settings.classLeft + '"' + applyStyle(settings.styleLeft) + '>'
						+ '<div class="' + settings.classRight + '"' + applyStyle(settings.styleRight) + '>'
							+ '<div class="' + settings.classContent + '"' + applyStyle(settings.styleContent) + '"></div>'
						+ '</div>'
					+ '</div>'
					+ '<div class="' + settings.classBottom + '"' + applyStyle(settings.styleBottom) + '>'
						+ '<div class="' + settings.classBottomLeft + '"' + applyStyle(settings.styleBottomLeft) + '></div>'
						+ '<div class="' + settings.classBottomCenter + '"' + applyStyle(settings.styleBottomCenter) + '></div>'
						+ '<div class="' + settings.classBottomRight + '"' + applyStyle(settings.styleBottomRight) + '></div>'
					+ '</div>'
				+ '</div>';
			var replace = $(html);
			el.replaceWith(replace);
			replace.find('.' + settings.classContent).append(el).prepend('').append('');
		});
		
		/**
		 * Returns an aesthetically formed style attribute
		 * 
		 * @param {String} style
		 */
		function applyStyle(style) {
			return ((typeof style !== 'undefined' && style && style !== '') ? ' style="' + style + '"' : '');
		}
	}
})(jQuery);