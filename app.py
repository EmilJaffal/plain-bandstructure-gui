import matplotlib
matplotlib.use('Agg')
import os
import re
import io
import base64
import tempfile
import dash
import matplotlib.pyplot as plt
from dash import Dash, dcc, html, Input, Output, State, ctx, no_update
from pyprocar import bandsplot
import zipfile
import glob

DEFAULTS = {
    "ymin": -3,
    "ymax": 1
}

def plot_bandstructure(dirname, ylabel, xlabel, emin, emax, show_titles, show_axis_scale, xmin=None, xmax=None, fermi=8.41046738, custom_title=None):
    fig, ax = bandsplot(
        code='vasp',
        dirname=dirname,
        mode='plain',
        fermi=fermi,
        elimit=[emin, emax],
        color='blue',
        show=False
    )
    folder_name = os.path.basename(dirname)
    def subscript_numbers(s):
        return re.sub(r'(\d+)', r'$_{\1}$', s)
    show_plot_title = 'plot_title' in show_titles if show_titles else True
    show_x_title = 'x_title' in show_titles if show_titles else True
    show_y_title = 'y_title' in show_titles if show_titles else True
    show_x_scale = 'x_scale' in show_axis_scale if show_axis_scale else True
    show_y_scale = 'y_scale' in show_axis_scale if show_axis_scale else True

    if custom_title and show_plot_title:
        title_str = custom_title
    elif show_plot_title:
        title_str = subscript_numbers(folder_name) + ' band structure'
    else:
        title_str = ""
    ax.set_title(title_str, fontsize=14)
    ax.set_ylabel(ylabel if show_y_title else "", fontsize=14)
    ax.set_xlabel(xlabel if show_x_title else "", fontsize=14)
    ax.tick_params(axis='y', which='major', labelsize=12, labelleft=show_y_scale, length=10, width=1)
    ax.tick_params(axis='y', which='minor', labelsize=12, length=0, width=0)
    ax.tick_params(axis='x', labelsize=12, labelbottom=show_x_scale)
    fig.set_size_inches(4.5, 4.5)  # ~800x800px at 300dpi
    for spine in ax.spines.values():
        spine.set_linewidth(1.2)
    ax.axhline(0, color='black', linestyle='--', linewidth=1.2)
    if xmin is not None and xmax is not None:
        ax.set_xlim(xmin, xmax)
    xmax_val = ax.get_xlim()[1]
    ax.annotate(
        r'$E_{\mathit{F}}$', 
        xy=(xmax_val, 0), 
        xytext=(10, 0), 
        textcoords='offset points',
        fontsize=12,
        va='center',
        ha='left',
        color='black'
    )
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches='tight', dpi=300)
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('ascii')

app = Dash(__name__)

app.layout = html.Div([
    html.H2("Band Structure Plotter",  style={
        "fontSize": "32px", "fontWeight": "bold", "fontFamily": "DejaVu Sans, Arial, sans-serif",
        "textAlign": "center", "marginBottom": "20px", "color": "#333"
    }),
    html.Div([
        dcc.Upload(
            id='upload-zip',
            children=html.Button('Upload .zip with KPOINTS, OUTCAR & PROCAR', style={
                "backgroundColor": "#17a2b8", "color": "white", "padding": "10px 20px",
                "border": "none", "borderRadius": "5px", "cursor": "pointer",
                "fontSize": "16px", "fontWeight": "bold", "fontFamily": "DejaVu Sans, Arial, sans-serif",
                "marginRight": "10px", "boxShadow": "0px 2px 3px rgba(0, 0, 0, 0.1)"
            }),
            multiple=False,
            style={"marginBottom": "15px"}
        ),
        dcc.Input(id='custom-title', type='text', placeholder='Custom plot title...', style={"width": "350px", "marginRight": "15px"}),
    ], style={"marginBottom": "15px", "display": "flex", "alignItems": "center"}),
    html.Div([
        html.Button("Demo file", id="demo-file", n_clicks=0, style={
            "backgroundColor": "#28a745", "color": "white", "padding": "10px 20px",
            "border": "none", "borderRadius": "5px", "cursor": "pointer",
            "fontSize": "16px", "fontWeight": "bold", "fontFamily": "DejaVu Sans, Arial, sans-serif",
            "marginRight": "10px", "boxShadow": "0px 2px 3px rgba(0, 0, 0, 0.1)"
        }),
        html.Button("Save plot", id="save-plot", n_clicks=0, style={
            "backgroundColor": "#007bff", "color": "white", "padding": "10px 20px",
            "border": "none", "borderRadius": "5px", "cursor": "pointer",
            "fontSize": "16px", "fontWeight": "bold", "fontFamily": "DejaVu Sans, Arial, sans-serif",
            "marginRight": "10px", "boxShadow": "0px 2px 3px rgba(0, 0, 0, 0.1)"
        }),
        html.Button("Reset axes", id="reset-axes", n_clicks=0, style={
            "backgroundColor": "#dc3545", "color": "white", "padding": "10px 15px",
            "border": "none", "borderRadius": "5px", "cursor": "pointer",
            "fontSize": "16px", "fontWeight": "bold", "fontFamily": "DejaVu Sans, Arial, sans-serif",
            "marginRight": "10px", "boxShadow": "0px 2px 3px rgba(0, 0, 0, 0.1)"
        }),
    ], style={"display": "flex", "flexDirection": "row", "alignItems": "center", "marginBottom": "20px"}),
    html.Div([
        html.Div([
            html.Img(id='band-plot', style={
                "height": "800px",
                "width": "800px",
                "backgroundColor": "#fff",
                "borderRadius": "10px",
                "boxShadow": "0px 4px 6px rgba(0, 0, 0, 0.08)"
            }),
            html.Div(id="save-confirmation", style={
                "marginTop": "10px", "color": "#4CAF50", "fontFamily": "DejaVu Sans, Arial, sans-serif"
            }),
            html.Div(id="parse-message", style={"marginTop": "10px", "fontFamily": "DejaVu Sans, Arial, sans-serif"}),
        ], style={"flex": "0 0 auto"}),
        html.Div([
            html.H3("Graph adjustments", style={
                "fontFamily": "DejaVu Sans, Arial, sans-serif", "color": "#333",
                "marginBottom": "10px", "textDecoration": "underline", "fontSize": "20px"
            }),
            html.Div([
                html.Label("X-axis limits:", style={"fontWeight": "bold", "marginBottom": "5px", "fontFamily": "DejaVu Sans, Arial, sans-serif"}),
                dcc.Input(id='xmin', type='number', value=None, style={"marginRight": "10px", "padding": "8px", "borderRadius": "5px", "border": "1px solid #ccc", "width": "60px"}),
                dcc.Input(id='xmax', type='number', value=None, style={"padding": "8px", "borderRadius": "5px", "border": "1px solid #ccc", "width": "60px"}),
            ], style={"marginBottom": "15px"}),
            html.Div([
                html.Label("Y-axis limits:", style={"fontWeight": "bold", "marginBottom": "5px", "fontFamily": "DejaVu Sans, Arial, sans-serif"}),
                dcc.Input(id='ymin', type='number', value=DEFAULTS["ymin"], style={"marginRight": "10px", "padding": "8px", "borderRadius": "5px", "border": "1px solid #ccc", "width": "60px"}),
                dcc.Input(id='ymax', type='number', value=DEFAULTS["ymax"], style={"padding": "8px", "borderRadius": "5px", "border": "1px solid #ccc", "width": "60px"}),
            ], style={"marginBottom": "15px"}),
            html.Div([
                html.Label("Toggle plot elements:", style={"fontWeight": "bold", "fontFamily": "DejaVu Sans, Arial, sans-serif", "marginBottom": "5px"}),
                dcc.Checklist(
                    id='show-titles',
                    options=[
                        {'label': 'Plot title', 'value': 'plot_title'},
                        {'label': 'X axis title', 'value': 'x_title'},
                        {'label': 'Y axis title', 'value': 'y_title'},
                    ],
                    value=['plot_title', 'x_title', 'y_title'],
                    labelStyle={"display": "block", "marginBottom": "3px"},
                    style={"fontFamily": "DejaVu Sans, Arial, sans-serif"}
                ),
            ], style={"marginBottom": "15px"}),

            html.Div([
                html.Label("Toggle axis scales:", style={"fontWeight": "bold", "fontFamily": "DejaVu Sans, Arial, sans-serif", "marginBottom": "5px"}),
                dcc.Checklist(
                    id='show-axis-scale',
                    options=[
                        {'label': 'Show X axis scale', 'value': 'x_scale'},
                        {'label': 'Show Y axis scale', 'value': 'y_scale'},
                    ],
                    value=['x_scale', 'y_scale'],
                    labelStyle={"display": "block", "marginBottom": "3px"},
                    style={"fontFamily": "DejaVu Sans, Arial, sans-serif"}
                ),
            ], style={"marginBottom": "15px"}),
            html.Div([
                dcc.Input(id='folder-path', type='text', placeholder='Paste folder path here...', style={"width": "350px", "marginRight": "15px"}),
                html.Button("Input path to folder with KPOINTS, OUTCAR & PROCAR", id="use-folder", n_clicks=0, style={
                    "backgroundColor": "#007bff", "color": "white", "padding": "20px 20px",
                    "border": "none", "borderRadius": "5px", "cursor": "pointer",
                    "fontSize": "16px", "fontWeight": "bold", "fontFamily": "DejaVu Sans, Arial, sans-serif",
                    "marginRight": "10px", "boxShadow": "0px 2px 3px rgba(0, 0, 0, 0.1)"
                }),
            ], style={"marginBottom": "15px", "display": "flex", "alignItems": "center"}),
            html.Div([
                dcc.Input(id='fermi-energy', type='number', placeholder='Fermi energy (eV)', value=8.41046738, style={"width": "200px", "marginRight": "15px"}),
                html.Label("Fermi energy (eV)", style={"marginRight": "10px", "fontFamily": "DejaVu Sans, Arial, sans-serif"}),
            ], style={"marginBottom": "15px", "display": "flex", "alignItems": "center"}),
        ], style={"flex": "0 0 320px", "marginLeft": "40px"})
    ], style={"display": "flex", "flexDirection": "row", "alignItems": "flex-start"}),
    dcc.Download(id="download-plot"),
    dcc.Store(id='current-dir')
])

@app.callback(
    Output('band-plot', 'src'),
    Output('parse-message', 'children'),
    Output('current-dir', 'data'),
    Output('fermi-energy', 'value'), 
    Input('use-folder', 'n_clicks'),
    Input('demo-file', 'n_clicks'),
    Input('reset-axes', 'n_clicks'),
    Input('upload-zip', 'contents'),
    Input('xmin', 'value'),
    Input('xmax', 'value'),
    Input('ymin', 'value'),
    Input('ymax', 'value'),
    Input('show-titles', 'value'),
    Input('show-axis-scale', 'value'),
    Input('fermi-energy', 'value'), 
    State('folder-path', 'value'),
    State('current-dir', 'data'),
    State('custom-title', 'value'),
    prevent_initial_call=True
)
def update_band_plot(n_use_folder, n_demo, n_reset, zip_contents, xmin, xmax, ymin, ymax, show_titles, show_axis_scale, fermi_energy, folder_path, current_dir, custom_title):
    messages = []
    trigger = ctx.triggered_id
    DEMO_PATH = os.path.join(os.path.dirname(__file__), "CeCoAl4")
    dirname = current_dir if current_dir else DEMO_PATH

    # Handle zip upload
    if trigger == 'upload-zip' and zip_contents:
        content_type, content_string = zip_contents.split(',')
        decoded = base64.b64decode(content_string)
        temp_dir = tempfile.mkdtemp()
        zip_path = os.path.join(temp_dir, "input.zip")
        with open(zip_path, "wb") as f:
            f.write(decoded)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        dirname = temp_dir
        messages.append(html.Div("Zip uploaded and extracted.", style={"color": "green"}))

        # Check for required files
        required_files = ['OUTCAR', 'PROCAR', 'KPOINTS', 'POSCAR']
        found_files = {}
        for fname in required_files:
            matches = glob.glob(os.path.join(temp_dir, '**', fname), recursive=True)
            if matches:
                found_files[fname] = matches[0]
            else:
                messages.append(html.Div(f"WARNING: {fname} not found in zip.", style={"color": "orange"}))

        # If all files found, set dirname to their parent directory
        if all(f in found_files for f in ['OUTCAR', 'PROCAR', 'KPOINTS']):
            dirname = os.path.dirname(found_files['OUTCAR'])
        else:
            messages.append(html.Div("ERROR: Required files missing. Please check your zip.", style={"color": "red"}))
            return dash.no_update, messages, current_dir

    elif trigger == 'demo-file':
        dirname = DEMO_PATH
    elif trigger == 'use-folder' and folder_path:
        dirname = folder_path

    kpoints_path = os.path.join(dirname, "KPOINTS")
    if os.path.isfile(kpoints_path):
        messages.append(html.Div(f"Parsing KPOINTS file: {kpoints_path}", style={"color": "blue"}))

    outcar_path = os.path.join(dirname, "OUTCAR")
    if not os.path.isfile(outcar_path):
        messages.append(html.Div("WARNING: Issue with outcar file. Either it was not found or there is an issue with the parser", style={"color": "orange"}))

    doscar_path = os.path.join(dirname, "DOSCAR")
    if os.path.isfile(doscar_path):
        fermi_energy = get_fermi_from_doscar(doscar_path)
        messages.append(html.Div(f"Fermi energy read from DOSCAR: {fermi_energy}", style={"color": "blue"}))
    else:
        messages.append(html.Div("WARNING: DOSCAR not found, using default Fermi energy.", style={"color": "orange"}))
        fermi_energy = fermi_energy if fermi_energy is not None else 8.41046738

    try:
        img = plot_bandstructure(
            dirname=dirname,
            ylabel='Energy (eV)',
            xlabel='K vector',
            emin=ymin if ymin is not None else DEFAULTS["ymin"],
            emax=ymax if ymax is not None else DEFAULTS["ymax"],
            show_titles=show_titles,
            show_axis_scale=show_axis_scale,
            xmin=xmin,
            xmax=xmax,
            fermi=fermi_energy,
            custom_title=custom_title
        )
        return "data:image/png;base64," + img, messages, dirname, fermi_energy 
    except Exception as e:
        messages.append(html.Div(f"{type(e).__name__}: {e}", style={"color": "red"}))
        return dash.no_update, messages, dirname, fermi_energy 

@app.callback(
    Output("download-plot", "data"),
    Input("save-plot", "n_clicks"),
    State('xmin', 'value'),
    State('xmax', 'value'),
    State('ymin', 'value'),
    State('ymax', 'value'),
    State('show-titles', 'value'),
    State('show-axis-scale', 'value'),
    State('fermi-energy', 'value'),  
    State('current-dir', 'data'),    
    prevent_initial_call=True
)
def save_plot(n_clicks, xmin, xmax, ymin, ymax, show_titles, show_axis_scale, fermi_energy, current_dir):
    if not n_clicks:
        return no_update

    dirname = current_dir if current_dir else os.path.join(os.path.dirname(__file__), "CeCoAl4")
    folder_name = os.path.basename(dirname)

    fig_data = plot_bandstructure(
        dirname=dirname,
        ylabel='Energy (eV)',
        xlabel='K vector',
        emin=ymin if ymin is not None else DEFAULTS["ymin"],
        emax=ymax if ymax is not None else DEFAULTS["ymax"],
        show_titles=show_titles,
        show_axis_scale=show_axis_scale,
        xmin=xmin,
        xmax=xmax,
        fermi=fermi_energy if fermi_energy is not None else 8.41046738
    )
    filename = f"{folder_name}_bandstructure.png"
    return dict(content=fig_data, filename=filename, type="image/png", base64=True)

def get_fermi_from_doscar(doscar_path):
    try:
        with open(doscar_path, 'r') as f:
            lines = f.readlines()
            if len(lines) >= 6:
                # Line 6 (index 5), split by whitespace, get 4th value (index 3)
                values = lines[5].split()
                if len(values) >= 4:
                    return float(values[3])
    except Exception:
        pass
    return 8.41046738  # fallback default

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8050))
    app.run_server(debug=False, host='0.0.0.0', port=port)