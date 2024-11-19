import os
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import numpy as np
import plotly.graph_objs as go


app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])

app.title = 'Stress in Soils'
app._favicon = ('assets/favicon.ico')

# Updated layout with sliders on top and layer properties below
app.layout = html.Div([
    dcc.Store(id='window-width'),

    # Add the dcc.Interval component to track the window width
    dcc.Interval(id='interval', interval=1000, n_intervals=0),

    # Main container
    html.Div(style={'display': 'flex', 'flexDirection': 'row', 'width': '100%', 'height': '100vh'}, children=[
        # Control container (sliders)
        html.Div(id='control-container', style={'width': '25%', 'padding': '2%', 'flexDirection': 'column'}, children=[
            html.H1('Stress in Soils', style={'textAlign': 'center'}, className='h1'),

            # Sliders for each layer
            html.Div(className='slider-container', children=[
                # Layer 1 Slider
                html.Label(children=[
                    'Z', html.Sub('1'), ' (m)', 
                            html.Div(className='tooltip', children=[
                                html.Img(src='/assets/info-icon.png', className='info-icon', alt='Info'), 
                                html.Span('Thickness of layer 1 (Layer 1).', className='tooltiptext')
                            ])], className='slider-label'),
                dcc.Slider(
                    id='z-1', min=0, max=20, step=0.25, value=4,
                    marks={i: f'{i}' for i in range(0, 21, 5)},
                    className='slider', tooltip={'placement': 'bottom', 'always_visible': True}
                ),

                # Layer 2 Slider
                html.Label(children=[
                    'Z', html.Sub('2'), ' (m)', 
                            html.Div(className='tooltip', children=[
                                html.Img(src='/assets/info-icon.png', className='info-icon', alt='Info'), 
                                html.Span('Thickness of layer 2 (Layer 2).', className='tooltiptext')
                            ])], className='slider-label'),
                dcc.Slider(
                    id='z-2', min=0, max=20, step=0.25, value=4,
                    marks={i: f'{i}' for i in range(0, 21, 5)},
                    className='slider', tooltip={'placement': 'bottom', 'always_visible': True}
                ),

                # Layer 3 Slider
                html.Label(children=[
                    'Z', html.Sub('3'), ' (m)', 
                            html.Div(className='tooltip', children=[
                                html.Img(src='/assets/info-icon.png', className='info-icon', alt='Info'), 
                                html.Span('Thickness of layer 3 (Layer 3).', className='tooltiptext')
                            ])], className='slider-label'),
                dcc.Slider(
                    id='z-3', min=0, max=20, step=0.25, value=4,
                    marks={i: f'{i}' for i in range(0, 21, 5)},
                    className='slider', tooltip={'placement': 'bottom', 'always_visible': True}
                ),

                # Layer 1 h slider
                html.Label(children=[
                    "Water Table", 
                            html.Div(className='tooltip', children=[
                                html.Img(src='/assets/info-icon.png', className='info-icon', alt='Info'), 
                                html.Span('Piezometric head for layer 1 (Layer 1).', className='tooltiptext')
                            ])], className='slider-label'),
                dcc.Slider(
                    id='water-table', min=0, max=20, step=0.25, value=1,
                    marks={i: f'{i}' for i in range(0, 21, 5)},
                    className='slider', tooltip={'placement': 'bottom', 'always_visible': True}
                ),

            ]),
        


        # Properties for each layer
        html.Div(className='layer-properties', children=[
                # foundation Properties
                html.H3('Foundation:', style={'textAlign': 'left'}),
                html.Label(["a", 
                            html.Div(className='tooltip', children=[
                                html.Img(src='/assets/info-icon.png', className='info-icon', alt='Info'), 
                                html.Span('Width of the foundation', className='tooltiptext')
                            ]),'(m)'], className='input-label'),
                dcc.Input(id='a', type='number', value=3, step=0.1, style={'width': '12%'}, className='input-field'),
                html.Label(["b", 
                            html.Div(className='tooltip', children=[
                                html.Img(src='/assets/info-icon.png', className='info-icon', alt='Info'), 
                                html.Span('Length of the foundation', className='tooltiptext')
                            ]),'(m)'], className='input-label'),
                dcc.Input(id='b', type='number', value=1.5, step=0.1, style={'width': '12%'}, className='input-field'),
                html.Label(["q", 
                            html.Div(className='tooltip', children=[
                                html.Img(src='/assets/info-icon.png', className='info-icon', alt='Info'), 
                                html.Span('Footing load', className='tooltiptext')
                            ]),'(kPa)'], className='input-label'),
                dcc.Input(id='q', type='number', value=100, step=1, style={'width': '12%'}, className='input-field'),


                # Layer 1 Properties
                html.H3('Layer 1:', style={'textAlign': 'left'}),
                html.Label([f'γ', html.Sub('d'), 
                            html.Div(className='tooltip', children=[
                                html.Img(src='/assets/info-icon.png', className='info-icon', alt='Info'), 
                                html.Span('Dry unit weight of Layer 1', className='tooltiptext')
                            ]),' (kN/m³)'], className='input-label'),
                dcc.Input(id='gamma_1', type='number', value=18, step=0.01, style={'width': '12%'}, className='input-field'),
                html.Label([f'γ', html.Sub('sat'), 
                            html.Div(className='tooltip', children=[
                                html.Img(src='/assets/info-icon.png', className='info-icon', alt='Info'), 
                                html.Span('Saturated unit weight of Layer 1', className='tooltiptext')
                            ]),' (kN/m³)'], className='input-label'),
                dcc.Input(id='gamma_r_1', type='number', value=19, step=0.01, style={'width': '12%'}, className='input-field'),
                html.Div(style={'display': 'flex', 'alignItems': 'center', 'whiteSpace': 'nowrap'}, children=[
                    html.Label([f'γ′', 
                                html.Div(className='tooltip', children=[
                                    html.Img(src='/assets/info-icon.png', className='info-icon', alt='Info'), 
                                    html.Span('Submerged unit weight of Layer 1', className='tooltiptext')
                                ])], className='input-label', style={'marginRight': '5px'}),
                    html.Div(id='gamma_prime_1', style={'width': 'auto', 'display': 'inline-block', 'fontWeight': 'bold', 'color': 'red'})  
                ]),
                html.Label([f'C', html.Sub('c'), 
                            html.Div(className='tooltip', children=[
                                html.Img(src='/assets/info-icon.png', className='info-icon', alt='Info'), 
                                html.Span('Compression index of Layer 1', className='tooltiptext')
                            ])], className='input-label'),
                dcc.Input(id='C_c_1', type='number', value=0.6, step=0.01, style={'width': '12%'}, className='input-field'),
                html.Label([f'C', html.Sub('s'), 
                            html.Div(className='tooltip', children=[
                                html.Img(src='/assets/info-icon.png', className='info-icon', alt='Info'), 
                                html.Span('Swelling index of Layer 1', className='tooltiptext')
                            ])], className='input-label'),
                dcc.Input(id='C_s_1', type='number', value=0.1, step=0.01, style={'width': '12%'}, className='input-field'),
                html.Label([f'e', html.Sub('0'), 
                            html.Div(className='tooltip', children=[
                                html.Img(src='/assets/info-icon.png', className='info-icon', alt='Info'), 
                                html.Span('initial void ratio of Layer 1', className='tooltiptext')
                            ])], className='input-label'),
                dcc.Input(id='e_0_1', type='number', value=2, step=0.01, style={'width': '12%'}, className='input-field'),
                html.Label(["OCR", 
                            html.Div(className='tooltip', children=[
                                html.Img(src='/assets/info-icon.png', className='info-icon', alt='Info'), 
                                html.Span('OverConsolidation ratio of Layer 1', className='tooltiptext')
                            ])], className='input-label'),
                dcc.Input(id='OCR_1', type='number', value=1, step=0.1, style={'width': '12%'}, className='input-field'),

                # Layer 2 Properties
                html.H3('Layer 2:', style={'textAlign': 'left'}),
                html.Label([f'γ', html.Sub('d'), 
                            html.Div(className='tooltip', children=[
                                html.Img(src='/assets/info-icon.png', className='info-icon', alt='Info'), 
                                html.Span('Dry unit weight of Layer 2', className='tooltiptext')
                            ]),' (kN/m³)'], className='input-label'),
                dcc.Input(id='gamma_2', type='number', value=19, step=0.01, style={'width': '12%'}, className='input-field'),
                html.Label([f'γ', html.Sub('sat'), 
                            html.Div(className='tooltip', children=[
                                html.Img(src='/assets/info-icon.png', className='info-icon', alt='Info'), 
                                html.Span('Saturated unit weight of Caly', className='tooltiptext')
                            ]),' (kN/m³)'], className='input-label'),
                dcc.Input(id='gamma_r_2', type='number', value=21, step=0.01, style={'width': '12%'}, className='input-field'),
                html.Div(style={'display': 'flex', 'alignItems': 'center', 'whiteSpace': 'nowrap'}, children=[
                    html.Label([f'γ′', 
                                html.Div(className='tooltip', children=[
                                    html.Img(src='/assets/info-icon.png', className='info-icon', alt='Info'), 
                                    html.Span('Submerged unit weight of Layer 2 under flow condition', className='tooltiptext')
                                ])], className='input-label', style={'marginRight': '5px'}),
                    html.Div(id='gamma_prime_2', style={'width': 'auto', 'display': 'inline-block', 'fontWeight': 'bold', 'color': 'red'})  
                ]),
                html.Label([f'C', html.Sub('c'), 
                            html.Div(className='tooltip', children=[
                                html.Img(src='/assets/info-icon.png', className='info-icon', alt='Info'), 
                                html.Span('Compression index of Layer 1', className='tooltiptext')
                            ])], className='input-label'),
                dcc.Input(id='C_c_2', type='number', value=0.6, step=0.01, style={'width': '12%'}, className='input-field'),
                html.Label([f'C', html.Sub('s'), 
                            html.Div(className='tooltip', children=[
                                html.Img(src='/assets/info-icon.png', className='info-icon', alt='Info'), 
                                html.Span('Swelling index of Layer 2', className='tooltiptext')
                            ])], className='input-label'),
                dcc.Input(id='C_s_2', type='number', value=0.1, step=0.01, style={'width': '12%'}, className='input-field'),
                html.Label([f'e', html.Sub('0'), 
                            html.Div(className='tooltip', children=[
                                html.Img(src='/assets/info-icon.png', className='info-icon', alt='Info'), 
                                html.Span('initial void ratio of Layer 2', className='tooltiptext')
                            ])], className='input-label'),
                dcc.Input(id='e_0_2', type='number', value=2, step=0.01, style={'width': '12%'}, className='input-field'),
                html.Label(["OCR", 
                            html.Div(className='tooltip', children=[
                                html.Img(src='/assets/info-icon.png', className='info-icon', alt='Info'), 
                                html.Span('OverConsolidation ratio of Layer 2', className='tooltiptext')
                            ])], className='input-label'),
                dcc.Input(id='OCR_2', type='number', value=1, step=0.1, style={'width': '12%'}, className='input-field'),

                # Layer 3 Properties
                html.H3('Layer 3:', style={'textAlign': 'left'}),
                html.Label([f'γ', html.Sub('d'), 
                            html.Div(className='tooltip', children=[
                                html.Img(src='/assets/info-icon.png', className='info-icon', alt='Info'), 
                                html.Span('Dry unit weight of Layer 3', className='tooltiptext')
                            ]),' (kN/m³)'], className='input-label'),
                dcc.Input(id='gamma_3', type='number', value=18, step=0.01, style={'width': '12%'}, className='input-field'),
                html.Label([f'γ', html.Sub('sat'), 
                            html.Div(className='tooltip', children=[
                                html.Img(src='/assets/info-icon.png', className='info-icon', alt='Info'), 
                                html.Span('Saturated unit weight of Layer 3', className='tooltiptext')
                            ]),' (kN/m³)'], className='input-label'),
                dcc.Input(id='gamma_r_3', type='number', value=19, step=0.01, style={'width': '12%'}, className='input-field'),
                html.Div(style={'display': 'flex', 'alignItems': 'center', 'whiteSpace': 'nowrap'}, children=[
                    html.Label([f'γ′', 
                                html.Div(className='tooltip', children=[
                                    html.Img(src='/assets/info-icon.png', className='info-icon', alt='Info'), 
                                    html.Span('Submerged unit weight of Layer 3', className='tooltiptext')
                                ])], className='input-label', style={'marginRight': '5px'}),
                    html.Div(id='gamma_prime_3', style={'width': 'auto', 'display': 'inline-block', 'fontWeight': 'bold', 'color': 'red'})  
                ]),
                html.Label([f'C', html.Sub('c'), 
                            html.Div(className='tooltip', children=[
                                html.Img(src='/assets/info-icon.png', className='info-icon', alt='Info'), 
                                html.Span('Compression index of Layer 3', className='tooltiptext')
                            ])], className='input-label'),
                dcc.Input(id='C_c_3', type='number', value=0.6, step=0.01, style={'width': '12%'}, className='input-field'),
                html.Label([f'C', html.Sub('s'), 
                            html.Div(className='tooltip', children=[
                                html.Img(src='/assets/info-icon.png', className='info-icon', alt='Info'), 
                                html.Span('Swelling index of Layer 3', className='tooltiptext')
                            ])], className='input-label'),
                dcc.Input(id='C_s_3', type='number', value=0.1, step=0.01, style={'width': '12%'}, className='input-field'),
                html.Label([f'e', html.Sub('0'), 
                            html.Div(className='tooltip', children=[
                                html.Img(src='/assets/info-icon.png', className='info-icon', alt='Info'), 
                                html.Span('initial void ratio of Layer 3', className='tooltiptext')
                            ])], className='input-label'),
                dcc.Input(id='e_0_3', type='number', value=2, step=0.01, style={'width': '12%'}, className='input-field'),
                html.Label(["OCR", 
                            html.Div(className='tooltip', children=[
                                html.Img(src='/assets/info-icon.png', className='info-icon', alt='Info'), 
                                html.Span('OverConsolidation ratio of Layer 3', className='tooltiptext')
                            ])], className='input-label'),
                dcc.Input(id='OCR_3', type='number', value=1, step=0.1, style={'width': '12%'}, className='input-field'),
            ]),
        ]),

        # Graphs container
        html.Div(
            className='graph-container', 
            id='graphs-container', 
            style={
                'display': 'flex', 
                'flexDirection': 'row',  # Arrange the graphs in a row
                'width': '75%'  # Increased width to make it wider
            }, 
            children=[
                # Left column: Stack the first and second graphs
                html.Div(
                    style={'display': 'flex', 'flexDirection': 'column', 'width': '60%', 'height': '100%'}, 
                    children=[
                        # First graph (Foundation dimension)
                        html.Div(
                            style={'height': '20%'},  # First graph takes 50% of the height
                            children=[
                                dcc.Graph(id='foundation-dimension-graph', style={'height': '100%', 'width': '100%'})
                            ]
                        ),
                        # Second graph (Soil layers)
                        html.Div(
                            style={'height': '80%'},  # Second graph takes the remaining 50% of the height
                            children=[
                                dcc.Graph(id='soil-layers-graph', style={'height': '100%', 'width': '100%'})
                            ]
                        ),
                    ]
                ),
                # Right column: The third graph (change in stress) takes the same height as the second one
                html.Div(
                    style={'display': 'flex', 'flexDirection': 'column', 'width': '40%', 'height': '100%'},  # Adjusted to take 55% of the width
                    children=[
                        html.Div(style={'height': '20%'},
                            children=[
                            # html.H3('Total settelment under point E, =', style={'textAlign': 'center'}),
                            html.Div(id='total-settlement', 
                                     style={'textAlign': 'center', 'fontSize': '20px', 'fontWeight': 'bold', 'color': 'red', 
                                            'padding-top': '10%', 'padding-left': '10%', 'padding-right': '10%'}),
                            ]         
                        ),
                        html.Div(
                            style={'height': '80%'},  
                            children=[
                                dcc.Graph(id='stress-change-graph', style={'height': '100%', 'width': '100%'}) 
                            ]
                        ),
                    ]
                )
            ]
        ),

        
        # Add the logo image to the top left corner
        html.Img(
            src='/assets/logo.png', className='logo',
            style={
                'position': 'absolute',
                'width': '15%',  # Adjust size as needed
                'height': 'auto',
                'z-index': '1000',  # Ensure it's on top of other elements
            }
        )
    ])
])

# Callback to update γ′ based on γ_r values for each layer
@app.callback(
    [Output(f'gamma_prime_{i}', 'children') for i in range(1, 4)] + [Output('b', 'value')],
    [Input(f'gamma_r_{i}', 'value') for i in range(1, 4)],
    Input('a', 'value'),
    Input('b', 'value'),
)
def update_gamma_prime(gamma_r1, gamma_r2, gamma_r3, a_value, b_value):
    # Ensure b does not exceed a
    if b_value > a_value:
        b_value = a_value  # or return a message, e.g., "b cannot exceed a"

    # Calculate γ′ as γ_r - 9.81 for each layer
    gamma_prime1 = round(gamma_r1 - 10, 2) if gamma_r1 is not None else None
    gamma_prime2 = round(gamma_r2 - 10, 2) if gamma_r2 is not None else None
    gamma_prime3 = round(gamma_r3 - 10, 2) if gamma_r3 is not None else None

    return f"= {gamma_prime1} kN/m³", f"= {gamma_prime2} kN/m³", f"= {gamma_prime3} kN/m³", b_value




# JavaScript for updating window width
app.clientside_callback(
    """
    function(n_intervals) {
        return window.innerWidth;
    }
    """,
    Output('window-width', 'data'),
    Input('interval', 'n_intervals')
)


# Callback to handle the animations and input updates
@app.callback(
    Output('foundation-dimension-graph', 'figure'),
    Output('soil-layers-graph', 'figure'),
    Output('stress-change-graph', 'figure'),
    Output('total-settlement', 'children'),
    Input('z-1', 'value'),
    Input('z-2', 'value'),
    Input('z-3', 'value'),
    Input('water-table', 'value'),
    Input('a', 'value'),
    Input('b', 'value'),
    Input('q', 'value'),
    Input('gamma_1', 'value'),
    Input('gamma_r_1', 'value'),
    Input('gamma_2', 'value'),
    Input('gamma_r_2', 'value'),
    Input('gamma_3', 'value'),
    Input('gamma_r_3', 'value'),
    Input('C_c_1', 'value'),
    Input('C_s_1', 'value'),
    Input('e_0_1', 'value'),
    Input('OCR_1', 'value'),
    Input('C_c_2', 'value'),
    Input('C_s_2', 'value'),
    Input('e_0_2', 'value'),
    Input('OCR_2', 'value'),
    Input('C_c_3', 'value'),
    Input('C_s_3', 'value'),
    Input('e_0_3', 'value'),
    Input('OCR_3', 'value'),


    
)
def update_graphs( z1, z2, z3, water_table, a, b, q, gamma_1, gamma_r_1, gamma_2, gamma_r_2, 
                   gamma_3, gamma_r_3, C_c_1, C_s_1, e_0_1, OCR_1, C_c_2, C_s_2, e_0_2, 
                   OCR_2, C_c_3, C_s_3, e_0_3, OCR_3):
    # Constants
    gamma_water = 10 # kN/m³ for water

    # total depth
    total_depth = z1 + z2 + z3

    # Ensure y_top has a default value
    y_top = -0.1*total_depth

    # Define soil layers and their boundaries with specified patterns
    layers = [
        {'layer_id': '1', 'name': 'Layer 1', 'thickness' : z1,'top': 0, 'bottom': z1},  
        {'layer_id': '2', 'name': 'Layer 2', 'thickness' : z2, 'top': z1, 'bottom': z1 + z2},  
        {'layer_id': '3', 'name': 'Layer 3', 'thickness' : z3, 'top': z1 + z2, 'bottom': z1 + z2 + z3},  
    ]

    # Create the soil layers figure (139,69,19)
    foundation_fig = go.Figure()
    soil_layers_fig = go.Figure()
    stress_change_fig = go.Figure()

    # add top view dimension scaled to 0-1
    x0_dim = total_depth/2 - a/2
    y0_dim = 0
    x1_dim = total_depth/2 + a/2
    y1_dim = b

    # add rectangle for foundation top view
    foundation_fig.add_shape(
        type="rect",
        x0=x0_dim,
        y0=y0_dim,
        x1=x1_dim,
        y1=y1_dim,
        line=dict(width=3, color="black"),
        # fillcolor="lightskyblue",
        # opacity=0.5,
    )

    # Add text annotation at the middle of the line
    foundation_fig.add_annotation(
        x=0.5*(x1_dim - x0_dim) + x0_dim,  # Middle x-coordinate
        y=1.07 * y1_dim,  # Slightly above the line
        text=f"a= {a}m",  # The label text
        showarrow=False,  # No arrow for the text itself
        font=dict(size=14, color="black"),
        xanchor='center',
        yanchor='bottom'  # Align the text to appear above the line
    )

    # Add text annotation at the middle of the line with dircetion of the text from down to up
    foundation_fig.add_annotation(
        x=0.99*x0_dim,  # Slightly left of the line
        y=0.5*(y1_dim - y0_dim) + y0_dim,  # Middle y-coordinate
        text=f"b= {b}m",  # The label text
        showarrow=False,  # No arrow for the text itself
        font=dict(size=14, color="black"),
        xanchor='right',
        yanchor='middle',  # Align the text to appear above the line
        textangle=-90
    )

    # add A-A section the middle of foundation length b
    foundation_fig.add_shape(
        type="line",
        x0=0.8*((total_depth/2) - a/2),
        y0=b/2,
        x1=1.1*((total_depth/2) + a/2),
        y1=b/2,
        line=dict(color="black", width=2, dash='dash'),
    )   

    # add text at the begining and end of the line
    foundation_fig.add_annotation(
        x=0.8*((total_depth/2) - a/2), # x-coordinate of arrow head
        y=b/2, # y-coordinate of arrow head
        text="A",  # The label text
        showarrow=False,  # No arrow for the text itself
        font=dict(size=14, color="black"),
        xanchor='center',
        yanchor='bottom'  # Align the text to appear above the line
    )
    foundation_fig.add_annotation(
        x=1.1*((total_depth/2) + a/2), # x-coordinate of arrow head
        y=b/2, # y-coordinate of arrow head
        text="A",  # The label text
        showarrow=False,  # No arrow for the text itself
        font=dict(size=14, color="black"),
        xanchor='center',
        yanchor='bottom'  # Align the text to appear above the line
    )

    # add a point E at the center of the foundation with annotation E, show a dot at the point
    foundation_fig.add_trace(go.Scatter(
        x=[(total_depth/2)],
        y=[b/2],
        mode='markers',
        marker=dict(size=10, color='black'),
        showlegend=False,
        hoverinfo='skip'
    ))
    foundation_fig.add_annotation(
        x=(total_depth/2), # x-coordinate of arrow head
        y=b/2, # y-coordinate of arrow head
        text="E",  # The label text
        showarrow=False,  # No arrow for the text itself
        font=dict(size=14, color="black"),
        xanchor='left',
        yanchor='bottom'  # Align the text to appear above the line
    )


    for layer in layers:
        if layer['thickness'] > 0:
            # Add a line at the top and bottom of each layer
            soil_layers_fig.add_trace(go.Scatter(
                x=[0, total_depth],  # Start at -1 and end at 1
                y=[layer['top'], layer['top']],  # Horizontal line at the top of the layer
                mode='lines',
                line=dict(color='black', width=1, dash='dash'),
                showlegend=False,  # Hide legend for these lines
                hoverinfo='skip'  # Skip the hover info for these lines
            ))


    soil_layers_fig.add_trace(go.Scatter(
        x=[0, total_depth],  # Start at -1 and end at 1
        y=[water_table, water_table],  # Horizontal line at the top of the layer
        mode='lines',
        line=dict(color='blue', width=2, dash='dot'),
        showlegend=False,  # Hide legend for these lines
        hoverinfo='skip'  # Skip the hover info for these line
    )) 

    # adding arrowas distributed load on the foundation
    num_arrows = a//0.5
    for i in range(0, int(num_arrows+1)):
        soil_layers_fig.add_annotation(
            x=(total_depth/2) - (a/2) + i*0.5, # x-coordinate of arrow head
            y=0, # y-coordinate of arrow head
            ax=(total_depth/2) - (a/2) + i*0.5, # x-coordinate of tail
            ay=y_top, # y-coordinate of tail
            xref="x",
            yref="y",
            axref="x",
            ayref="y",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor="black"
        )

    soil_layers_fig.add_trace(go.Scatter(
        x=[(total_depth/2) - a/2, (total_depth/2) + a/2],  
        y=[0, 0],  # Horizontal line at the top of the layer
        mode='lines',
        line=dict(color='black', width=4, dash='solid'),
        showlegend=False,  # Hide legend for these lines
        hoverinfo='skip'  # Skip the hover info for these line
    ))

    # add A text at the begeing and end of the foundation
    soil_layers_fig.add_annotation(
        x=0.90*((total_depth/2) - a/2), # x-coordinate of arrow head   
        y=0, # y-coordinate of arrow head
        text="A",  # The label text
        showarrow=False,  # No arrow for the text itself
        font=dict(size=14, color="black"),
        xanchor='center',
        yanchor='bottom'  # Align the text to appear above the line
    )
    soil_layers_fig.add_annotation(
        x=1.05*((total_depth/2) + a/2), # x-coordinate of arrow head
        y=0, # y-coordinate of arrow head
        text="A",  # The label text
        showarrow=False,  # No arrow for the text itself
        font=dict(size=14, color="black"),
        xanchor='center',
        yanchor='bottom'  # Align the text to appear above the line
    )

    no_of_steps = int((4*a)//0.1)

    x = np.linspace((total_depth / 2) - a, (total_depth / 2) + a, int(no_of_steps/1))
    z = np.linspace(0, 2.5 * a, int(no_of_steps/1))
    X, Z = np.meshgrid(x, z)

    # Initialize I as an array filled with zeros
    I = np.zeros_like(X)

    b1 = b2 = b / 2

    for i, x_val in enumerate(x):
        
        if x_val <= (total_depth / 2) - a / 2:
            a1 = (total_depth / 2) + a / 2 - x_val
            a2 = (total_depth / 2) - a / 2 - x_val
            # print(b1, b2)
        elif x_val >= (total_depth / 2) + a / 2:
            a1 = x_val - ((total_depth / 2) - (a / 2))
            a2 = x_val - ((total_depth / 2) + (a / 2))
            # print(x_val)
        else:
            a1 = (total_depth / 2) + a / 2 - x_val
            a2 = x_val - ((total_depth / 2) - (a / 2))
            # print(x_val)

        R1 = np.sqrt(a1**2 + b1**2 + Z**2)
        R2 = np.sqrt(a2**2 + b2**2 + Z**2)

        I1 = (1 / (2 * np.pi)) * (
            (np.arctan((a1 * b1) / (R1 * Z))) + (((a1 * b1 * Z) / R1) * ((1 / ((a1**2) + (Z**2))) + (1 / ((b1**2) + (Z**2)))))
        )
        I2 = (1 / (2 * np.pi)) * (
            (np.arctan((a2 * b2) / (R2 * Z))) + (((a2 * b2 * Z) / R2) * ((1 / ((a2**2) + (Z**2))) + (1 / ((b2**2) + (Z**2)))))
        )

        if x_val <= (total_depth / 2) - a / 2 or x_val >= (total_depth / 2) + a / 2:
            I[:, i] = 2 * I1[:, i] - 2 * I2[:, i]  # Adjust to take the i-th column slice if needed
        else:
            I[:, i] = 2 * I1[:, i] + 2 * I2[:, i]  # Adjust to take the i-th column slice if needed

    # Ensure I has no negative values
    I = np.where(I < 0, 0, I)
    
    # Create the contour trace with only lines and no color fill
    contour_trace = go.Contour(
        z=I,
        x=x,
        y=z,
        contours=dict(
            start=0.1,
            end=0.9,
            size=0.1,
            showlabels=True,
            labelfont=dict(size=12, color='black')  # Ensures labels are visible
        ),
        colorscale='YlOrRd',  # Use 'Cividis' or 'Plasma' for alternatives
        showscale=False,
        showlegend=False,
        hovertemplate='J: %{z:.3f}<br>x: %{x:.3f}<br>y: %{y:.3f}<extra></extra>'
    )

    # Add the contour trace to the figure
    soil_layers_fig.add_trace(contour_trace)

    
    # First figure (soil_layers_fig)
    soil_layers_fig.update_layout(
        plot_bgcolor='white',
        # autosize=False,
        xaxis_title= dict(text='Width (m)', font=dict(size=14,weight='bold')),
        xaxis=dict(
            range=[y_top, total_depth],  # Adjusting the x-range as needed
            side = 'top',
            title_standoff=4,
            showticklabels=True,
            ticks='outside',
            ticklen=5,
            minor_ticks="inside",
            showline=True,
            linewidth=2,
            linecolor='black',
            zeroline=False,
            scaleanchor="y",  # Link x and y axes scaling
            scaleratio=1,
        ),
        yaxis_title= dict(text='Depth (m)', font=dict(size=14,weight='bold')),
        yaxis=dict(
            range=[total_depth, y_top],  # Adjusted range for the y-axis (inverted for depth)
            showticklabels=True,
            ticks='outside',
            title_standoff=4,
            ticklen=5,
            minor_ticks="inside",
            showline=True,
            linewidth=2,
            linecolor='black',
            zeroline=False,
            scaleanchor="x",  # Link y-axis scaling with x-axis
            scaleratio=1,
        ),
        margin=dict(l=30, r=10, t=10, b=20),
    )

    # Get the x-axis range from the first figure
    x_range = soil_layers_fig.layout.xaxis.range

    # Second figure (foundation_fig)
    foundation_fig.update_layout(
        plot_bgcolor='white',
        dragmode=False,  # Disable zooming and panning
        autosize=False,
        xaxis=dict(
            range=x_range,  # Set the same x-range as soil_layers_fig
            showticklabels=False,
            title_standoff=4,
            showgrid=False,
            showline=False,
            title=None,
            zeroline=False,
            fixedrange=True
        ),
        yaxis=dict(
            range=[0, a],  # Adjusted range for the y-axis in this figure
            showticklabels=False,
            title_standoff=4,
            showgrid=False,
            showline=False,
            title=None,
            zeroline=False,
            fixedrange=True,
            scaleanchor="x",  # Link y-axis scaling with x-axis
            scaleratio=1,
        ),
        margin=dict(l=90, r=40, t=10, b=10),
    )

    # Third figure (stress_change_fig)
    step = delta_h =0.05
    depths = np.linspace(0, z1 + z2 + z3, num=int((z1 + z2 + z3)/step) + 1, endpoint=True)  # Define depths from 0 to total depth
    stress_change = np.zeros_like(depths)
    settelment = np.zeros_like(depths)

    # Calculate change in stress based on the conditions
    for i, depth in enumerate(depths):
        # claculate I for each depth
        a_E = a/2
        b_E = b/2
        R= np.sqrt(a_E**2 + b_E**2 + depth**2)
        I = (1 / (2 * np.pi)) * (
            (np.arctan((a_E * b_E) / (R * depth))) + (((a_E * b_E * depth) / R) * ((1 / ((a_E**2) + (depth**2))) + (1 / ((b_E**2) + (depth**2)))))
        )
        stress_change[i] = 4* I * q

    stress_change_fig.add_trace(go.Scatter(
        x=stress_change,
        y=depths,
        mode='lines',
        line=dict(color='red', width=3 ),
        name='Stress increment with depth under point E, Δσ<sub>z,E</sub>',
        showlegend=True,
    ))

    # add point dot with annottion for E point at the 0 level of the trace line
    stress_change_fig.add_trace(go.Scatter(
        x=[max(stress_change)],
        y=[0],
        mode='markers',
        marker=dict(size=10, color='black'),
        showlegend=False,
        hoverinfo='skip'
    ))
    stress_change_fig.add_annotation(
        x=max(stress_change), # x-coordinate of arrow head
        y=0, # y-coordinate of arrow head
        text="E",  # The label text
        showarrow=False,  # No arrow for the text itself
        font=dict(size=14, color="black"),
        xanchor='left',
        yanchor='top'  # Align the text to appear above the line
    )

    for layer in layers:
        if layer['thickness'] > 0:
            # Add a line at the bottom of each layer other graph
            stress_change_fig.add_trace(go.Scatter(
                x=[0, 1.2 * max(stress_change)],  # Start at -1 and end at 1
                y=[layer['top'], layer['top']],  # Horizontal line at the top of the layer
                mode='lines',
                line=dict(color='black', width=1, dash='dash'),
                showlegend=False,  # Hide legend for these lines
                hoverinfo='skip'  # Skip the hover info for these line
            ))

    # Settelment calculations per depth level under point E
    sigma_i = np.zeros_like(depths)
    sigma_f = np.zeros_like(depths)
    sigma_p = np.zeros_like(depths)
    total_settelment = 0
    # OCR = sigma_c/sigma_i
    for i, depth in enumerate(depths):
        if depth <= z1:
            if depth <= water_table:
                sigma_i[i] = depth * gamma_1
            else:
                sigma_i[i] = water_table * gamma_1 + (depth - water_table) * (gamma_r_1 - gamma_water)

            sigma_f[i] = sigma_i[i] + stress_change[i]
            sigma_p[i] = OCR_1 * sigma_i[i]
            
            if OCR_1 == 1:
                settelment[i] = 1000*(delta_h/(1+e_0_1)) * C_c_1 * np.log(sigma_f[i]/sigma_i[i])
            elif OCR_1 > 1 and sigma_f[i] <= sigma_p[i]:
                settelment[i] = 1000*(delta_h/(1+e_0_1)) * C_s_1 * np.log(sigma_f[i]/sigma_i[i])
            elif OCR_1 > 1 and sigma_f[i] > sigma_p[i]:
                settelment[i] = 1000*(delta_h/(1+e_0_1)) * ((C_s_1 * np.log(sigma_p[i]/sigma_i[i])) + 
                                                        (C_c_1 * np.log(sigma_f[i]/sigma_p[i])))

        elif depth > z1 and depth <= z1 + z2:
            if depth <= water_table:
                sigma_i[i] = sigma_i[int(z1/step)]+ (depth - z1) * gamma_2
            else:
                sigma_i[i] = sigma_i[int(z1/step)]+ (depth - z1) * (gamma_r_2 - gamma_water) 

            sigma_f[i] = sigma_i[i] + stress_change[i]
            sigma_p[i] = OCR_2 * sigma_i[i]

            if OCR_2 == 1:
                settelment[i] = 1000*(delta_h/(1+e_0_2)) * C_c_2 * np.log(sigma_f[i]/sigma_i[i])
            elif OCR_2 > 1 and sigma_f[i] <= sigma_p[i]:
                settelment[i] = 1000*(delta_h/(1+e_0_2)) * C_s_2 * np.log(sigma_f[i]/sigma_i[i])
            elif OCR_2 > 1 and sigma_f[i] > sigma_p[i]:
                settelment[i] = 1000*(delta_h/(1+e_0_2)) * ((C_s_2 * np.log(sigma_p[i]/sigma_i[i])) + 
                                                        (C_c_2 * np.log(sigma_f[i]/sigma_p[i])))
        else:
            if depth <= water_table:
                sigma_i[i] = sigma_i[int((z1 + z2)/step)]+ (depth - z1 - z2) * gamma_3
            else:
                sigma_i[i] = sigma_i[int((z1 + z2)/step)]+ (depth - z1 - z2) * (gamma_r_3 - gamma_water)

            sigma_f[i] = sigma_i[i] + stress_change[i]
            sigma_p[i] = OCR_3 * sigma_i[i]

            if OCR_3 == 1:
                settelment[i] = 1000*(delta_h/(1+e_0_3)) * C_c_3 * np.log(sigma_f[i]/sigma_i[i])
            elif OCR_3 > 1 and sigma_f[i] <= sigma_p[i]:
                settelment[i] = 1000*(delta_h/(1+e_0_3)) * C_s_3 * np.log(sigma_f[i]/sigma_i[i])
            elif OCR_3 > 1 and sigma_f[i] > sigma_p[i]:
                settelment[i] = 1000* (delta_h/(1+e_0_3)) * ((C_s_3 * np.log(sigma_p[i]/sigma_i[i])) + 
                                                        (C_c_3 * np.log(sigma_f[i]/sigma_p[i])))
        settelment[0] = settelment[1]  
        total_settelment += settelment[i]
    total_settelment -= settelment[0]
    
    stress_change_fig.add_trace(go.Scatter(
        x=settelment,
        y=depths,
        mode='lines',
        xaxis='x2',
        line=dict(color='green', width=3 ),
        name='Settelment with depth under point E, Δ𝜌<sub>z,E</sub>',
        showlegend=True,
    ))

        # add point dot with annottion for E point at the 0 level of the trace line
    stress_change_fig.add_trace(go.Scatter(
        x=[max(settelment)],
        y=[0],
        mode='markers',
        xaxis='x2',
        marker=dict(size=10, color='black'),
        showlegend=False,
        hoverinfo='skip'
    ))
    stress_change_fig.add_annotation(
        x=max(settelment), # x-coordinate of arrow head
        y=0, # y-coordinate of arrow head
        xref='x2',
        text="E",  # The label text
        showarrow=False,  # No arrow for the text itself
        font=dict(size=14, color="black"),
        xanchor='left',
        yanchor='top'  # Align the text to appear above the line
    )
            


    # print(step, settelment)

    stress_change_fig.update_layout(
        xaxis_title=dict(text='Δσ<sub>z,E</sub> (kPa)', font=dict(size=14, weight='bold')),
        plot_bgcolor='white',
        xaxis=dict(
            range=[0, 1.2 * max(stress_change)],
            side='top',
            title_standoff=4,
            zeroline=False,
            showticklabels=True,
            ticks='outside',
            ticklen=5,
            minor_ticks="inside",
            showline=True,
            linewidth=2,
            linecolor='black',
            showgrid=False,
            gridwidth=1,
            gridcolor='lightgrey',
            mirror=True,
            hoverformat=".2f"  # Sets hover value format for x-axis to two decimal places
        ),
        xaxis2=dict(  # Second x-axis (Displacement)
            title=dict(text='Δ𝜌<sub>z,E</sub> (mm)', font=dict(size=12, weight='bold')),
            overlaying='x',  # Share the same space as the first x-axis
            title_standoff=1,
            side='top',   
            position = ((total_depth)/(total_depth-y_top)), 
            anchor='free', 
            showticklabels=True,
            ticks='outside',
            ticklen=3,
            minor_ticks="inside",
            showline=True,
            linewidth=2,
            linecolor='black',
            showgrid=False,
            gridwidth=1,
            gridcolor='lightgrey',
            mirror=True,
            hoverformat=".2f",  # Sets hover value format for x-axis to two decimal places
            range=[0,  1.4* max(settelment)],  # Match the range of the first x-axis
        ),
        yaxis_title=dict(text='Depth (m)', font=dict(size=14, weight='bold')),
        yaxis=dict(
            range=[total_depth, y_top],
            zeroline=False,
            title_standoff=4,
            showticklabels=True,
            ticks='outside',
            ticklen=5,
            minor_ticks="inside",
            showline=True,
            linewidth=2,
            linecolor='black',
            showgrid=False,
            gridwidth=1,
            gridcolor='lightgrey',
            mirror=True,
            hoverformat=".2f"  # Sets hover value format for y-axis to two decimal places
        ),
        legend=dict(
            yanchor="bottom",  # Align the bottom of the legend box
            y=0,               # Position the legend at the bottom inside the plot
            xanchor="right",    # Align the right edge of the legend box
            x=1,               # Position the legend at the right inside the plot
            font= dict(size=9),  # Adjust font size
            bgcolor="rgba(255, 255, 255, 0.7)",  # Optional: Semi-transparent white background
            bordercolor="black",                 # Optional: Border color
            borderwidth=1                        # Optional: Border width
        ),
        margin=dict(l=30, r=10, t=10, b=20),
    )




    return foundation_fig, soil_layers_fig, stress_change_fig, f"Total settelment under point E = {total_settelment:.2f} mm"

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
    

# Expose the server
server = app.server
