import dash
import dash_core_components as dcc
import dash_table
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import os
from dash.exceptions import PreventUpdate
import dash_bio as dashbio

from src.processing import Processing
from src.dashView import initializeData

# files, which are processed
# read-only
file_list = None
struct_data = None


# starts dash
# file_list: input data
# port: port
def startDash(files, port,secStruct_data):
    global file_list
    global struct_data
    file_list = files
    struct_data = secStruct_data
    app.run_server(debug=True, host='0.0.0.0', port=port)


# calculates slider ranges
# peak-boolean sets first value to 'none' (for peak-slider)
def markSliderRange(min_val, max_val, peak):
    mark = {}
    if peak:
        min_val += 1
        mark[0] = 'none'
    for i in range(min_val, max_val + 1):
        mark[i] = str(i)
    return mark


# calculation of slider ranges in steps [50, 100, 500, 1000,...,all]
def specialSliderRange(min_val, max_val):
    j = min_val
    mark = {}
    i = 0
    while i < 9:
        if "5" in str(j):
            j = j * 2
        else:
            j = j * 5

        if j <= max_val:
            mark[i] = str(j)
        else:
            break
        i += 1
    mark[i] = 'all'
    return mark


def dropdownRange(min_val, max_val):
    j = min_val
    mark = []
    i = 0
    while i < 9:
        if "5" in str(j):
            j = j * 2
        else:
            j = j * 5

        if j <= max_val:
            mark.append({'label': str(j), 'value': str(i)})
        else:
            break
        i += 1
    mark.append({'label': 'all', 'value': 'all'})
    return mark


# ------------------------------------------- Dash-Layout --------------------------------------------------------------

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.title = "k-Mer Dash"

app.layout = dbc.Container([
    # ------------------------------------------ Store -----------------------------------------------------------------
    dbc.Spinner(children=[dcc.Store(id='memory', storage_type='memory')],
                color="primary", fullscreen=True),

    # -------------------------------------------------------------------------------------------------------------------
    dbc.Card([
        dbc.Row([
            dbc.Col(
                dbc.CardBody([
                    html.H3("Menu"),
                    html.Br(),
                    html.Br(),
                    # ------------------------------------- Select File1 And File 2 ------------------------------------
                    html.H6("Selected Files:"),
                    dbc.Select(
                        id="file1",
                        options=[]),
                    dbc.Select(
                        id="file2",
                        options=[]),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    # ------------------------------------------- K ----------------------------------------------------
                    html.H6("K-mer length:"),
                    dcc.Slider(
                        id='k',
                        min=0,
                        max=10,
                        step=1,
                        value=3,
                        marks=markSliderRange(0, 10, False)
                    ),
                    html.Br(),
                    # ----------------------------------------- Peak ---------------------------------------------------
                    html.H6("Peak-position:"),
                    dcc.Slider(
                        id='peak',
                        min=1,
                        max=10,
                        step=1,
                        value=0,
                        marks=markSliderRange(0, 10, True)
                    ),
                    html.Br(),
                    # ------------------------------------------ top ---------------------------------------------------
                    html.H6("Top-values:"),
                    dbc.Select(
                        id='top',
                        options=[
                            {'label': '10', 'value': '0'},
                            {'label': '20', 'value': '1'},
                            {'label': '50', 'value': '2'},
                            {'label': '100', 'value': '3'}
                        ],
                        value="0"
                    ),
                    html.Br(),
                    html.Br(),
                    # -------------------------------- Highlighted Feature ---------------------------------------------
                    html.H6("Highlighted Feature:"),
                    dbc.Select(
                        id="Feature",
                        options=[
                            {"label": "Frequency", "value": "1"},
                            {"label": "T Occurrences", "value": "2"},
                        ],
                        value="1"
                    ),
                    html.Br(),
                    html.Br(),
                    html.Br(),

                ], style={
                    'height': '100vh',
                    'left': '0px',
                    'background': 'lightgrey'}),
                width=2,
                style={"padding-right": '0px',
                       "padding-left": '0px',
                       'margin-right': '0px'}),

            # --------------------------------------- ScatterPlot ------------------------------------------------------
            dbc.Col([
                dbc.Card([
                    dbc.Spinner(children=[
                        dcc.Tabs(value="s-tab", children=[
                            dcc.Tab(label="Scatterplot", value='s-tab', id="s-tab1", children=[
                                dcc.Graph(figure={}, id="scatter", style={'height': '40vh'})
                            ]),
                            dcc.Tab(label="RNA-Structure", value='r-tab', id="s-tab2", children=[
                                dbc.Card(
                                    dashbio.FornaContainer(
                                        id='forna',height='300',width='400'
                                    ),
                                className="w-100 p-3"
                                ),
                            ]),
                        ]),
                    ],
                        color="primary", spinner_style={'position': 'absolute',
                                                        'top': '50%',
                                                        'left': '50%'
                                                        }),

                ], style={
                    'background': '#f2f2f2', 'height': '50vh'}, outline=True),

                # -------------------------------------------- TopK ----------------------------------------------------
                dbc.Spinner(children=[dbc.Card(id="topK", children=[], style={
                    'background': '#f2f2f2', 'height': '49vh', 'overflow-y': 'scroll'}, outline=True)],
                            color="primary", spinner_style={'position': 'absolute',
                                                            'top': '50%',
                                                            'left': '50%'
                                                            }),
            ],
                width=5,
                style={"padding-right": '5px',
                       "padding-left": '10px'}),

            # ------------------------------------------------- PCAs ---------------------------------------------------
            dbc.Col(
                [dbc.Card([
                    dbc.Spinner(children=[
                        dcc.Tabs(id='tabs-example', value='Tab1', children=[
                            dcc.Tab(label="", value='Tab1', id="Tab1", children=[
                                dcc.Graph(figure={}, id="PCA1",
                                          style={'height': '42vh'}
                                          )
                            ]),
                            dcc.Tab(label="", value='Tab2', id="Tab2", children=[
                                dcc.Graph(figure={}, id="PCA2",
                                          style={'height': '42vh'}
                                          )
                            ]),
                        ],
                                 )], color="primary",
                        spinner_style={'position': 'absolute',
                                       'top': '50%',
                                       'left': '50%'
                                       }),

                ], style={
                    'background': '#f2f2f2', 'height': '50vh'}, outline=True),

                    # ------------------------------------------- MSA --------------------------------------------------
                    dbc.Spinner(children=[dbc.Card(id="msa", children=[], style={
                        'background': '#f2f2f2', 'height': '49vh', 'overflow-y': 'scroll'}, outline=True)],
                                color="primary", spinner_style={'position': 'absolute',
                                                                'top': '50%',
                                                                'left': '50%'
                                                                }),
                ],
                width=5,
                style={"padding-right": '0px',
                       "padding-left": '0px'}
            )

        ], style={'padding-top': '0px', 'padding-bottom': '0px', 'margin-top': '0px', 'margin-bottom': '0px',
                  'margin-left': '0px', 'padding-left': '0px'},
            className="mw-100 mh-100"
        ),

    ],
        className="mw-100 mh-100"),
], className="mw-100 mh-100", style={'left': '0px', 'margin-left': '0px', 'padding': '0px'})


# ------------------------------------ Store Callback ------------------------------------------------------------------

@app.callback(
    dash.dependencies.Output('memory', 'data'),
    dash.dependencies.Input('file1', 'value'),
    dash.dependencies.Input('file2', 'value'),
    dash.dependencies.Input('k', 'value'),
    dash.dependencies.Input('peak', 'value'),
    dash.dependencies.Input('top', 'value'),
    dash.dependencies.Input('Feature', 'value'),
    dash.dependencies.State('memory', 'data'),
)
# calculates new data for tables/diagrams
# k: kmer length
# peak: peak: peak-position, where sequences should be aligned
# top: number of best values
# pca_feature: number of T or kmer-Frequency for pcas
# data: storage to share data between callbacks
def updateData(f1, f2, k, peak, top, pca_feature, data):
    top_opt_val = {'0': 10, '1': 20, '2': 50, '3': 100}

    top = top_opt_val[top]

    if peak is 0:
        peak = None

    if data is None:
        selected = [file_list[0], file_list[1]]
    else:
        selected = [file_list[int(f1)], file_list[int(f2)]]

    new_process = initializeData.initData(selected, selected, k, peak, top, pca_feature,struct_data)

    # calculate top-table
    top_k = Processing.getTopKmer(new_process).copy()
    kmer = top_k.index
    top_k["K-Mer"] = kmer
    top_k[""] = ["" for i in range(0, len(top_k))]
    top_k = top_k[["", "K-Mer", "Frequency", "File"]]
    top_k = top_k.sort_values(by="Frequency", ascending=False)
    top_k_table = [
        dash_table.DataTable(columns=[{"name": i, "id": i} for i in top_k.columns], data=top_k.to_dict('records'),
                             style_table={'overflow-x': 'hidden'},
                             style_cell={'textAlign': 'center'},
                             export_format="csv",
                             sort_action='native')]

    # calculate MSA

    algn1, algn2, f1_name, f2_name = initializeData.getAlignmentData(new_process)

    # if cols differ in their length, need to do some adaptions

    if (len(algn1) > 1) and (len(algn2) > 1):
        algn1_df = pd.DataFrame(columns=[f1_name], data=algn1)
        algn2_df = pd.DataFrame(columns=[f2_name], data=algn2)
        algn1_df = pd.concat([algn1_df, algn2_df], ignore_index=False, axis=1)
        msas = [
            dash_table.DataTable(columns=[{"name": i, "id": i} for i in algn1_df.columns],
                                 data=algn1_df.to_dict('records'),
                                 style_table={'overflow-x': 'hidden'},
                                 style_cell={'textAlign': 'center'},
                                 export_format="csv")]
    elif len(algn1) <= 1 and len(algn2) <= 1:
        algn1 = ['No data to align']
        algn2 = ['No data to align']

        algn1_df = pd.DataFrame(columns=[f1_name], data=algn1)
        algn2_df = pd.DataFrame(columns=[f2_name], data=algn2)
        algn1_df = pd.concat([algn1_df, algn2_df], ignore_index=False, axis=1)
        msas = [
            dash_table.DataTable(columns=[{"name": i, "id": i} for i in algn1_df.columns],
                                 data=algn1_df.to_dict('records'),
                                 style_table={'overflow-x': 'hidden'},
                                 style_cell={'textAlign': 'center'},
                                 export_format="csv")]

    else:
        if len(algn1) <= 1:
            algn1 = ['No data to align']

            algn1_df = pd.DataFrame(columns=[f1_name], data=algn1)
            algn2_df = pd.DataFrame(columns=[f2_name], data=algn2)
            algn1_df = pd.concat([algn1_df, algn2_df], ignore_index=False, axis=1)
        else:
            algn2 = ['No data to align']

            algn1_df = pd.DataFrame(columns=[f1_name], data=algn1)
            algn2_df = pd.DataFrame(columns=[f2_name], data=algn2)
            algn1_df = pd.concat([algn1_df, algn2_df], ignore_index=False, axis=1)

        msas = [dash_table.DataTable(columns=[{"name": i, "id": i} for i in algn1_df.columns],
                                     data=algn1_df.to_dict('records'),
                                     style_table={'overflow-x': 'hidden'},
                                     style_cell={'textAlign': 'center'},
                                     export_format="csv")]

    # calculate scatterplot

    scatter = initializeData.getScatterPlot(new_process)

    # calculate PCAs

    pca_12, file1, file2 = initializeData.getPCA(new_process)
    pcas = [pca_12, file1, file2]

    seq_len = new_process.getSeqLen()

    data = {'topK': top_k_table, 'msas': msas, 'scatter': scatter, 'pcas': pcas, 'seqLen': seq_len}

    return data


# --------------------------------------- File Dropdown Updater --------------------------------------------------------
@app.callback([
    dash.dependencies.Output("file1", "value"),
    dash.dependencies.Output("file2", "value"),
    dash.dependencies.Input('memory', 'modified_timestamp'),
])
def initialSelect(ts):
    if ts is None:
        f1 = "0"
        f2 = "1"
    else:
        raise PreventUpdate

    return f1, f2


@app.callback([
    dash.dependencies.Output("file1", "options"),
    dash.dependencies.Input("file2", "value"),
])
def updateFile1Dropdown(f2):
    return updateFileList(f2)


@app.callback([
    dash.dependencies.Output("file2", "options"),
    dash.dependencies.Input("file1", "value"),
])
def updateFile2Dropdown(f1):
    return updateFileList(f1)


def updateFileList(val):
    option = [
        {'label': os.path.basename(file_list[i]), 'value': str(i)} if not (str(i) == val)
        else {'label': os.path.basename(file_list[i]), 'value': str(i), 'disabled': True}
        for i in range(0, len(file_list))]

    return [option]


# --------------------------------------- Slider Values Updater --------------------------------------------------------


@app.callback(
    [
        dash.dependencies.Output("k", "min"),
        dash.dependencies.Output("k", "max"),
        dash.dependencies.Output("k", "marks"),
        dash.dependencies.Output("peak", "min"),
        dash.dependencies.Output("peak", "max"),
        dash.dependencies.Output("peak", "marks"),
    ],
    [
        dash.dependencies.Input("file1", "value"),
        dash.dependencies.Input("file2", "value"),
        dash.dependencies.Input('memory', 'modified_timestamp'),
        dash.dependencies.State('memory', 'data'),
    ],
)
# calculates slider ranges (marks)
# fil1/file2: input file
# ts: timestamp when data was modified
# data: storage to share data between callbacks
def updateSliderRange(file1, file2, ts, data):
    if ts is None:
        raise PreventUpdate
    k_p_slider_max = data['seqLen']
    k_p_slider_min = 2

    k_slider_max = k_p_slider_max - 1
    peak_min = 0

    # calculation of new slider ranges, if files were changed or if dataframe-size was changed (for top-slider)

    k_range = markSliderRange(k_p_slider_min, k_slider_max, False)
    peak_range = markSliderRange(peak_min, k_p_slider_max, True)

    return k_p_slider_min, k_slider_max, k_range, peak_min, k_p_slider_max, peak_range


# ---------------------- test

@app.callback(
    dash.dependencies.Output('forna', 'sequences'),
    [dash.dependencies.Input('memory', 'data')]
)
def show_selected_sequences(data):
    if data is None:
        raise PreventUpdate

    sequences = [{
        'sequence': 'AUGGGCCCGGGCCCAAUGGGCCCGGGCCCA',
        'structure': '.((((((())))))).((((((()))))))'
    }]
    return sequences


# --------------------------------------------- Diagram/Table Updater --------------------------------------------------

# Tables/Diagrams only get updated figures/datatables here

@app.callback(dash.dependencies.Output('scatter', 'figure'),
              dash.dependencies.Input('memory', 'modified_timestamp'),
              dash.dependencies.State('memory', 'data'))
# ts: timestamp when data was modified
# data: storage to share data between callbacks
def updateScatter(ts, data):
    if ts is None:
        raise PreventUpdate
    return data.get('scatter', 0)


@app.callback([dash.dependencies.Output('PCA1', 'figure'),
               dash.dependencies.Output('PCA2', 'figure'),
               dash.dependencies.Output('Tab1', 'label'),
               dash.dependencies.Output('Tab2', 'label')],
              dash.dependencies.Input('memory', 'modified_timestamp'),
              dash.dependencies.State('memory', 'data'))
# ts: timestamp when data was modified
# data: storage to share data between callbacks
def updateScatter(ts, data):
    if ts is None:
        raise PreventUpdate
    pca_data = data.get('pcas', 0)
    pca1 = pca_data[0][0]
    pca2 = pca_data[0][1]
    file1 = pca_data[1]
    file2 = pca_data[2]
    return [pca1, pca2, file1, file2]


@app.callback(dash.dependencies.Output('topK', 'children'),
              dash.dependencies.Input('memory', 'modified_timestamp'),
              dash.dependencies.State('memory', 'data'))
# ts: timestamp when data was modified
# data: storage to share data between callbacks
def updateTopK(ts, data):
    if ts is None:
        raise PreventUpdate
    return data.get('topK', 0)


@app.callback(dash.dependencies.Output('msa', 'children'),
              dash.dependencies.Input('memory', 'modified_timestamp'),
              dash.dependencies.State('memory', 'data'))
# ts: timestamp when data was modified
# data: storage to share data between callbacks
def updateMSA(ts, data):
    if ts is None:
        raise PreventUpdate
    return data.get('msas', 0)
