import pandas as pd
import xlsxwriter
import os


def get_col_widths(df, cols=None, idx=False):
    cols = cols if cols is not None else df.columns
    if idx:
        idx_max = [
            max([len(str(s)) for s in df.index.values] + [len(str(df.index.name))])
        ]
    else:
        idx_max = []
    return idx_max + [
        max([len(str(s)) for s in df[col].values] + [len(col)]) for col in cols
    ]


def save_xlsx(
        df, write_file, sheetname="papers", cols=None, row_height=8
):
    """Read EXCEL file into xlsxwriter workbook worksheet"""

    workbook = xlsxwriter.Workbook(write_file)
    worksheet = workbook.add_worksheet(sheetname)
    worksheet.set_default_row(12 * row_height)

    cellf = dict(
        text_wrap=True,
        right=1,
        align="center",
        valign="vcenter",
        indent=1,
    )
    cell_format = workbook.add_format(cellf)

    idxf = dict(text_wrap=True, bold=True, right=1, align="center", valign="vcenter")
    idx_format = workbook.add_format(idxf)

    headf = dict(
        text_wrap=True,
        bold=True,
        bottom=1,
        right=1,
        align="center",
        valign="vcenter",
    )
    header_format = workbook.add_format(headf)
        
    if os.path.isfile(write_file):
        old = pd.read_excel(write_file).set_index("title")
        # Column "note" is never overwritten:
        df["note"] = old["note"]
        # Columns manually added in xlsx are kept:
        for col in old.columns:
            if col not in df.columns:
                df[col] = old[col]
        
    df = df.fillna("").reset_index()
        
    rows, columns = len(df.index), len(df.columns)
    cols = cols if cols is not None else df.columns

    [
        worksheet.write(0, idx, col, header_format)
        for idx, col in zip(range(columns), cols)
    ]

    [
        worksheet.write(idx + 1, 0, row, idx_format)
        for idx, row in zip(range(rows), df.iloc[:, 0])
    ]

    [
        worksheet.write(row_idx + 1, col_idx, df.loc[row, col], cell_format)
        for row_idx, row in zip(range(rows), df.index)
        for col_idx, col in zip(range(1, columns), cols[1:])
    ]

    for i, width in enumerate(get_col_widths(df, cols)):
        worksheet.set_column(i, i, width / row_height + 15)
        
    worksheet.set_row(0, 30)
        
    workbook.close()