# 3rd party
from coincidence.regressions import AdvancedFileRegressionFixture

# this package
from folium_about_button import render_markdown


def test_complex(advanced_file_regression: AdvancedFileRegressionFixture):
	markdown_body = "## Heading 2\n\n**Bold Text** and *Italic Text*\n\nSome normal text and a link to [Google](https://google.com)"
	advanced_file_regression.check(render_markdown(markdown_body))


def test_edge_cases():
	assert render_markdown('') == ''
	assert render_markdown('\n') == ''
	assert render_markdown('\n   \n\n') == ''
