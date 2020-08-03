from analysis import analyze
from MakePDF import write_entire_pdf


def serve(file):
    try:
        data = analyze(file)
        write_entire_pdf(data)
    except Exception as e:
        print(e)
        return -1
