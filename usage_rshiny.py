import dash_bio
import dash
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_table_experiments as dt
import graph_data as data
import base64
import datetime
import io
import pandas as pd
import json
import circos_parser as circos_parser

empty = dash_bio.DashCircos(
    id="main-circos", selectEvent={}, layout=[], size=800, config={}, tracks=[]
)


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(",")

    decoded = base64.b64decode(content_string).decode("UTF-8")
    try:
        if "csv" in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(io.StringIO(decoded))
            df = df.to_dict(orient="records")
            return df
    except Exception as e:
        print(e)
        return html.Div(["There was an error processing this file."])
    return


app = dash.Dash("")

app.scripts.config.serve_locally = True

app.layout = html.Div(
    [
        html.Div(
            id="container",
            style={"background-color": "#119DFF"},
            children=[
                html.H2("Dash Bio: Circos Graph Selector"),
                html.A(
                    html.Img(
                        src="https://s3-us-west-1.amazonaws.com/plotly-tutorials/excel/dash-daq/dash-daq-logo-by-plotly-stripe+copy.png"
                    ),
                    href="http://www.dashdaq.io",
                ),
            ],
            className="banner",
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                dt.DataTable(
                                                    id="data-table",
                                                    rows=[{}],
                                                    row_selectable=True,
                                                    filterable=True,
                                                    sortable=True,
                                                    selected_row_indices=[],
                                                    editable=False,
                                                    min_height="35vh",
                                                ),
                                                html.Div(id="expected-index"),
                                            ],
                                            style={"height": "10%"},
                                        ),
                                        html.Div(
                                            [
                                                html.Div(
                                                    [
                                                        html.H5("Select Circos Graph"),
                                                        dcc.Dropdown(
                                                            id="circos-selector",
                                                            options=[
                                                                {
                                                                    "label": "Custom",
                                                                    "value": "custom",
                                                                },
                                                                {
                                                                    "label": "Heatmap",
                                                                    "value": "heatmap",
                                                                },
                                                                {
                                                                    "label": "Chords",
                                                                    "value": "chords",
                                                                },
                                                                {
                                                                    "label": "Highlight",
                                                                    "value": "highlight",
                                                                },
                                                                {
                                                                    "label": "Histogram",
                                                                    "value": "histogram",
                                                                },
                                                                {
                                                                    "label": "Line",
                                                                    "value": "line",
                                                                },
                                                                {
                                                                    "label": "Scatter",
                                                                    "value": "scatter",
                                                                },
                                                                {
                                                                    "label": "Stack",
                                                                    "value": "stack",
                                                                },
                                                                {
                                                                    "label": "Text",
                                                                    "value": "text",
                                                                },
                                                            ],
                                                            value="chords",
                                                        ),
                                                    ],
                                                    className="six columns",
                                                ),
                                                html.Div(
                                                    [
                                                        html.H5("Size Slider"),
                                                        html.Div(
                                                            [
                                                                dcc.Slider(
                                                                    id="size-slider",
                                                                    marks={
                                                                        600: "Min",
                                                                        800: "Max",
                                                                    },
                                                                    min=600,
                                                                    max=800,
                                                                    step=10,
                                                                    value=750,
                                                                )
                                                            ],
                                                            style={
                                                                "paddingLeft": "3.5%"
                                                            },
                                                        ),
                                                    ],
                                                    className="six columns",
                                                ),
                                            ],
                                            className="row",
                                            style={"marginTop": "2.5%"},
                                        ),
                                        html.Div(
                                            [
                                                html.Div(
                                                    [
                                                        html.H5("Select Data Set"),
                                                        dcc.Dropdown(
                                                            id="data-selector",
                                                            options=[
                                                                {
                                                                    "label": "Layout",
                                                                    "value": "layout",
                                                                }
                                                            ],
                                                            value="layout",
                                                        ),
                                                    ],
                                                    className="six columns",
                                                ),
                                                html.Div(
                                                    [
                                                        html.H5("Hover/Click Data"),
                                                        dcc.Textarea(
                                                            id="event-data",
                                                            placeholder="Hover or click on data to see it here!",
                                                            value="Hover or click on data to see it here!",
                                                            style={"width": "100%"},
                                                        ),
                                                    ],
                                                    className="six columns",
                                                ),
                                            ],
                                            className="row",
                                            style={"marginTop": "2.5%"},
                                        ),
                                        html.Div(
                                            [
                                                html.Div(
                                                    [
                                                        html.H5(
                                                            "Upload Custom Data",
                                                            className="six columns",
                                                        ),
                                                        html.Button(
                                                            "Render",
                                                            id="render-button",
                                                            style={
                                                                "marginTop": "0.5%",
                                                                "marginBottom": "2%",
                                                            },
                                                            className="three columns",
                                                        ),
                                                        html.A(
                                                            html.Button(
                                                                "Download Data"
                                                            ),
                                                            href="https://github.com/plotly/dash-bio/blob/dash-circos/upload_data/Data/Download.rar",
                                                            target="_blank",
                                                            className="three columns",
                                                            style={
                                                                "margin-top": "0.5%",
                                                                "margin-bottom": "2%",
                                                            },
                                                        ),
                                                    ],
                                                    className="row",
                                                    style={"marginTop": "2.5%"},
                                                ),
                                                html.Div(
                                                    [
                                                        dcc.Upload(
                                                            id="upload-data",
                                                            children=html.Div(
                                                                [
                                                                    "1. Set Circos to Custom. 2. Select Dataset. 3. Drag and Drop .CSV for each Dataset"
                                                                ]
                                                            ),
                                                            style={
                                                                "width": "100%",
                                                                "height": "10vh",
                                                                "lineHeight": "10vh",
                                                                "borderWidth": "1px",
                                                                "borderStyle": "dashed",
                                                                "borderRadius": "3px",
                                                                "textAlign": "center",
                                                                "margin": "10px",
                                                            },
                                                            multiple=True,
                                                        )
                                                    ],
                                                    className="twelve columns",
                                                ),
                                            ],
                                            className="row",
                                        ),
                                    ],
                                    className="five columns",
                                ),
                                html.Div(
                                    id="circos-hold",
                                    children=[
                                        dash_bio.DashCircos(
                                            id="main-circos",
                                            selectEvent={"0": "hover", "1": "hover"},
                                            layout=data.month_layout,
                                            config={
                                                "innerRadius": (650 / 2 - 80),
                                                "outerRadius": (650 / 2 - 30),
                                                "ticks": {"display": False},
                                                "labels": {
                                                    "position": "center",
                                                    "display": True,
                                                    "size": 14,
                                                    "color": "#000",
                                                    "radialOffset": 15,
                                                },
                                            },
                                            tracks=[
                                                {
                                                    "type": "HEATMAP",
                                                    "data": data.heatmap,
                                                    "config": {
                                                        "innerRadius": 0.8,
                                                        "outerRadius": 0.98,
                                                        "logScale": False,
                                                        "color": "YlOrRd",
                                                        "tooltipContent": {
                                                            "name": "value"
                                                        },
                                                    },
                                                },
                                                {
                                                    "type": "HEATMAP",
                                                    "data": data.heatmap,
                                                    "config": {
                                                        "innerRadius": 0.7,
                                                        "outerRadius": 0.79,
                                                        "logScale": False,
                                                        "color": "Blues",
                                                        "tooltipContent": {
                                                            "name": "value"
                                                        },
                                                    },
                                                },
                                            ],
                                            size=800,
                                            style={
                                                "display": "flex",
                                                "justify-content": "center",
                                            },
                                        )
                                    ],
                                    className="seven columns",
                                ),
                            ],
                            className="row",
                        ),
                        html.Div(
                            [
                                html.Div(id="slider-hold"),
                                html.Div(id="data-table-hold"),
                                html.Div(id="click-data"),
                                html.Div(id="hover-data"),
                                html.Div(id="output-data-upload"),
                                dcc.Interval(id="init", n_intervals=0, interval=1000),
                            ],
                            style={"display": "none"},
                        ),
                    ]
                )
            ]
        ),
    ]
)


@app.callback(
    Output("init", "interval"), 
    [Input("init", "n_intervals")]
    )
def update_output(init):
    if init >= 1:
        return 10000000000000
    return 1000


@app.callback(
    Output("data-selector", "options"),
    [Input("circos-hold", "children"), 
    Input("circos-selector", "value")],
    [State("main-circos", "tracks")],
)
def event_dropdown(dropdown, circos_select, tracks):
    if tracks is not None and circos_select != "custom":
        array = []
        dropdown = []

        for k, v in [(k, v) for x in tracks for (k, v) in x.items()]:
            if k == "type":
                array.append(v)

        for i in range(len(tracks)):
            dropdown.append({"label": "{}".format(array[i]), "value": i})
        dropdown.append({"label": "LAYOUT", "value": "layout"}.copy())
        return dropdown
    elif circos_select == "custom":
        dropdown = [
            {"label": "Layout", "value": 0},
            {"label": "Track One", "value": 1},
            {"label": "Track Two", "value": 2},
        ]
        return dropdown
    else:
        return ["blank"]


@app.callback(
    Output("output-data-upload", "children"),
    [Input("upload-data", "contents")],
    [State("upload-data", "filename"),
    State("upload-data", "last_modified"),
    State("output-data-upload", "children"),
    State("data-selector", "value"),
    State("circos-selector", "value")]
)
def update_output(
    list_of_contents, list_of_names, list_of_dates, data, upload_select, circos_select
):
    if data == None:
        array = [None, None, None]
    else:
        array = json.loads(data)

    if list_of_contents is not None:
        children = list(
            (
                parse_contents(c, n, d)
                for c, n, d in zip(list_of_contents, list_of_names, list_of_dates)
            )
        )
        children = children[0]
        array[upload_select] = children
        return json.dumps(array)
    return


@app.callback(
    Output("circos-hold", "children"),
    [
        Input("circos-selector", "value"),
        Input("size-slider", "value"),
        Input("init", "n_intervals"),
        Input("render-button", "n_clicks"),
    ],
    [State("output-data-upload", "children")],
)
def init(circos_select, size, init_onstart, render_button, uploadData):
    if circos_select == "custom" and uploadData != None:
        array = json.loads(uploadData)
        return dash_bio.DashCircos(
            id="main-circos",
            selectEvent={"0": "hover", "1": "click"},
            layout=array[0],
            config={
                "innerRadius": size / 2 - 80,
                "outerRadius": size / 2 - 40,
                "ticks": {"display": True, "labelDenominator": 1000000},
                "labels": {
                    "position": "center",
                    "display": True,
                    "size": 12,
                    "color": "#000",
                    "radialOffset": 70,
                },
            },
            tracks=[
                {
                    "type": "HIGHLIGHT",
                    "data": array[1],
                    "config": {
                        "innerRadius": size / 2 - 80,
                        "outerRadius": size / 2 - 40,
                        "opacity": 0.3,
                        "tooltipContent": {"name": "block_id"},
                        "color": {"name": "color"},
                    },
                },
                {
                    "type": "HIGHLIGHT",
                    "data": array[2],
                    "config": {
                        "innerRadius": size / 2 - 80,
                        "outerRadius": size / 2 - 40,
                        "opacity": 0.3,
                        "tooltipContent": {"name": "block_id"},
                        "color": {"name": "color"},
                    },
                },
            ],
            size=800,
            style={"display": "flex", "justify-content": "center"},
        )
    elif circos_select == "heatmap":
        return dash_bio.DashCircos(
            id="main-circos",
            selectEvent={"0": "hover", "1": "hover"},
            layout=data.month_layout,
            config={
                "innerRadius": (size / 2 - 80),
                "outerRadius": (size / 2 - 30),
                "ticks": {"display": False},
                "labels": {
                    "position": "center",
                    "display": True,
                    "size": 14,
                    "color": "#000",
                    "radialOffset": 15,
                },
            },
            tracks=[
                {
                    "type": "HEATMAP",
                    "data": data.heatmap,
                    "config": {
                        "innerRadius": 0.8,
                        "outerRadius": 0.98,
                        "logScale": False,
                        "color": "YlOrRd",
                        "tooltipContent": {"name": "value"},
                    },
                },
                {
                    "type": "HEATMAP",
                    "data": data.heatmap,
                    "config": {
                        "innerRadius": 0.7,
                        "outerRadius": 0.79,
                        "logScale": False,
                        "color": "Blues",
                        "tooltipContent": {"name": "value"},
                    },
                },
            ],
            size=800,
            style={"display": "flex", "justify-content": "center"},
        )
    elif circos_select == "chords":
        return dash_bio.DashCircos(
            id="main-circos",
            selectEvent={"0": "both", "1": "both"},
            layout=data.GRCh37,
            config={
                "innerRadius": size / 2 - 80,
                "outerRadius": size / 2 - 40,
                "ticks": {"display": False, "labelDenominator": 1000000},
                "labels": {
                    "position": "center",
                    "display": True,
                    "size": 14,
                    "color": "#000",
                    "radialOffset": 70,
                },
            },
            tracks=[
                {
                    "type": "HIGHLIGHT",
                    "data": data.cytobands,
                    "config": {
                        "innerRadius": size / 2 - 80,
                        "outerRadius": size / 2 - 40,
                        "opacity": 0.3,
                        "tooltipContent": {"name": "all"},
                        "color": {"name": "color"},
                    },
                },
                {
                    "type": "CHORDS",
                    "data": data.chords,
                    "config": {
                        "logScale": False,
                        "opacity": 0.7,
                        "color": "#ff5722",
                        "tooltipContent": {
                            "source": "source",
                            "sourceID": "id",
                            "target": "target",
                            "targetID": "id",
                            "targetEnd": "end",
                        },
                    },
                },
            ],
            size=800,
            style={"display": "flex", "justify-content": "center"},
        )
    elif circos_select == "highlight":
        return dash_bio.DashCircos(
            id="main-circos",
            selectEvent={"0": "hover", "1": "hover"},
            layout=data.GRCh37,
            config={
                "innerRadius": size / 2 - 100,
                "outerRadius": size / 2 - 50,
                "ticks": {"display": False},
                "labels": {"display": False},
            },
            tracks=[
                {
                    "type": "HIGHLIGHT",
                    "data": data.cytobands,
                    "config": {
                        "innerRadius": size / 2 - 100,
                        "outerRadius": size / 2 - 50,
                        "opacity": 0.5,
                        "tooltipContent": {"name": "name"},
                        "color": {"name": "color"},
                    },
                }
            ],
            size=800,
            style={"display": "flex", "justify-content": "center"},
        )

    elif circos_select == "histogram":
        return dash_bio.DashCircos(
            id="main-circos",
            layout=data.GRCh37,
            config={
                "innerRadius": size / 2 - 150,
                "outerRadius": size / 2 - 120,
                "ticks": {"display": False, "labelDenominator": 1000000},
                "labels": {"display": False},
            },
            tracks=[
                {
                    "type": "HIGHLIGHT",
                    "data": data.cytobands,
                    "config": {
                        "innerRadius": size / 2 - 150,
                        "outerRadius": size / 2 - 120,
                        "opacity": 0.6,
                        "tooltipContent": {"name": "name"},
                        "color": {"name": "color"},
                    },
                },
                {
                    "type": "HISTOGRAM",
                    "data": data.histogram,
                    "config": {
                        "innerRadius": 1.01,
                        "outerRadius": 1.4,
                        "color": "OrRd",
                        "tooltipContent": {"name": "value"},
                    },
                },
            ],
            size=800,
            style={"display": "flex", "justify-content": "center"},
        )
    elif circos_select == "line":
        return dash_bio.DashCircos(
            id="main-circos",
            layout=list(
                filter(lambda d: d["id"] in ["chr1", "chr2", "chr3"], data.GRCh37)
            ),
            config={
                "innerRadius": size / 2 - 150,
                "outerRadius": size / 2 - 130,
                "ticks": {"display": False, "spacing": 1000000, "labelSuffix": ""},
                "labels": {
                    "position": "center",
                    "display": False,
                    "size": 14,
                    "color": "#000",
                    "radialOffset": 30,
                },
            },
            tracks=[
                {
                    "type": "HIGHLIGHT",
                    "data": list(
                        filter(
                            lambda d: d["block_id"] in ["chr1", "chr2", "chr3"],
                            data.cytobands,
                        )
                    ),
                    "config": {
                        "innerRadius": size / 2 - 150,
                        "outerRadius": size / 2 - 130,
                        "opacity": 0.3,
                        "tooltipContent": {"name": "name"},
                        "color": {"name": "color"},
                    },
                },
                {
                    "type": "LINE",
                    "data": data.snp250,
                    "config": {
                        "innerRadius": 0.5,
                        "outerRadius": 0.8,
                        "color": "#222222",
                        "tooltipContent": {
                            "source": "block_id",
                            "target": "position",
                            "targetEnd": "value",
                        },
                        "axes": [
                            {"spacing": 0.001, "thickness": 1, "color": "#666666"}
                        ],
                        "backgrounds": [
                            {
                                "start": 0,
                                "end": 0.002,
                                "color": "#f44336",
                                "opacity": 0.5,
                            },
                            {
                                "start": 0.006,
                                "end": 0.015,
                                "color": "#4caf50",
                                "opacity": 0.5,
                            },
                        ],
                        "maxGap": 1000000,
                        "min": 0,
                        "max": 0.015,
                    },
                },
                {
                    "type": "SCATTER",
                    "data": data.snp250,
                    "config": {
                        "innerRadius": 0.5,
                        "outerRadius": 0.8,
                        "min": 0,
                        "max": 0.015,
                        "fill": False,
                        "strokeWidth": 0,
                        "tooltipContent": {
                            "source": "block_id",
                            "target": "position",
                            "targetEnd": "value",
                        },
                    },
                },
                {
                    "type": "LINE",
                    "data": data.snp,
                    "config": {
                        "innerRadius": 1.01,
                        "outerRadius": 1.15,
                        "maxGap": 1000000,
                        "min": 0,
                        "max": 0.015,
                        "color": "#222222",
                        "tooltipContent": {"name": "value"},
                        "axes": [
                            {"position": 0.002, "color": "#f44336"},
                            {"position": 0.006, "color": "#4caf50"},
                        ],
                    },
                },
                {
                    "type": "LINE",
                    "data": data.snp1m,
                    "config": {
                        "innerRadius": 1.01,
                        "outerRadius": 1.15,
                        "maxGap": 1000000,
                        "min": 0,
                        "max": 0.015,
                        "color": "#f44336",
                        "tooltipContent": {"name": "value"},
                    },
                },
                {
                    "type": "LINE",
                    "data": data.snp,
                    "config": {
                        "innerRadius": 0.85,
                        "outerRadius": 0.95,
                        "maxGap": 1000000,
                        "direction": "in",
                        "min": 0,
                        "max": 0.015,
                        "color": "#222222",
                        "axes": [
                            {"position": 0.01, "color": "#4caf50"},
                            {"position": 0.008, "color": "#4caf50"},
                            {"position": 0.006, "color": "#4caf50"},
                            {"position": 0.002, "color": "#f44336"},
                        ],
                    },
                },
                {
                    "type": "LINE",
                    "data": data.snp1m,
                    "config": {
                        "innerRadius": 0.85,
                        "outerRadius": 0.95,
                        "maxGap": 1000000,
                        "direction": "in",
                        "min": 0,
                        "max": 0.015,
                        "color": "#f44336",
                        "tooltipContent": {"name": "value"},
                    },
                },
            ],
            size=800,
            style={"display": "flex", "justify-content": "center"},
        )
    elif circos_select == "scatter":
        return dash_bio.DashCircos(
            id="main-circos",
            layout=list(
                filter(lambda d: d["id"] in ["chr1", "chr2", "chr3"], data.GRCh37)
            ),
            config={
                "innerRadius": size / 2 - 150,
                "outerRadius": size / 2 - 130,
                "ticks": {"display": False, "spacing": 1000000, "labelSuffix": ""},
                "labels": {"display": False},
            },
            tracks=[
                {
                    "type": "HIGHLIGHT",
                    "data": list(
                        filter(
                            lambda d: d["block_id"] in ["chr1", "chr2", "chr3"],
                            data.cytobands,
                        )
                    ),
                    "config": {
                        "innerRadius": size / 2 - 150,
                        "outerRadius": size / 2 - 130,
                        "opacity": 0.8,
                        "tooltipContent": {"name": "name"},
                        "color": {"name": "color"},
                    },
                },
                {
                    "type": "SCATTER",
                    "data": list(
                        filter(lambda d: float(d["value"]) > 0.007, data.snp250)
                    ),
                    "config": {
                        "innerRadius": 0.65,
                        "outerRadius": 0.95,
                        "color": {"colorData": "name"},
                        "tooltipContent": {
                            "source": "block_id",
                            "target": "position",
                            "targetEnd": "value",
                        },
                        "strokeColor": "grey",
                        "strokeWidth": 1,
                        "shape": "circle",
                        "size": 14,
                        "min": 0,
                        "max": 0.013,
                        "axes": [
                            {
                                "spacing": 0.001,
                                "start": 0.006,
                                "thickness": 1,
                                "color": "#4caf50",
                                "opacity": 0.3,
                            },
                            {
                                "spacing": 0.002,
                                "start": 0.006,
                                "thickness": 1,
                                "color": "#4caf50",
                                "opacity": 0.5,
                            },
                            {
                                "spacing": 0.002,
                                "start": 0.002,
                                "end": 0.006,
                                "thickness": 1,
                                "color": "#666",
                                "opacity": 0.5,
                            },
                            {
                                "spacing": 0.001,
                                "end": 0.002,
                                "thickness": 1,
                                "color": "#f44336",
                                "opacity": 0.5,
                            },
                        ],
                        "backgrounds": [
                            {"start": 0.006, "color": "#4caf50", "opacity": 0.1},
                            {
                                "start": 0.002,
                                "end": 0.006,
                                "color": "#d3d3d3",
                                "opacity": 0.1,
                            },
                            {"end": 0.002, "color": "#f44336", "opacity": 0.1},
                        ],
                    },
                },
                {
                    "type": "SCATTER",
                    "data": data.snp250,
                    "config": {
                        "tooltipContent": {
                            "source": "block_id",
                            "target": "position",
                            "targetEnd": "value",
                        },
                        "color": "#4caf50",
                        "strokeColor": "green",
                        "strokeWidth": 1,
                        "shape": "rectangle",
                        "size": 10,
                        "min": 0.007,
                        "max": 0.013,
                        "innerRadius": 1.075,
                        "outerRadius": 1.175,
                        "axes": [
                            {
                                "spacing": 0.001,
                                "thickness": 1,
                                "color": "#4caf50",
                                "opacity": 0.3,
                            },
                            {
                                "spacing": 0.002,
                                "thickness": 1,
                                "color": "#4caf50",
                                "opacity": 0.5,
                            },
                        ],
                        "backgrounds": [
                            {"start": 0.007, "color": "#4caf50", "opacity": 0.1},
                            {"start": 0.009, "color": "#4caf50", "opacity": 0.1},
                            {"start": 0.011, "color": "#4caf50", "opacity": 0.1},
                            {"start": 0.013, "color": "#4caf50", "opacity": 0.1},
                        ],
                    },
                },
                {
                    "type": "SCATTER",
                    "data": list(
                        filter(lambda d: float(d["value"]) < 0.002, data.snp250)
                    ),
                    "config": {
                        "tooltipContent": {
                            "source": "block_id",
                            "target": "position",
                            "targetEnd": "value",
                        },
                        "color": "#f44336",
                        "strokeColor": "red",
                        "strokeWidth": 1,
                        "shape": "triangle",
                        "size": 10,
                        "min": 0,
                        "max": 0.002,
                        "innerRadius": 0.35,
                        "outerRadius": 0.60,
                        "axes": [
                            {
                                "spacing": 0.0001,
                                "thickness": 1,
                                "color": "#f44336",
                                "opacity": 0.3,
                            },
                            {
                                "spacing": 0.0005,
                                "thickness": 1,
                                "color": "#f44336",
                                "opacity": 0.5,
                            },
                        ],
                        "backgrounds": [
                            {"end": 0.0004, "color": "#f44336", "opacity": 0.1},
                            {"end": 0.0008, "color": "#f44336", "opacity": 0.1},
                            {"end": 0.0012, "color": "#f44336", "opacity": 0.1},
                            {"end": 0.0016, "color": "#f44336", "opacity": 0.1},
                            {"end": 0.002, "color": "#f44336", "opacity": 0.1},
                        ],
                    },
                },
                {
                    "type": "SCATTER",
                    "data": data.snp250,
                    "config": {
                        "tooltipContent": {
                            "source": "block_id",
                            "target": "position",
                            "targetEnd": "value",
                        },
                        "innerRadius": 0.65,
                        "outerRadius": 0.95,
                        "strokeColor": "grey",
                        "strokeWidth": 1,
                        "shape": "circle",
                        "size": 14,
                        "min": 0,
                        "max": 0.013,
                        "axes": [
                            {
                                "spacing": 0.001,
                                "start": 0.006,
                                "thickness": 1,
                                "color": "#4caf50",
                                "opacity": 0.3,
                            },
                            {
                                "spacing": 0.002,
                                "start": 0.006,
                                "thickness": 1,
                                "color": "#4caf50",
                                "opacity": 0.5,
                            },
                            {
                                "spacing": 0.002,
                                "start": 0.002,
                                "end": 0.006,
                                "thickness": 1,
                                "color": "#666",
                                "opacity": 0.5,
                            },
                            {
                                "spacing": 0.001,
                                "end": "0.002",
                                "thickness": 1,
                                "color": "#f44336",
                                "opacity": 0.5,
                            },
                        ],
                        "backgrounds": [
                            {"start": 0.006, "color": "#4caf50", "opacity": 0.1},
                            {
                                "start": 0.002,
                                "end": 0.006,
                                "color": "#d3d3d3",
                                "opacity": 0.1,
                            },
                            {"end": 0.002, "color": "#f44336", "opacity": 0.1},
                        ],
                    },
                },
            ],
            size=800,
            style={"display": "flex", "justify-content": "center"},
        )
    elif circos_select == "stack":
        return dash_bio.DashCircos(
            id="main-circos",
            layout=[
                {"id": "chr9", "len": 8000000, "label": "chr9", "color": "#FFCC00"}
            ],
            config={
                "innerRadius": size / 2 - 50,
                "outerRadius": size / 2 - 30,
                "ticks": {"display": True, "labels": False, "spacing": 10000},
                "labels": {"display": False, "labels": False, "spacing": 10000},
            },
            tracks=[
                {
                    "type": "STACK",
                    "data": data.stack,
                    "config": {
                        "innerRadius": 0.7,
                        "outerRadius": 1,
                        "thickness": 4,
                        "margin": 0.01 * 8000000,
                        "direction": "out",
                        "strokeWidth": 0,
                        "opacity": 0.5,
                        "color": "#d3d3d3",
                        "tooltipContent": {"name": "chr"},
                        "color": {
                            "conditional": {
                                "end": "end",
                                "start": "start",
                                "value": [150000, 120000, 90000, 60000, 30000],
                                "color": ["red", "black", "#000000", "#999", "#BBB"],
                            }
                        },
                    },
                }
            ],
            size=800,
            style={"display": "flex", "justify-content": "center"},
        )
    elif circos_select == "text":
        return dash_bio.DashCircos(
            id="main-circos",
            layout=[data.GRCh37[0]],
            config={
                "innerRadius": size / 2 - 100,
                "outerRadius": size / 2 - 80,
                "labels": {"display": False},
                "ticks": {"display": False},
            },
            tracks=[
                {
                    "type": "HIGHLIGHT",
                    "data": list(
                        filter(
                            lambda d: d["block_id"] == data.GRCh37[0]["id"],
                            data.cytobands,
                        )
                    ),
                    "config": {
                        "innerRadius": size / 2 - 100,
                        "outerRadius": size / 2 - 80,
                        "opacity": 0.7,
                        "tooltipContent": {"name": "name"},
                        "color": {"name": "color"},
                    },
                },
                {
                    "type": "TEXT",
                    "data": list(
                        map(
                            lambda d: {
                                "position": (d["start"] + d["end"]) / 2,
                                "value": d["name"],
                                "block_id": d["block_id"],
                            },
                            filter(
                                lambda d: d["block_id"] == data.GRCh37[0]["id"],
                                data.cytobands,
                            ),
                        )
                    ),
                    "config": {
                        "innerRadius": 1.02,
                        "outerRadius": 1.3,
                        "style": {"font-size": 12},
                    },
                },
            ],
            size=800,
            style={"display": "flex", "justify-content": "center"},
        )


@app.callback(
    Output("data-table", "rows"),
    [Input("data-selector", "value"),
    Input("data-selector", "options"),
    Input("data-table", "selected_row_indices")],
    [State("main-circos", "layout"), 
    State("main-circos", "tracks")],
)
def update_table(data_selector, circos_trigger, selected, layout, tracks):
    if data_selector == "layout":
        df = pd.DataFrame(layout)
    else:
        df = pd.DataFrame(tracks[data_selector]["data"])
    return df.to_dict("records")


@app.callback(
    Output("event-data", "value"),
    [Input("main-circos", "hoverDatum"), 
    Input("main-circos", "clickDatum")],
)
def event_data(hoverDatum, clickDatum):
    if hoverDatum != None:
        return str(hoverDatum)
    if clickDatum != None:
        return str(clickDatum)


if __name__ == "__main__":

    app.run_server(debug=True)
