import pandas as pd
import glob
# glob is useful here for lists with multiple files
from fpdf import FPDF
from pathlib import Path
# helps with using filepaths


def generate(invoices_path, pdfs_path):
    filepaths = glob.glob("invoices/*.xlsx")
    print(filepaths)

    for filepath in filepaths:

        pdf = FPDF(orientation="P", unit="mm", format="A4")
        pdf.add_page()
        filename = Path(filepath).stem
        # stem extract a property of the file
        # which here will be the name
        invoice_nr = filename.split("-")[0]
        date = filename.split("-")[1]
        # or use invoice_nr, date = filename.split("-")

        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=50, h=8, txt=f"Invoice nr.{invoice_nr}", ln=1)
        # ln=1 indicated that a breakline should be added

        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=50, h=8, txt=f"Date: {date}", ln=1)

        df = pd.read_excel(filepath, sheet_name="Sheet 1")

        columns = list(df.columns)
        #converted to list from object type
        columns = [item.replace("_", " ").title() for item in columns]
        pdf.set_font(family="Times", size=10, style="B")
        pdf.set_text_color(80, 80, 80)
        pdf.cell(w=30, h=8, txt=columns[0], border=1)
        pdf.cell(w=70, h=8, txt=columns[1], border=1)
        pdf.cell(w=30, h=8, txt=columns[2], border=1)
        pdf.cell(w=30, h=8, txt=columns[3], border=1)
        pdf.cell(w=30, h=8, txt=columns[4], border=1, ln=1)

        for index, row in df.iterrows():
            pdf.set_font(family="Times", size=10)
            pdf.set_text_color(80, 80, 80)
            pdf.cell(w=30, h=8, txt=str(row["product_id"]), border=1)
            pdf.cell(w=70, h=8, txt=str(row["product_name"]), border=1)
            pdf.cell(w=30, h=8, txt=str(row["amount_purchased"]), border=1)
            pdf.cell(w=30, h=8, txt=str(row["price_per_unit"]), border=1)
            pdf.cell(w=30, h=8, txt=str(row["total_price"]), border=1, ln=1)
    #str here is to convert integer values to string
    # because they are used in a replace() function
    # and ints cant be used with that function

        total_sum = df["total_price"].sum()
        pdf.set_font(family="Times", size=10)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(w=30, h=8, txt="", border=1)
        pdf.cell(w=70, h=8, txt="", border=1)
        pdf.cell(w=30, h=8, txt="", border=1)
        pdf.cell(w=30, h=8, txt="", border=1)
        pdf.cell(w=30, h=8, txt=str(total_sum), border=1, ln=1)

        pdf.set_font(family="Times", size=10, style="B")
        pdf.cell(w=30, h=8, txt=f"The total price is {total_sum}", ln=1)
        # Add total sum sentence

        pdf.set_font(family="Times", size=14, style="B")
        pdf.cell(w=25, h=8, txt=f"Python")
        pdf.image("pythonhow.png", w=10)
        # Add company name and logo

        pdf.output(f"PDFS/{filename}.pdf")
        # f string useful here
        # because we generate files dynamically from multiple files


        # we create a pdf for each excel
        # that's the logic to use inside for loop

    print(df)
    #reminder prints are good to check step by step the output,
    # but also actions done correctly