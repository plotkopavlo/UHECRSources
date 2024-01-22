from ipywidgets import GridspecLayout, Layout, Box
import ipywidgets as widgets
import numpy as np
radius = np.array([5.00e16,  7.34e16,  1.08e17,  1.58e17,  2.32e17, 3.41e17,  5.00e17,  7.34e17,  1.08e18, 1.58e18, 2.32e18, 3.41e18, 5.00e18])
rigidity_max =  np.array([1.00e9,  1.39e9,  1.92e9,  2.66e9,  3.68e9,  5.10e9,  7.07e9,  9.80e9,  1.36e10,  1.88e10, 2.61e10, 3.61e10, 5.00e10])/1e9
grid_param_dsg = GridspecLayout(3, 3)
grid_param_dsg[0,0] = widgets.HTML(value="<h2>Paramaters  </h2>",)
grid_param_dsg[1,0] = widgets.Dropdown(options=radius.tolist(), description="Radius [cm]", layout={'width': 'max-content'})
grid_param_dsg[1,1] = widgets.Dropdown(options=rigidity_max.tolist(), description="R_max [1e9 GeV]", layout={'width': 'max-content'})
grid_param_dsg[1,2] = widgets.Dropdown(options=[0.1], description="B [G]", layout={'width': 'max-content'})
grid_param_dsg[2,0] = widgets.BoundedFloatText(value=7.5, min=0, max=1e6, step=0.1, description='local rate:', disabled=False, layout={'width': 'max-content'})
grid_param_dsg[2,1] = widgets.BoundedFloatText(value=0.020, min=0, max=5.0, step=0.001, description='radshift:', disabled=False, layout={'width': 'max-content'} )
grid_comp_dsg = GridspecLayout(4, 4)
grid_comp_dsg[0,0] = widgets.HTML(value="<h2> Composition  </h2>",)
grid_comp_dsg[1:3,0] =widgets.RadioButtons(options=['MS', 'RSG', 'WR', 'CO-WD', 'ONeMg-WD', 'Free'], description='Composition:', disabled=False)
grid_comp_dsg[1,1] = widgets.BoundedFloatText(value=12.5,  min=0, max=1,   step=0.1, description='H %:', disabled=False, layout={'width': 'max-content'})
grid_comp_dsg[2,1] = widgets.BoundedFloatText(value=12.5, min=0, max=100, step=0.1, description='He %:',disabled=False, layout={'width': 'max-content'})
grid_comp_dsg[1,2] = widgets.BoundedFloatText(value=12.5, min=0, max=100, step=0.1, description='C %:', disabled=False, layout={'width': 'max-content'})
grid_comp_dsg[2,2] = widgets.BoundedFloatText(value=12.5, min=0, max=100, step=0.1, description='N %:', disabled=False, layout={'width': 'max-content'})
grid_comp_dsg[3,2] = widgets.BoundedFloatText(value=12.5, min=0, max=100, step=0.1, description='O %:', disabled=False, layout={'width': 'max-content'})
grid_comp_dsg[1,3] = widgets.BoundedFloatText(value=12.5, min=0, max=100, step=0.1, description='Na %:', disabled=False, layout={'width': 'max-content'})
grid_comp_dsg[2,3] = widgets.BoundedFloatText(value=12.5, min=0, max=100, step=0.1, description='Si %:', disabled=False, layout={'width': 'max-content'})
grid_comp_dsg[3,3] = widgets.BoundedFloatText(value=12.5, min=0, max=100, step=0.1, description='Fe %:', disabled=True, layout={'width': 'max-content'})

grid_param_fdr = GridspecLayout(3, 3)
grid_param_fdr[0,0] = widgets.HTML(value="<h2>Paramaters  </h2>",)
grid_param_fdr[1,0] = widgets.Dropdown(options=radius.tolist(), description="Radius [cm]", layout={'width': 'max-content'})
grid_param_fdr[1,1] = widgets.Dropdown(options=rigidity_max.tolist(), description="R_max [1e9 GeV]", layout={'width': 'max-content'})
grid_param_fdr[1,2] = widgets.Dropdown(options=[0.1], description="B [G]", layout={'width': 'max-content'})
grid_param_fdr[2,0] = widgets.BoundedFloatText(value=7.5, min=0, max=1e6, step=0.1, description='local rate:', disabled=False, layout={'width': 'max-content'})
grid_param_fdr[2,1] = widgets.BoundedFloatText(value=0.020, min=0, max=5.0, step=0.001, description='radshift:', disabled=False, layout={'width': 'max-content'} )
grid_comp_fdr = GridspecLayout(4, 4)
grid_comp_fdr[0,0] = widgets.HTML(value="<h2> Composition  </h2>",)
grid_comp_fdr[1:3,0] =widgets.RadioButtons(options=['MS', 'RSG', 'WR', 'CO-WD', 'ONeMg-WD', 'Free'], description='Composition:', disabled=False)
grid_comp_fdr[1,1] = widgets.BoundedFloatText(value=12.5,  min=0, max=1,   step=0.1, description='H %:', disabled=False, layout={'width': 'max-content'})
grid_comp_fdr[2,1] = widgets.BoundedFloatText(value=12.5, min=0, max=100, step=0.1, description='He %:',disabled=False, layout={'width': 'max-content'})
grid_comp_fdr[1,2] = widgets.BoundedFloatText(value=12.5, min=0, max=100, step=0.1, description='C %:', disabled=False, layout={'width': 'max-content'})
grid_comp_fdr[2,2] = widgets.BoundedFloatText(value=12.5, min=0, max=100, step=0.1, description='N %:', disabled=False, layout={'width': 'max-content'})
grid_comp_fdr[3,2] = widgets.BoundedFloatText(value=12.5, min=0, max=100, step=0.1, description='O %:', disabled=False, layout={'width': 'max-content'})
grid_comp_fdr[1,3] = widgets.BoundedFloatText(value=12.5, min=0, max=100, step=0.1, description='Na %:', disabled=False, layout={'width': 'max-content'})
grid_comp_fdr[2,3] = widgets.BoundedFloatText(value=12.5, min=0, max=100, step=0.1, description='Si %:', disabled=False, layout={'width': 'max-content'})
grid_comp_fdr[3,3] = widgets.BoundedFloatText(value=12.5, min=0, max=100, step=0.1, description='Fe %:', disabled=True, layout={'width': 'max-content'})


grid_param_aalc = GridspecLayout(3, 3)
grid_param_aalc[0,0] = widgets.HTML(value="<h2>Paramaters  </h2>",)
grid_param_aalc[1,0] = widgets.Dropdown(options=radius.tolist(), description="Radius [cm]", layout={'width': 'max-content'})
grid_param_aalc[1,1] = widgets.Dropdown(options=rigidity_max.tolist(), description="R_max [1e9 GeV]", layout={'width': 'max-content'})
grid_param_aalc[1,2] = widgets.Dropdown(options=[0.1], description="B [G]", layout={'width': 'max-content'})
grid_param_aalc[2,0] = widgets.BoundedFloatText(value=7.5, min=0, max=1e6, step=0.1, description='local rate:', disabled=False, layout={'width': 'max-content'})
grid_param_aalc[2,1] = widgets.BoundedFloatText(value=0.020, min=0, max=5.0, step=0.001, description='radshift:', disabled=False, layout={'width': 'max-content'} )
grid_comp_aalc = GridspecLayout(4, 4)
grid_comp_aalc[0,0] = widgets.HTML(value="<h2> Composition  </h2>",)
grid_comp_aalc[1:3,0] =widgets.RadioButtons(options=['MS', 'RSG', 'WR', 'CO-WD', 'ONeMg-WD', 'Free'], description='Composition:', disabled=False)
grid_comp_aalc[1,1] = widgets.BoundedFloatText(value=12.5,  min=0, max=1,   step=0.1, description='H %:', disabled=False, layout={'width': 'max-content'})
grid_comp_aalc[2,1] = widgets.BoundedFloatText(value=12.5, min=0, max=100, step=0.1, description='He %:',disabled=False, layout={'width': 'max-content'})
grid_comp_aalc[1,2] = widgets.BoundedFloatText(value=12.5, min=0, max=100, step=0.1, description='C %:', disabled=False, layout={'width': 'max-content'})
grid_comp_aalc[2,2] = widgets.BoundedFloatText(value=12.5, min=0, max=100, step=0.1, description='N %:', disabled=False, layout={'width': 'max-content'})
grid_comp_aalc[3,2] = widgets.BoundedFloatText(value=12.5, min=0, max=100, step=0.1, description='O %:', disabled=False, layout={'width': 'max-content'})
grid_comp_aalc[1,3] = widgets.BoundedFloatText(value=12.5, min=0, max=100, step=0.1, description='Na %:', disabled=False, layout={'width': 'max-content'})
grid_comp_aalc[2,3] = widgets.BoundedFloatText(value=12.5, min=0, max=100, step=0.1, description='Si %:', disabled=False, layout={'width': 'max-content'})
grid_comp_aalc[3,3] = widgets.BoundedFloatText(value=12.5, min=0, max=100, step=0.1, description='Fe %:', disabled=True, layout={'width': 'max-content'})


grid_param_cr_data = GridspecLayout(3, 1)
grid_param_cr_data[0,0] = widgets.HTML(value="UHECR data")
grid_param_cr_data[1,0] = widgets.Checkbox(
                        value=True,
                        description='Auger 2019',
                        disabled=False,
                        indent=False
                    )

grid_param_cr_data[2,0] = widgets.Checkbox(
                        value=True,
                        description='TA 2019',
                        disabled=False,
                        indent=False
                    )

grid_param_nu_sens = GridspecLayout(4, 1)

grid_param_nu_sens[0,0] = widgets.HTML(value="Neutrino sensetivity")
grid_param_nu_sens[1,0] = widgets.Checkbox(
                        value=True,
                        description='IceCube-Gen2',
                        disabled=False,
                        indent=False
                    )

grid_param_nu_sens[2,0] = widgets.Checkbox(
                        value=True,
                        description='RNO-G',
                        disabled=False,
                        indent=False
                    )

grid_param_nu_sens[3,0] = widgets.Checkbox(
                        value=True,
                        description='GRAND',
                        disabled=False,
                        indent=False
                    )

grid_param_plot = GridspecLayout(2, 3)



grid_param_plot[0,0] = widgets.HTML(value="<h2>Plot Settings  </h2>",)
grid_param_plot[1,0] = grid_param_cr_data
grid_param_plot[1,1] = widgets.RadioButtons(options=['EPOS-LHC', 'SIBYLL2.3d', 'SIBYLL2.3c', 'QGSJET-II04'], description='Air Shower model:', disabled=False)
grid_param_plot[1,2] = grid_param_nu_sens


grid_param_buttons = GridspecLayout(1, 4)



grid_param_buttons[0,0] = widgets.Button(
                        description='Create Plot',
                        disabled=False,
                        button_style='', # 'success', 'info', 'warning', 'danger' or ''
                        tooltip='Click me',
                        icon='check' # (FontAwesome names without the `fa-` prefix)
                    )
grid_param_buttons[0,1] = widgets.Button(
                        description='Fit Data',
                        disabled=False,
                        button_style='', # 'success', 'info', 'warning', 'danger' or ''
                        tooltip='Click me',
                        icon='check' # (FontAwesome names without the `fa-` prefix)
                    )
grid_param_buttons[0,2] = widgets.Button(
                        description='Save Plot',
                        disabled=False,
                        button_style='', # 'success', 'info', 'warning', 'danger' or ''
                        tooltip='Click me',
                        icon='check' # (FontAwesome names without the `fa-` prefix)
                    )
grid_param_buttons[0,3] = widgets.Button(
                        description='Save Data',
                        disabled=False,
                        button_style='', # 'success', 'info', 'warning', 'danger' or ''
                        tooltip='Click me',
                        icon='check' # (FontAwesome names without the `fa-` prefix)
                    )




box_layout = Layout(display='flex',
                    flex_flow='column', 
                    align_items='stretch', 
                    border='solid',
                    width='100%')

words = ['correct', 'horse', 'battery', 'staple']
widgets.HTML(value="<h1>DSG </h1>")
items_dsg = [widgets.HTML(value="<h1>dsg </h1>"), widgets.Checkbox( value=False, description='inculde to the plot',disabled=False), grid_param_dsg, grid_comp_dsg]
box_dsg = Box(children=items_dsg, layout=box_layout)

items_fdr = [widgets.HTML(value="<h1>fdr </h1>"), widgets.Checkbox( value=False, description='inculde to the plo',disabled=False), grid_param_fdr, grid_comp_fdr]
box_fdr = Box(children=items_fdr, layout=box_layout)

items_aalc = [widgets.HTML(value="<h1>aalc </h1>"), widgets.Checkbox( value=False, description='inculde to the plo',disabled=False), grid_param_aalc, grid_comp_aalc]
box_aalc = Box(children=items_aalc, layout=box_layout)

box_TDEs = Box(children=[box_dsg, box_fdr, box_aalc, grid_param_plot,grid_param_buttons], layout=box_layout)
