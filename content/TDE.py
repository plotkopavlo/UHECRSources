from ipywidgets import GridspecLayout, Layout, Box
import ipywidgets as widgets
import numpy as np
radius = np.array([5.00e16,  7.34e16,  1.08e17,  1.58e17,  2.32e17, 3.41e17,  5.00e17,  7.34e17,  1.08e18, 1.58e18, 2.32e18, 3.41e18, 5.00e18])
rigidity_max =  np.array([1.00e9,  1.39e9,  1.92e9,  2.66e9,  3.68e9,  5.10e9,  7.07e9,  9.80e9,  1.36e10,  1.88e10, 2.61e10, 3.61e10, 5.00e10])
grid_param_dsg = GridspecLayout(3, 3)
grid_param_dsg[0,0] = widgets.HTML(value="<h2>Paramaters  </h2>",)
grid_param_dsg[1,0] = widgets.Dropdown(options=radius.tolist(), description="Radius [cm]")
grid_param_dsg[1,1] = widgets.Dropdown(options=rigidity_max.tolist(), description="R_max [GeV]")
grid_param_dsg[1,2] = widgets.Dropdown(options=[0.1], description="dsg B")
grid_param_dsg[2,0] = widgets.BoundedFloatText(value=7.5, min=0, max=1e6, step=0.1, description='local rate:', disabled=False)
grid_param_dsg[2,1] = widgets.BoundedFloatText(value=0.020, min=0, max=5.0, step=0.001, description='radshift:', disabled=False )
grid_comp_dsg = GridspecLayout(4, 4)
grid_comp_dsg[0,0] = widgets.HTML(value="<h2> Composition  </h2>",)
grid_comp_dsg[1:3,0] =widgets.RadioButtons(options=['MS', 'RSG', 'WR', 'CO-WD', 'ONeMg-WD', 'Free'], description='Composition:', disabled=False)
grid_comp_dsg[1,1] = widgets.BoundedFloatText(value=1.0,  min=0, max=1,   step=0.1, description='H:', disabled=True)
grid_comp_dsg[2,1] = widgets.BoundedFloatText(value=0.42, min=0, max=100, step=0.1, description='He:',disabled=False)
grid_comp_dsg[1,2] = widgets.BoundedFloatText(value=0.42, min=0, max=100, step=0.1, description='C:', disabled=False)
grid_comp_dsg[2,2] = widgets.BoundedFloatText(value=0.42, min=0, max=100, step=0.1, description='N:', disabled=False)
grid_comp_dsg[3,2] = widgets.BoundedFloatText(value=0.42, min=0, max=100, step=0.1, description='O:', disabled=False)
grid_comp_dsg[1,3] = widgets.BoundedFloatText(value=0.42, min=0, max=100, step=0.1, description='Na:', disabled=False)
grid_comp_dsg[2,3] = widgets.BoundedFloatText(value=0.42, min=0, max=100, step=0.1, description='Si:', disabled=False)
grid_comp_dsg[3,3] = widgets.BoundedFloatText(value=0.42, min=0, max=100, step=0.1, description='Fe:', disabled=False)

grid_param_fdr = GridspecLayout(3, 3)
grid_param_fdr[0,0] = widgets.HTML(value="<h2>Paramaters  </h2>",)
grid_param_fdr[1,0] = widgets.Dropdown(options=radius.tolist(), description="Radius [cm]")
grid_param_fdr[1,1] = widgets.Dropdown(options=rigidity_max.tolist(), description="R_max [GeV]")
grid_param_fdr[1,2] = widgets.Dropdown(options=[0.1], description="dsg B")
grid_param_fdr[2,0] = widgets.BoundedFloatText(value=7.5, min=0, max=1e6, step=0.1, description='local rate:', disabled=False)
grid_param_fdr[2,1] = widgets.BoundedFloatText(value=0.020, min=0, max=5.0, step=0.001, description='radshift:', disabled=False )
grid_comp_fdr = GridspecLayout(4, 4)
grid_comp_fdr[0,0] = widgets.HTML(value="<h2> Composition  </h2>",)
grid_comp_fdr[1:3,0] =widgets.RadioButtons(options=['MS', 'RSG', 'WR', 'CO-WD', 'ONeMg-WD', 'Free'], description='Composition:', disabled=False)
grid_comp_fdr[1,1] = widgets.BoundedFloatText(value=1.0,  min=0, max=1,   step=0.1, description='H:', disabled=True)
grid_comp_fdr[2,1] = widgets.BoundedFloatText(value=0.42, min=0, max=100, step=0.1, description='He:',disabled=False)
grid_comp_fdr[1,2] = widgets.BoundedFloatText(value=0.42, min=0, max=100, step=0.1, description='C:', disabled=False)
grid_comp_fdr[2,2] = widgets.BoundedFloatText(value=0.42, min=0, max=100, step=0.1, description='N:', disabled=False)
grid_comp_fdr[3,2] = widgets.BoundedFloatText(value=0.42, min=0, max=100, step=0.1, description='O:', disabled=False)
grid_comp_fdr[1,3] = widgets.BoundedFloatText(value=0.42, min=0, max=100, step=0.1, description='Na:', disabled=False)
grid_comp_fdr[2,3] = widgets.BoundedFloatText(value=0.42, min=0, max=100, step=0.1, description='Si:', disabled=False)
grid_comp_fdr[3,3] = widgets.BoundedFloatText(value=0.42, min=0, max=100, step=0.1, description='Fe:', disabled=False)


grid_param_aalc = GridspecLayout(3, 3)
grid_param_aalc[0,0] = widgets.HTML(value="<h2>Paramaters  </h2>",)
grid_param_aalc[1,0] = widgets.Dropdown(options=radius.tolist(), description="Radius [cm]")
grid_param_aalc[1,1] = widgets.Dropdown(options=rigidity_max.tolist(), description="R_max [GeV]")
grid_param_aalc[1,2] = widgets.Dropdown(options=[0.1], description="dsg B")
grid_param_aalc[2,0] = widgets.BoundedFloatText(value=7.5, min=0, max=1e6, step=0.1, description='local rate:', disabled=False)
grid_param_aalc[2,1] = widgets.BoundedFloatText(value=0.020, min=0, max=5.0, step=0.001, description='radshift:', disabled=False )
grid_comp_aalc = GridspecLayout(4, 4)
grid_comp_aalc[0,0] = widgets.HTML(value="<h2> Composition  </h2>",)
grid_comp_aalc[1:3,0] =widgets.RadioButtons(options=['MS', 'RSG', 'WR', 'CO-WD', 'ONeMg-WD', 'Free'], description='Composition:', disabled=False)
grid_comp_aalc[1,1] = widgets.BoundedFloatText(value=1.0,  min=0, max=1,   step=0.1, description='H:', disabled=True)
grid_comp_aalc[2,1] = widgets.BoundedFloatText(value=0.42, min=0, max=100, step=0.1, description='He:',disabled=False)
grid_comp_aalc[1,2] = widgets.BoundedFloatText(value=0.42, min=0, max=100, step=0.1, description='C:', disabled=False)
grid_comp_aalc[2,2] = widgets.BoundedFloatText(value=0.42, min=0, max=100, step=0.1, description='N:', disabled=False)
grid_comp_aalc[3,2] = widgets.BoundedFloatText(value=0.42, min=0, max=100, step=0.1, description='O:', disabled=False)
grid_comp_aalc[1,3] = widgets.BoundedFloatText(value=0.42, min=0, max=100, step=0.1, description='Na:', disabled=False)
grid_comp_aalc[2,3] = widgets.BoundedFloatText(value=0.42, min=0, max=100, step=0.1, description='Si:', disabled=False)
grid_comp_aalc[3,3] = widgets.BoundedFloatText(value=0.42, min=0, max=100, step=0.1, description='Fe:', disabled=False)
items_layout = Layout( width='auto')     # override the default width of the button to 'auto' to let the button grow

box_layout = Layout(display='flex',
                    flex_flow='column', 
                    align_items='stretch', 
                    border='solid',
                    width='70%')

words = ['correct', 'horse', 'battery', 'staple']
items_dsg = [widgets.Checkbox( value=False, description='dsg',disabled=False), grid_param_dsg, grid_comp_dsg]
box_dsg = Box(children=items_dsg, layout=box_layout)

items_fdr = [widgets.Checkbox( value=False, description='fdr',disabled=False), grid_param_fdr, grid_comp_fdr]
box_fdr = Box(children=items_fdr, layout=box_layout)

items_aalc = [widgets.Checkbox( value=False, description='aalc',disabled=False), grid_param_aalc, grid_comp_aalc]
box_aalc = Box(children=items_aalc, layout=box_layout)

box_TDEs = Box(children=[box_dsg, box_fdr, box_aalc], layout=box_layout)
box_TDEs
