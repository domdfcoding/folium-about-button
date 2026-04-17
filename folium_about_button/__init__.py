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

# stdlib
from re import Match

# 3rd party
import folium.elements
import markdown
from folium.template import Template
from folium.utilities import remove_empty
from markdown.inlinepatterns import IMAGE_LINK_RE, ImageInlineProcessor

__author__: str = "Dominic Davis-Foster"
__copyright__: str = "2026 Dominic Davis-Foster"
__license__: str = "MIT License"
__version__: str = "0.1.0b1"
__email__: str = "dominic@davis-foster.co.uk"

__all__ = ["AboutControl", "AboutModal", "render_markdown"]


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

	default_js = [
			(
					"about_button_js",
					f"https://cdn.jsdelivr.net/gh/domdfcoding/folium-about-button@v{__version__}/folium_about_button/about_button.min.js",
					),
			]

	default_css = [
			(
					"fontawesome_css",
					"https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.2.0/css/all.min.css",
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


class AboutModal(folium.elements.JSCSSMixin, folium.elements.MacroElement):
	r"""
	Adds a bootstrap modal with a markdown body, such as for an about dialog.

	:param title: The dialog's title.
	:param markdown_body: The dialog's body, as markdown.
	:param modal_id: The HTML element ID of the modal.
	"""

	def __init__(self, title: str, markdown_body: str, modal_id: str = "aboutModal"):
		super().__init__()
		self._name = "AboutModal"
		self.title = title
		self.markdown_body = markdown_body
		self.modal_id = modal_id

	@property
	def body(self) -> str:
		"""
		The dialog body, as HTML.
		"""

		return self._body

	@property
	def markdown_body(self) -> str:
		"""
		The dialog body, as the markdown input.
		"""

		return self._markdown_body

	@markdown_body.setter
	def markdown_body(self, value: str) -> None:
		self._markdown_body = value
		self._body = render_markdown(value)

	default_js = [
			(
					"bootstrap",
					"https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/js/bootstrap.bundle.min.js",
					),
			]

	default_css = [
			(
					"bootstrap_css",
					"https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/css/bootstrap.min.css",
					),
			]

	_template = Template(
			"""
			{% macro html(this, kwargs) %}
				<div class="modal fade modal-lg"
					id="{{ this.modal_id }}"
					tabindex="-1"
					aria-labelledby="{{ this.modal_id }}Label"
					aria-hidden="true">
					<div class="modal-dialog">
						<div class="modal-content">
							<div class="modal-header">
								<h1 class="modal-title fs-5" id="{{ this.modal_id }}Label">{{ this.title }}</h1>
								<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
							</div>
							<div class="modal-body">
								{{ this.body }}
							</div>
						</div>
					</div>
				</div>
			{% endmacro %}
			""",
			)


class _ImgFluidInlineProcessor(ImageInlineProcessor):
	"""
	Markdown image processor to use bootstrap's ``img-fluid`` class.
	"""

	# TODO: mypy thinks the signature doesn't match the superclass but it matches what's in their docs and the pyright stubs.
	def handleMatch(self, m: Match[str], data: str):  # type: ignore[override]  # noqa: MAN002
		el, start, index = super().handleMatch(m, data)
		assert el is not None
		el.set("class", "img-fluid")  # type: ignore[union-attr]
		return el, start, index


def render_markdown(source: str) -> str:
	"""
	Render the given markdown to HTML.

	:param source:
	"""

	text = source.splitlines()

	md = markdown.Markdown(extensions=["fenced_code", "codehilite", "toc"])
	md.inlinePatterns.register(_ImgFluidInlineProcessor(IMAGE_LINK_RE, md), "image_link", 150)

	while not text[0].strip():
		text.pop(0)

	body = md.convert('\n'.join(text))

	return body
