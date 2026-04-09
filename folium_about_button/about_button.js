/*
 * AboutControl
 *
 * Leaflet control for displaying an about dialog (a Bootstrap modal).
 */
//
// Copyright © 2026 Dominic Davis-Foster <dominic@davis-foster.co.uk>
//
// Adapted from https://github.com/domoritz/leaflet-locatecontrol
// Copyright (c) 2016 Dominik Moritz
//
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
//
// The above copyright notice and this permission notice shall be included in all
// copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
// EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
// MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
// IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
// DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
// OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
// OR OTHER DEALINGS IN THE SOFTWARE.
//

/**
 * See also
 * https://github.com/CliffCloud/Leaflet.EasyButton
 * https://github.com/prhbrt/folium-jsbutton
 */

/**
 * Create a DOM element with a class name and optionally append it to a parent.
 * @param {string} tag - The element tag name.
 * @param {string} [className] - Space-separated class names.
 * @param {HTMLElement} [parent] - Optional parent to append the element to.
 * @returns {HTMLElement}
 */
function createElement(tag, className, parent) {
	const el = document.createElement(tag);
	if (className) el.className = className;
	parent?.append(el);
	return el;
}

/**
 * Shallow clone options to prevent prototype pollution.
 * Clones arrays and plain objects, keeps functions/classes as references.
 * @param {Object} options - The options object to clone.
 * @returns {Object} A shallow clone of the options object.
 */
function cloneOptions(options) {
	const cloned = {};
	for (const key in options) {
		const val = options[key];
		if (Array.isArray(val)) {
			cloned[key] = [...val];
		} else if (val?.constructor === Object) {
			cloned[key] = { ...val };
		} else {
			cloned[key] = val;
		}
	}
	return cloned;
}

const AboutControl = L.Control.extend({
	options: {
		/** Position of the control */
		position: 'topleft',
		/** The CSS class for the icon. For example 'fa-solid fa-circle-info' */
		icon: 'fa-solid fa-circle-info',
		/** The element to be created for icons. For example span or i */
		iconElementTag: 'span',
		/** The ID of the modal element */
		modalID: undefined,

		/**
		 * This callback can be used in case you would like to override button creation behavior.
		 * This is useful for DOM manipulation frameworks such as angular etc.
		 * This function should return an object with HtmlElement for the button (link property) and the icon (icon property).
		 */
		createButtonCallback(container, options) {
			const link = createElement('a', 'leaflet-bar-part leaflet-bar-part-single', container);
			link.setAttribute('data-bs-toggle', 'modal');
			link.setAttribute('data-bs-target', `#${options.modalID}`);
			link.title = 'About';
			link.href = '#';
			link.setAttribute('role', 'button');
			link.setAttribute('aria-label', link.title);
			const icon = createElement(options.iconElementTag, options.icon, link);
			// Add common class for all icons to enable color status changes
			icon.classList.add('leaflet-about-icon');

			return { link, icon };
		},
	},

	initialize(options = {}) {
		// Clone default options to prevent prototype pollution
		this.options = cloneOptions(this.options);

		// Merge user-provided options
		for (const key in options) {
			const userVal = options[key];
			const defaultVal = this.options[key];
			if (userVal?.constructor === Object && defaultVal?.constructor === Object) {
				Object.assign(defaultVal, userVal);
			} else {
				this.options[key] = userVal;
			}
		}
	},

	/**
	 * Add control to map. Returns the container for the control.
	 */
	onAdd(map) {
		const container = createElement('div', 'leaflet-control-about leaflet-bar leaflet-control');
		this._container = container;
		this._map = map;

		const linkAndIcon = this.options.createButtonCallback(container, this.options);
		this._link = linkAndIcon.link;
		this._icon = linkAndIcon.icon;

		// this._link.addEventListener('click', (ev) => {
		// 	ev.stopPropagation();
		// 	ev.preventDefault();
		// 	this._onClick();
		// });
		// this._link.addEventListener('dblclick', (ev) => ev.stopPropagation());

		return container;
	},

	// /**
	//  * This method is called when the user clicks on the control.
	//  */
	// _onClick() {
	// 	alert('Clicked about button');
	// },
});

function aboutControl(options) {
	return new AboutControl(options);
}
