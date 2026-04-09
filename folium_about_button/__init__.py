#!/usr/bin/env python3
#
#  __init__.py
"""
Folium plugin that adds a button for displaying an about dialog (a bootstrap modal).
"""
#
#  Copyright © 2026 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#

# 3rd party
import folium.elements
from folium.template import Template
from folium.utilities import remove_empty

__author__: str = "Dominic Davis-Foster"
__copyright__: str = "2026 Dominic Davis-Foster"
__license__: str = "MIT License"
__version__: str = "0.1.0b1"
__email__: str = "dominic@davis-foster.co.uk"

__all__ = ["AboutControl"]


class AboutControl(folium.elements.JSCSSMixin, folium.elements.MacroElement):  # noqa: PRM003
	r"""
	Control for showing an about dialog (a Bootstrap modal).

	:param modal_id: The ID of the modal element.
	:param icon: The icon to show.
	:type icon: :class:`str`
	:default icon: ``fa-solid fa-circle-info``
	:param \*\*kwargs: Additional options for the javascript ``AboutControl`` class.
	"""

	def __init__(self, modal_id: str, **kwargs):
		super().__init__()
		self._name = "AboutControl"
		self.options = remove_empty(modalID=modal_id, **kwargs)

	# TODO: bootstrap CSS and JS (but avoid duplication)
	#       Can use same keys as map so duplicates are ignored/overwritten?

	default_js = [
			(
					"about_button_js",
					f"https://cdn.jsdelivr.net/gh/domdfcoding/folium-about-button@v{__version__}/folium_about_button/about_button.min.js",
					),
			]

	_template = Template(
			"""
			{% macro header(this, kwargs) %}
				<style>
					.leaflet-control-about {
						a {
							font-size: 1.4em;
							.leaflet-about-icon {
								color: black;
							}
						}
					}
				</style>
			{% endmacro %}

			{% macro script(this, kwargs) %}
				var {{this.get_name()}} = new AboutControl(
					{{this.options | tojson}}
				).addTo({{ this._parent.get_name() }});
			{% endmacro %}
			""",
			)
