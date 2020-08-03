import datetime
import os
from reportlab.lib import colors
from analysis import analyze
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.shapes import Drawing


def create_cover_page(flowables, styles):
    now = datetime.datetime.now()
    timestamp = (
        str(now.month)
        + "/"
        + str(now.day)
        + "/"
        + str(now.year)
        + " "
        + str(now.hour)
        + ":"
        + str(now.minute)
        + ":"
        + str(now.second)
    )
    flowables.append(Spacer(width=0, height=225))
    nyu_title = "New York University College of Arts and Sciences"
    flowables.append(Paragraph(nyu_title, styles["Title"]))
    flowables.append(Spacer(width=0, height=5))
    tcr_title = "Transfer College Report Analysis"
    flowables.append(Paragraph(tcr_title, styles["Title"]))
    flowables.append(Spacer(width=0, height=25))
    time_text = "Generated " + timestamp + " EST"
    flowables.append(Paragraph(time_text, styles["Center"]))
    flowables.append(PageBreak())


def create_table(column_names, data):
    table_data = [column_names] + data
    table_style = [
        ("GRID", (0, 0), (-1, -1), 0.5, "#000"),
        ("BACKGROUND", (0, 0), (-1, 0), "#8900E1"),
        ("FONTNAME", (0, 0), (-1, 0), "Times-Bold"),
    ]
    return Table(table_data, style=table_style)


def write_concern(data, flowables, styles, ptext, column_names):
    flowables.append(Spacer(width=0, height=15))
    flowables.append(Paragraph(ptext, styles["Title"]))
    flowables.append(Spacer(width=0, height=15))
    if sum(data["a"].values()) + sum(data["b"].values()) == 0:
        flowables.append(Paragraph("No data has been recorded so far."))
    else:
        d = {}
        for k in data["a"]:
            d[k] = (k, data["a"].get(k, 0), data["b"].get(k, 0))
        for k in data["b"]:
            d[k] = (k, data["a"].get(k, 0), data["b"].get(k, 0))
        flowables.append(create_table(column_names, list(d.values())))
    flowables.append(PageBreak())


# for country and school concerns
def write_concern_alt(data, flowables, styles, ptexts, column_names):
    if not data:
        flowables.append(Paragraph("No data has been recorded so far."))
    else:
        flowables.append(Spacer(width=0, height=15))
        flowables.append(Paragraph(ptexts[0], styles["Title"]))
        flowables.append(create_table(column_names[0], list(data["a"].items())[0:10]))
        flowables.append(Spacer(width=0, height=15))
        flowables.append(Paragraph(ptexts[1], styles["Title"]))
        flowables.append(create_table(column_names[1], list(data["b"].items())[0:10]))
        flowables.append(Spacer(width=0, height=15))
        flowables.append(PageBreak())


def write_concern_6(data, flowables, styles):
    if not data:
        flowables.append(Paragraph("No data has been recorded so far."))
    else:
        d = {}
        for k in data["a"]:
            d[k] = (k, data["b"].get(k, 0), data["c"].get(k, 0), data["a"].get(k, 0))
        for k in data["b"]:
            d[k] = (k, data["b"].get(k, 0), data["c"].get(k, 0), data["a"].get(k, 0))
        for k in data["c"]:
            d[k] = (k, data["b"].get(k, 0), data["c"].get(k, 0), data["a"].get(k, 0))
        ptext = "Reasons"
        flowables.append(Spacer(width=0, height=15))
        flowables.append(Paragraph(ptext, styles["Title"]))
        flowables.append(Spacer(width=0, height=15))
        column_names = ["Transfer Reasons", "# domestic", "# international", "total"]
        flowables.append(create_table(column_names, list(d.values())))
        flowables.append(PageBreak())


def write_entire_pdf(data):
    outfilename = "analysis.pdf"
    outfiledir = '/tmp'
    outfilepath = os.path.join( outfiledir, outfilename )
    doc = SimpleDocTemplate(outfilepath, pagesize=letter)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="Center", alignment=TA_CENTER))
    flowables = []

    create_cover_page(flowables, styles)

    write_concern(
        data["1"],
        flowables,
        styles,
        "Number of students interested in a transfer.",
        ["int'l status", "total", "met"],
    )

    write_concern_alt(
        data["2"],
        flowables,
        styles,
        ["Countries of Origin: Total", "Countries of Origin: Met"],
        [["country", "total"], ["country", "met"]],
    )

    write_concern(
        data["3"],
        flowables,
        styles,
        "Admissions Decisions of Students",
        ["decision", "total", "met"],
    )

    write_concern_alt(
        data["4"],
        flowables,
        styles,
        ["Top 10 Schools: Total", "Top 10 Schools: Met"],
        [["school", "total"], ["school", "met"]],
    )

    write_concern(
        data["5"], flowables, styles, "Census Results", ["result", "total", "met"]
    )

    write_concern_6(data["6"], flowables, styles)

    write_concern(
        data["7"],
        flowables,
        styles,
        "Results of Indicated Codes",
        ["Transfer Reasons", "Stayed", "Left"],
    )

    write_concern(
        data["8"],
        flowables,
        styles,
        "Stayed/Left vs Met/Not Met",
        ["results", "met", "not met"],
    )
    doc.build(flowables)
