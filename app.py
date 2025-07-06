from dash import Dash, dcc, html, Input, Output, callback, State
#import dash
import pandas as pd
import io
import base64
import gini_coefficient

app = Dash()

app.layout = html.Div([
    html.H6("Upload a 1-column CSV file to see callbacks in action!"),
    dcc.Upload(
        id='upload-data',
        children=html.Button('Upload CSV'),
        multiple=False
    ),
    html.Br(),
    html.Div(id='my-output'),
])

@callback(
    Output('my-output', 'children'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename')
)
def update_output_div(contents, filename):
    if contents is None:
        return "No file uploaded yet."
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), header=None)
        if df.shape[1] != 1:
            return "Please upload a CSV with exactly one column."
        
        result = df.iloc[:, 0].astype(float)
        gini_array = [val for val in result if not pd.isna(val)]
        return html.Div([
            html.H6("Output:"),
            html.H6(f"Gini Coefficient (Pairwise): {gini_coefficient.gini_pairwise(gini_array)}"),
            html.H6(f"Gini Coefficient (Cumulative): {gini_coefficient.gini_cumulative(gini_array)}"),
        ])
    except Exception as e:
        return f"Error processing file: {e}"

if __name__ == '__main__':
    app.run(debug=True)
