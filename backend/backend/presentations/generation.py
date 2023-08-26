from __future__ import annotations

from pptx import Presentation
from pptx.slide import Slide
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor


PRESENTATION_WIDTH = Inches(16)
PRESENTATION_HEIGHT = Inches(9)


def add_custom_logo(config, slide: Slide):
    border_offset = Inches(0.25) + Inches(config["logo"]["size"])
    slide.shapes.add_picture(
        config["logo"]["path"],
        PRESENTATION_WIDTH - border_offset,
        PRESENTATION_HEIGHT - border_offset,
        width=Inches(config["logo"]["size"]),
    )


def apply_text_formatting(
    config, obj, color: str = "000000", bold=False, is_title=False
):
    obj.text_frame.paragraphs[0].font.name = config["font"]["name"]
    obj.text_frame.paragraphs[0].font.bold = bold
    obj.text_frame.paragraphs[0].font.color.rgb = RGBColor.from_string(color)
    font_size = (
        config["font"]["title_size"] if is_title else config["font"]["regular_size"]
    )
    obj.text_frame.paragraphs[0].font.size = Pt(font_size)


def set_slide_background(config, slide: Slide):
    background = slide.background
    fill = background.fill
    if config["bg"]["type"] == "gradient":
        fill.gradient()
        fill.gradient_stops[0].color.rgb = RGBColor.from_string(config["bg"]["color1"])
        fill.gradient_stops[1].color.rgb = RGBColor.from_string(config["bg"]["color2"])
        fill.gradient_angle = config["bg"]["angle"]
    elif config["bg"]["type"] == "solid":
        fill.solid()
        fill.fore_color.rgb = RGBColor.from_string(config["bg"]["color"])


def create_title_slide(config, slide: Slide):
    title = slide.shapes.title
    subtitle = slide.placeholders[1]

    title.text = config["name"]
    title.width = PRESENTATION_WIDTH - Inches(2)
    title.left = Inches(1)
    title.top = Inches(3.5)

    subtitle.text = config["brief"]
    subtitle.width = Inches(14)
    subtitle.left = Inches(1)
    subtitle.top = Inches(3.5) + Inches(1)

    apply_text_formatting(config, title, bold=True, is_title=True)
    apply_text_formatting(config, subtitle)


def driver(config, output_path: str):
    prs = Presentation()

    prs.slide_width = PRESENTATION_WIDTH
    prs.slide_height = PRESENTATION_HEIGHT

    slide = prs.slides.add_slide(prs.slide_layouts[0])
    create_title_slide(config, slide)
    set_slide_background(config, slide)
    add_custom_logo(config, prs, slide)

    prs.save(output_path)
