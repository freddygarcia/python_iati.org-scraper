
import io
import datetime
import pandas


def cad_to_pd(f_content):
    df = pandas.read_csv(io.StringIO(f_content))
    df.set_index('iati-identifier', inplace=True)
    return df

def filename():
    ext = '.xlsx'
    title = 'iati-report'
    return title + ext


def auto_fit_columns(df, worksheet):
    def get_col_widths(dataframe):
        # First we find the maximu  m length of the index column   
        idx_max = max([len(str(s)) for s in dataframe.index.values] + [len(str(dataframe.index.name))])
        # Then, we concatenate this to the max of the lengths of column name and its values for each column, left to right
        return [idx_max] + [max([len(str(s)) for s in dataframe[col].values] + [len(col)]) for col in dataframe.columns]

    for i, width in enumerate(get_col_widths(df)):
        worksheet.set_column(i, i, width)

def save(f_content):

    df = cad_to_pd(f_content)

    # get filename
    f_name = filename()

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pandas.ExcelWriter(f_name, engine='xlsxwriter')

    # Convert the dataframe to an XlsxWriter Excel object.
    df.to_excel(writer, sheet_name='Sheet1')

    # Get the xlsxwriter workbook and worksheet objects.
    workbook  = writer.book
    worksheet = writer.sheets['Sheet1']

    # Add some cell formats.
    # format2 = workbook.add_format({'bold': True})

    # Set the column width and format.
    # worksheet.set_column('A:B', None, format_no_border)

    auto_fit_columns(df, worksheet)

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()

    return f_name
