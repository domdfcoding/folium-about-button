# stdlib
import re

# 3rd party
from coincidence.regressions import AdvancedFileRegressionFixture
from domdf_folium_tools import set_branca_random_seed
from folium import Map

# this package
from folium_about_button import AboutControl, AboutModal


def test_generation(advanced_file_regression: AdvancedFileRegressionFixture):
	set_branca_random_seed("ZOOM")

	m = Map(location=(45.5236, -122.6750))
	modal = AboutModal(
			title="About",
			markdown_body="## Heading 2\n\n**Bold Text** and *Italic Text*\n\nSome normal text and a link to [Google](https://google.com)",
			modal_id="ExampleModal",
			).add_to(m)
	AboutControl(modal.modal_id).add_to(m)

	root = m.get_root()
	html = root.render()
	html = re.sub(
			"folium-about-button@v.*/folium_about_button",
			"folium-about-button@latest/folium_about_button",
			html,
			)
	advanced_file_regression.check(html, extension=".html")


def test_classes(advanced_file_regression: AdvancedFileRegressionFixture):
	set_branca_random_seed("ZOOM")

	m = Map(location=(45.5236, -122.6750))
	modal = AboutModal(
			title="About",
			markdown_body="## Heading 2\n\n**Bold Text** and *Italic Text*\n\nSome normal text and a link to [Google](https://google.com)",
			modal_id="ExampleModal",
			title_extra_classes=iter(["fs-4", "custom-class"]),
			body_extra_classes=["modal-body-custom-class"],
			).add_to(m)
	AboutControl(modal.modal_id).add_to(m)

	root = m.get_root()
	html = root.render()
	html = re.sub(
			"folium-about-button@v.*/folium_about_button",
			"folium-about-button@latest/folium_about_button",
			html,
			)
	advanced_file_regression.check(html, extension=".html")


def test_set_body(advanced_file_regression: AdvancedFileRegressionFixture):
	set_branca_random_seed("ZOOM")

	m = Map(location=(45.5236, -122.6750))
	modal = AboutModal(
			title="About",
			markdown_body="## Heading 2\n\n**Bold Text** and *Italic Text*\n\nSome normal text and a link to [Google](https://google.com)",
			modal_id="ExampleModal",
			).add_to(m)
	AboutControl(modal.modal_id).add_to(m)

	modal.markdown_body = "Simple Body"
	assert modal.markdown_body == "Simple Body"

	root = m.get_root()
	html = root.render()
	html = re.sub(
			"folium-about-button@v.*/folium_about_button",
			"folium-about-button@latest/folium_about_button",
			html,
			)
	advanced_file_regression.check(html, extension=".html")


def test_image(advanced_file_regression: AdvancedFileRegressionFixture):
	set_branca_random_seed("ZOOM")

	m = Map(location=(45.5236, -122.6750))
	modal = AboutModal(
			title="About",
			markdown_body="### Legend\n\n![](https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Us_map_legend.svg/250px-Us_map_legend.svg.png)",
			modal_id="ExampleModal",
			).add_to(m)
	AboutControl(modal.modal_id).add_to(m)

	root = m.get_root()
	html = root.render()
	html = re.sub(
			"folium-about-button@v.*/folium_about_button",
			"folium-about-button@latest/folium_about_button",
			html,
			)
	advanced_file_regression.check(html, extension=".html")
