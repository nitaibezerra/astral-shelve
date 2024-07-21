from dataclasses import dataclass
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import HRFlowable, Paragraph, SimpleDocTemplate, Spacer, Flowable
from typing import List

from astral_shelve.pdf_generator.repetition_bar_allocator import LevelAllocator


@dataclass
class Hymn:
    """
    Data class representing a hymn.
    """
    number: int
    title: str
    text: str
    style: str
    repetitions: str


class VerticalLine(Flowable):
    def __init__(self, x, y_start, y_end, thickness=0.7):
        Flowable.__init__(self)
        self.x = x
        self.y_start = y_start
        self.y_end = y_end
        self.thickness = thickness

    def draw(self):
        self.canv.setLineWidth(self.thickness)
        self.canv.line(self.x, self.y_start, self.x, self.y_end)


class HymnPDFGenerator:
    """
    A class to generate a PDF for a given hymn.
    """

    def __init__(self, hymn: Hymn, filename: str):
        """
        Initialize the HymnPDFGenerator with a hymn and output filename.

        :param hymn: An instance of the Hymn data class.
        :param filename: The output PDF filename.
        """
        self.hymn = hymn
        self.filename = filename
        self.pagesize = (288, 432)  # Width: 288 points (4 inches), Height: 432 points (6 inches)
        self.margin = 0.5 * inch
        self.styles = getSampleStyleSheet()
        self._setup_styles()

    def _setup_styles(self):
        """
        Set up custom paragraph styles.
        """
        self.title_style = ParagraphStyle(
            'TitleStyle',
            parent=self.styles['Title'],
            fontName='Times-Roman',
            fontSize=14,
            leading=20,
            spaceAfter=0
        )

        self.body_style = ParagraphStyle(
            'BodyStyle',
            parent=self.styles['BodyText'],
            fontName='Times-Roman',
            fontSize=14,
            leading=16,  # Increased line spacing
            spaceAfter=0.12 * inch
        )

        self.hymn_style_style = ParagraphStyle(
            'RightAlignStyle',
            parent=self.styles['Normal'],
            fontName='Times-Roman',
            fontSize=12,
            alignment=2,  # Right align
            leading=0,
            spaceAfter=22
        )

    def create_pdf(self):
        """
        Create a PDF with the hymn content.
        """
        doc = SimpleDocTemplate(
            self.filename,
            pagesize=self.pagesize,
            leftMargin=self.margin,
            rightMargin=self.margin,
            topMargin=20,
            bottomMargin=self.margin
        )

        elements = self._build_elements()
        doc.build(elements)


    def add_vertical_lines(self, elements):
        allocator = LevelAllocator()
        line_positions = allocator.get_entries_with_levels(self.hymn.repetitions)

        base_y_start = -12
        one_line_hight = 7
        space_between_lines = 9
        levels_distance = 6

        for line in line_positions:
            start_line = line['start'] - 1
            end_line = line['end'] - 1
            level = line['level']

            y_start = (
                base_y_start
                - (start_line * one_line_hight
                   + start_line * space_between_lines)
            )
            y_end = (
                base_y_start
                - (end_line * one_line_hight
                   + end_line * space_between_lines + one_line_hight)
            )

            elements.append(
                VerticalLine(-(level * levels_distance), y_start, y_end))


    def _build_elements(self) -> List[Paragraph]:
        """
        Build the PDF elements from the hymn content.

        :return: A list of Paragraph objects for the PDF.
        """
        elements = []

        # Add number and title
        title = f"{self.hymn.number:02d} {self.hymn.title}"
        elements.append(Paragraph(title, self.title_style))

        # Add horizontal line
        elements.append(HRFlowable(width="100%", thickness=1, color="black", spaceAfter=0))

        # Add hymn style aligned to the right
        elements.append(Paragraph(self.hymn.style, self.hymn_style_style))

        paragraphs = self.hymn.text.strip().split("\n\n")

        # Add vertical lines
        self.add_vertical_lines(elements)

        # Add body paragraphs
        for paragraph in paragraphs:
            elements.append(Paragraph(paragraph.replace("\n", "<br/>"), self.body_style))

        return elements


if __name__ == "__main__":
    # Input hymn data
    hymn = Hymn(
        number=2,
        title="ESTOU AQUI",
        text="""Eu estou aqui
Que o Mestre me mandou
Eu vou citar o nome
O Mestre é Juramidam

O Mestre manda
Eu cantar com os meus irmãos
Para louvar ao Pai Eterno
E a Virgem da Conceição

O Mestre tem
O amor no coração
Ele ama ao Pai Eterno
E também os seus irmãos

Oh! Meu Jesus Cristo
Vós que tem todo poder
Tirai-me destas trevas
Quem não enxerga não vê

Meu senhor Jesus
Que é da soberania
Filho da senhora mãe
A sempre Virgem Maria

Minha senhora mãe
Senhora da Conceição
Guiai-me neste mundo
Livrai-me da tentação""",
        style="Marcha",
        repetitions="1-2,3-4",
    )

    # Output filename
    output_filename = "example-estou-aqui.pdf"

    # Create the PDF
    generator = HymnPDFGenerator(hymn, output_filename)
    generator.create_pdf()
