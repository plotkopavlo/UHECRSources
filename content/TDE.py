class TDEsUI:
    from ipywidgets import GridspecLayout, Layout, Box
    import ipywidgets as widgets
    import numpy as np
    import io
    import matplotlib.pyplot as plt
    import seaborn as sns
    from astropy.visualization import quantity_support
    import pickle
    
    import io
    def __init__(self):
        import pickle
        with open("spectra_data.pkl", "rb") as file:
            self.spectra_data = pickle.load(file)
        self.radius = np.array([5.00e16,  7.34e16,  1.08e17,  1.58e17,  2.32e17, 3.41e17,  5.00e17,  7.34e17,  1.08e18, 1.58e18, 2.32e18, 3.41e18, 5.00e18])
        self.rigidity_max = np.array([1.00e9,  1.39e9,  1.92e9,  2.66e9,  3.68e9,  5.10e9,  7.07e9,  9.80e9,  1.36e10,  1.88e10, 2.61e10, 3.61e10, 5.00e10])/1e9
        self.B_field = np.array([0.1])
        self.input_spec = [101, 402, 1206, 1407,1608, 2311, 2814, 5626]
        
        self.error_comp_massage ='<span style="color: red;">Error: Total composition exceeds 100%</span>'

        self.composition_values = {
            'MS': np.array([73.9, 24.7, 0.22, 0.07, 0.63, 0.23, 0.07, 0.12])/100,
            'RSG': np.array([46.46, 36.74, 0.95 , 0.30, 2.72, 0.99, 0.3, 0.52])/100,
            'WR': np.array([0.00633, 98.1, 0.0292 , 1.33, 0.0321, 0.2573, 0.0734, 0.136])/100,
            'CO-WD': np.array([1e-5, 1e-5, 50, 1e-5, 50, 1e-5, 1e-5, 1e-5])/100,
            'ONeMg-WD': np.array([1e-5, 1e-5, 1e-5, 1e-5, 12, 88, 1e-5, 1e-5])/100
        }
        self.air_shower_model_names = ['EPOS-LHC', 'SIBYLL2.3d', 'SIBYLL2.3c', 'QGSJET-II04']
        self.air_shower_model = {
            'name': 'EPOS-LHC',
            'model': None,
        }

        

        self.dsg_parameters = {
            "local_rate": 50,
            "z": 0.020,
            "radius_index": 0,
            "r_max_index": 0,
            "b_field_index": 0, 
            "comp": np.zeros(8)+12.5/100,
            "comp_checked": True,
            "include": True,
        }

        self.fdr_parameters = {
            "local_rate": 50,
            "z": 0.020,
            "radius_index": 0,
            "r_max_index": 0,
            "b_field_index": 0, 
            "comp": np.zeros(8)+12.5/100,
            "comp_checked": True,
            "include": True,

        }

        self.aalc_parameters = {
            "local_rate": 50,
            "z": 0.020,
            "radius_index": 0,
            "r_max_index": 0,
            "b_field_index": 0, 
            "comp": np.zeros(8)+12.5/100,
            "comp_checked": True,
            "include": True,

        }


        self.parameters_best_fit_scenario={
            "Star Mass Abundance":{
                "dsg":{
                    "parameters":{
                        "local_rate": 32.45,
                        "z": 0.020,
                        "radius_index": 4,
                        "r_max_index": 4,
                        "b_field_index": 0, 
                        "comp":  self.composition_values["ONeMg-WD"],
                        "comp_checked": True,
                        "include": True,  
                    },

                    "comp_type": "ONeMg-WD"

                },
                "fdr":{
                    "parameters":{
                        "local_rate": 5.23,
                        "z": 0.020,
                        "radius_index": 3,
                        "r_max_index": 10,
                        "b_field_index": 0, 
                        "comp": self.composition_values["WR"],
                        "comp_checked": True,
                        "include": True,  
                    },

                    "comp_type": "WR"

                },
                "aalc":{
                    "parameters":{
                        "local_rate": 32.45,
                        "z": 0.020,
                        "radius_index": 4,
                        "r_max_index": 4,
                        "b_field_index": 0, 
                        "comp":  self.composition_values["ONeMg-WD"],
                        "comp_checked": True,
                        "include": True,  
                    },

                    "comp_type": "ONeMg-WD"

                },
                "syst":{
                    "Auger":{
                        "E": -8.3,
                        "Xmean": -148,
                        "SigmaXmean": 0.0
                    },
                    "TA":{
                        "E": 0.0,
                        "Xmean": 0.0,
                        "SigmaXmean": 0.0
                    }
                },
                "airshower": "EPOS-LHC",
                "cr":{
                        "Auger": True,
                        "TA": False,
                }
            },
            "MS star":{
                "dsg":{
                    "parameters":{
                        "local_rate": 220.24,
                        "z": 0.020,
                        "radius_index": 10,
                        "r_max_index": 3,
                        "b_field_index": 0, 
                        "comp":  self.composition_values["MS"],
                        "comp_checked": True,
                        "include": True,  
                    },

                    "comp_type": "MS"

                },
                "fdr":{
                    "parameters":{
                        "local_rate": 220.24,
                        "z": 0.020,
                        "radius_index": 12,
                        "r_max_index": 8,
                        "b_field_index": 0, 
                        "comp": self.composition_values["MS"],
                        "comp_checked": True,
                        "include": True,  
                    },

                    "comp_type": "MS"

                },
                "aalc":{
                    "parameters":{
                        "local_rate": 220.24,
                        "z": 0.020,
                        "radius_index": 10,
                        "r_max_index": 3,
                        "b_field_index": 0, 
                        "comp":  self.composition_values["MS"],
                        "comp_checked": True,
                        "include": True,  
                    },

                    "comp_type": "MS"

                },
                "syst":{
                    "Auger":{
                        "E": -42.0,
                        "Xmean": 300,
                        "SigmaXmean": 0.0
                    },
                    "TA":{
                        "E": 0.0,
                        "Xmean": 0.0,
                        "SigmaXmean": 0.0
                    }
                },
                "airshower": "EPOS-LHC",
                "cr":{
                        "Auger": True,
                        "TA": False,
                }
            },
            "RSG star":{
                "dsg":{
                    "parameters":{
                        "local_rate": 238.55,
                        "z": 0.020,
                        "radius_index": 9,
                        "r_max_index": 1,
                        "b_field_index": 0, 
                        "comp":  self.composition_values["RSG"],
                        "comp_checked": True,
                        "include": True,  
                    },

                    "comp_type": "RSG"

                },
                "fdr":{
                    "parameters":{
                        "local_rate": 238.55,
                        "z": 0.020,
                        "radius_index": 12,
                        "r_max_index": 8,
                        "b_field_index": 0, 
                        "comp": self.composition_values["RSG"],
                        "comp_checked": True,
                        "include": True,  
                    },

                    "comp_type": "RSG"

                },
                "aalc":{
                    "parameters":{
                        "local_rate": 238.55,
                        "z": 0.020,
                        "radius_index": 9,
                        "r_max_index": 1,
                        "b_field_index": 0, 
                        "comp":  self.composition_values["RSG"],
                        "comp_checked": True,
                        "include": True,  
                    },

                    "comp_type": "RSG"

                },
                "syst":{
                    "Auger":{
                        "E": -42.0,
                        "Xmean": 300,
                        "SigmaXmean": 0.0
                    },
                    "TA":{
                        "E": 0.0,
                        "Xmean": 0.0,
                        "SigmaXmean": 0.0
                    }
                },
                "airshower": "EPOS-LHC",
                "cr":{
                        "Auger": True,
                        "TA": False,
                },
            },
            "WR star":{
                "dsg":{
                    "parameters":{
                        "local_rate": 130.92,
                        "z": 0.020,
                        "radius_index": 4,
                        "r_max_index": 2,
                        "b_field_index": 0, 
                        "comp":  self.composition_values["WR"],
                        "comp_checked": True,
                        "include": True,  
                    },

                    "comp_type": "WR"

                },
                "fdr":{
                    "parameters":{
                        "local_rate": 130.92,
                        "z": 0.020,
                        "radius_index": 12,
                        "r_max_index": 9,
                        "b_field_index": 0, 
                        "comp": self.composition_values["WR"],
                        "comp_checked": True,
                        "include": True,  
                    },

                    "comp_type": "WR"

                },
                "aalc":{
                    "parameters":{
                        "local_rate": 130.92,
                        "z": 0.020,
                        "radius_index": 4,
                        "r_max_index": 2,
                        "b_field_index": 0, 
                        "comp":  self.composition_values["WR"],
                        "comp_checked": True,
                        "include": True,  
                    },

                    "comp_type": "WR"

                },
                "syst":{
                    "Auger":{
                        "E": 19.4,
                        "Xmean": 181,
                        "SigmaXmean": 0.0
                    },
                    "TA":{
                        "E": 0.0,
                        "Xmean": 0.0,
                        "SigmaXmean": 0.0
                    }
                },
                "airshower": "EPOS-LHC",
                "cr":{
                        "Auger": True,
                        "TA": False,
                }
            },
            "CO-WD":{
                "dsg":{
                    "parameters":{
                        "local_rate": 63.76,
                        "z": 0.020,
                        "radius_index": 9,
                        "r_max_index": 5,
                        "b_field_index": 0, 
                        "comp":  self.composition_values["CO-WD"],
                        "comp_checked": True,
                        "include": True,  
                    },

                    "comp_type": "CO-WD"

                },
                "fdr":{
                    "parameters":{
                        "local_rate": 63.76,
                        "z": 0.020,
                        "radius_index": 12,
                        "r_max_index": 9,
                        "b_field_index": 0, 
                        "comp": self.composition_values["CO-WD"],
                        "comp_checked": True,
                        "include": True,  
                    },

                    "comp_type": "CO-WD"

                },
                "aalc":{
                    "parameters":{
                        "local_rate": 63.76,
                        "z": 0.020,
                        "radius_index": 8,
                        "r_max_index": 2,
                        "b_field_index": 0, 
                        "comp":  self.composition_values["CO-WD"],
                        "comp_checked": True,
                        "include": True,  
                    },

                    "comp_type": "CO-WD"

                },
                "syst":{
                    "Auger":{
                        "E": -42.0,
                        "Xmean": 300,
                        "SigmaXmean": 0.0
                    },
                    "TA":{
                        "E": 0.0,
                        "Xmean": 0.0,
                        "SigmaXmean": 0.0
                    }
                },
                "airshower": "EPOS-LHC",
                "cr":{
                        "Auger": True,
                        "TA": False,
                }
            }
        }
        list(self.parameters_best_fit_scenario.keys())
        self.TDES_STYLES ={
            'dsg' : {
                'line_style' : ':',
                'marker': "^",
                'color' :(43/255,59/255,74/255),
            },
            'fdr' : {
                'line_style' : '--',
                'marker': "D",
                'color' : (147/255,4/255,22/255),
            },
            'aalc' : {
                'line_style' : '-.',
                'marker': "s",
                'color' : (234/255,182/255,77/255),
            }
            
        }
        plt.rcParams['xtick.major.size'] = 10
        plt.rcParams['xtick.minor.size'] = 4
        plt.rcParams['ytick.major.size'] = 10
        plt.rcParams['ytick.minor.size'] = 4
        plt.rcParams['xtick.labelsize'] = 18
        plt.rcParams['ytick.labelsize'] = 18
        plt.rcParams['axes.labelsize'] = 18
        plt.rcParams.update({'font.size': 16})

        self.plot_data_sets={
            "cr":{
                "Auger": True,
                "TA": False,
            },
            "nu":{
                "HESE": True,
                "ICGen2": True,
                "IC9yr": True,
                "Auger2019": True,
                "RNO-G": True,
                "GRAND200K": True
            }
        }



        self.cr_syst={
            "Auger":{
                "E": 0.0,
                "Xmean": 0.0,
                "SigmaXmean": 0.0
            },
            "TA":{
                "E": 0.0,
                "Xmean": 0.0,
                "SigmaXmean": 0.0
            }
        }


        self.filepath ='./collected_results.hdf5'

        self.input_spec = [ 101, 402, 1206, 1407, 1608, 2311, 2814, 5626]
        self.paramlist_fit = (('radius_dsg', np.array([5.00e+16, 7.34e+16, 1.08e+17, 1.58e+17, 2.32e+17, 3.41e+17,
                                5.00e+17, 7.34e+17, 1.08e+18, 1.58e+18, 2.32e+18, 3.41e+18,
                                5.00e+18])), ('rigidity_dsg', np.array([1.00e+09, 1.39e+09, 1.92e+09, 2.66e+09, 3.68e+09, 5.10e+09,
                                7.07e+09, 9.80e+09, 1.36e+10, 1.88e+10, 2.61e+10, 3.61e+10,
                                5.00e+10])), ('B_value_dsg', np.array([0.1])), ('radius_fdr', np.array([5.00e+16, 7.34e+16, 1.08e+17, 1.58e+17, 2.32e+17, 3.41e+17,
                                5.00e+17, 7.34e+17, 1.08e+18, 1.58e+18, 2.32e+18, 3.41e+18,
                                5.00e+18])), ('rigidity_fdr', np.array([1.00e+09, 1.39e+09, 1.92e+09, 2.66e+09, 3.68e+09, 5.10e+09,
                                7.07e+09, 9.80e+09, 1.36e+10, 1.88e+10, 2.61e+10, 3.61e+10,
                                5.00e+10])), ('B_value_fdr', np.array([0.1])), ('radius_aalc', np.array([5.00e+16, 7.34e+16, 1.08e+17, 1.58e+17, 2.32e+17, 3.41e+17,
                                5.00e+17, 7.34e+17, 1.08e+18, 1.58e+18, 2.32e+18, 3.41e+18,
                                5.00e+18])), ('rigidity_aalc', np.array([1.00e+09, 1.39e+09, 1.92e+09, 2.66e+09, 3.68e+09, 5.10e+09,
                                7.07e+09, 9.80e+09, 1.36e+10, 1.88e+10, 2.61e+10, 3.61e+10,
                                5.00e+10])), ('B_value_aalc', np.array([0.1])))
        self.data_folder = "/afs/ifh.de/user/p/pavlop/homepavlo/TDE/data/TDEData_3TDENR2"
        self.data_set = "3TDENR2"
        self.escape_type = ('direct', 1)
        self.fit = "epos_dif_all_free"
        self.chi2_list = True

        self.A = np.array([1, 4, 12, 14, 16, 23, 28, 56])
        self.Z = np.array([1, 2,  6,  7,  8, 11, 14, 26])
        self.E_p_min = 1

        self.setup_scan()
        self.setup_ui()

    

    def setup_scan(self):
        def get_index(index):
            index_dsg = {'radius': index[0],'rigidity_max': index[1], 'B_value': index[2]} 
            index_fdr = {'radius': index[3],'rigidity_max': index[4], 'B_value': index[5]} 
            index_aalc = {'radius': index[6],'rigidity_max': index[7], 'B_value': index[8]}
            
            return index_dsg, index_fdr, index_aalc
        from prince_analysis_tools.plotter import ScanPlotterTDE
        self.scan  = ScanPlotterTDE(self.filepath, self.input_spec, self.paramlist_fit, 
                                                                        get_index, 
                                                                        data_folder = self.data_folder,
                                                                        data_set = self.data_set,
                                                                        escape_type = self.escape_type,
                                                                        fit=self.fit,
                                                                        chi2list=self.chi2_list)
        
    def create_best_fit(self):

        widget = widgets.ToggleButtons(
        options=['I want to play'] + list(self.parameters_best_fit_scenario.keys()),
        description='wchich scanraio you want to plot?:',
        disabled=False,
        button_style='', # 'success', 'info', 'warning', 'danger' or ''
        # tooltips=['Description of slow', 'Description of regular', 'Description of fast'],
    #     icons=['check'] * 3
        )
        return widget

    def create_grid_param(self):
        grid_param = GridspecLayout(4, 2)
        grid_param[0, 0:1] = widgets.HTML(value="<h2>Parameters  </h2>")
        grid_param[1, 0] = widgets.Dropdown(options=self.radius.tolist(), description="Radius [cm]", layout={'width': 'max-content'})
        grid_param[2, 0] = widgets.Dropdown(options=self.rigidity_max.tolist(), description="R_max [1e9 GeV]", layout={'width': 'max-content'})
        grid_param[3, 0] = widgets.Dropdown(options=self.B_field.tolist(), description="B [G]", layout={'width': 'max-content'})
        grid_param[1, 1] = widgets.BoundedFloatText(value=50, min=0, max=1e6, step=0.1, description='local rate:', disabled=False, layout={'width': 'max-content'})
        grid_param[2, 1] = widgets.BoundedFloatText(value=0.020, min=0, max=5.0, step=0.001, description='radshift:', disabled=False, layout={'width': 'max-content'})
        return grid_param

    def create_grid_comp(self):
        grid_comp = GridspecLayout(5, 3)
        grid_comp[0, 0] = widgets.HTML(value="<h2> Composition  </h2>")
        grid_comp[0, 1] = widgets.HTML()
        grid_comp[1:4, 0] = widgets.RadioButtons(options=['MS', 'RSG', 'WR', 'CO-WD', 'ONeMg-WD', 'Free'], value='Free', description='Composition:', disabled=False)
        grid_comp[1, 1] = widgets.BoundedFloatText(value=12.5, min=1e-5, max=100, step=0.1, description='H %:', disabled=False, layout={'width': 'max-content'})
        grid_comp[2, 1] = widgets.BoundedFloatText(value=12.5, min=1e-5, max=100, step=0.1, description='He %:', disabled=False, layout={'width': 'max-content'})
        grid_comp[3, 1] = widgets.BoundedFloatText(value=12.5, min=1e-5, max=100, step=0.1, description='C %:', disabled=False, layout={'width': 'max-content'})
        grid_comp[4, 1] = widgets.BoundedFloatText(value=12.5, min=1e-5, max=100, step=0.1, description='N %:', disabled=False, layout={'width': 'max-content'})
        grid_comp[1, 2] = widgets.BoundedFloatText(value=12.5, min=1e-5, max=100, step=0.1, description='O %:', disabled=False, layout={'width': 'max-content'})
        grid_comp[2, 2] = widgets.BoundedFloatText(value=12.5, min=1e-5, max=100, step=0.1, description='Na %:', disabled=False, layout={'width': 'max-content'})
        grid_comp[3, 2] = widgets.BoundedFloatText(value=12.5, min=1e-5, max=100, step=0.1, description='Si %:', disabled=False, layout={'width': 'max-content'})
        grid_comp[4, 2] = widgets.BoundedFloatText(value=12.5, min=1e-5, max=100, step=0.1, description='Fe %:', disabled=True, layout={'width': 'max-content'})
        return grid_comp

    def create_grid_param_cr_data(self):
        grid_param_cr_data = GridspecLayout(3, 1)
        grid_param_cr_data[0, 0] = widgets.HTML(value="UHECR data")
        
        descriptions = ['Auger 2019', 'TA 2019']
        keys = ['Auger', 'TA']
        initial_values = [True, False]  # Initial values for each checkbox

        for i, (desc, key, val) in enumerate(zip(descriptions, keys, initial_values), start=1):
            checkbox = widgets.Checkbox(value=val, description=desc, disabled=False, indent=False)
            grid_param_cr_data[i, 0] = checkbox
            # Attach event handler
            checkbox.observe(lambda change, name=key: self.handle_cr_data_change(change, name), names='value')

        return grid_param_cr_data

    def create_grid_param_nu_sets(self):
        grid_param_nu_sets = GridspecLayout(7, 1)
        grid_param_nu_sets[0, 0] = widgets.HTML(value="Neutrino")
        descriptions = ['IceCube HESE', 'IceCube 9 years', 'IceCube-Gen2', 'RNO-G', 'GRAND200k', 'Auger 2019']
        keys = ['HESE', 'IC9yr', 'ICGen2', 'RNO-G', 'GRAND200K', 'Auger2019']

        for i, desc in enumerate(descriptions, start=1):
            checkbox = widgets.Checkbox(value=True, description=desc, disabled=False, indent=False)
            grid_param_nu_sets[i, 0] = checkbox
            # Attach event handler
            checkbox.observe(lambda change, name=keys[i-1]: self.handle_nu_sens_change(change, name), names='value')

        return grid_param_nu_sets

    def create_grid_param_air_shower_model(self):
        # grid_param_plot = GridspecLayout(3, 1)
        # grid_param_plot[1, 0] = self.create_grid_param_cr_data()
        # grid_param_plot[3, 0] = self.create_grid_param_nu_sets()
        return widgets.RadioButtons(options=self.air_shower_model_names, description='Air Shower model:', disabled=False)

    def create_grid_param_syst_cr(self):
        grid_param_plot = GridspecLayout(4, 2)
        grid_param_plot[0, 0:2] = widgets.HTML(value="Systematics")  # Adjusted for spanning two columns
        
        # Define BoundedFloatText widgets and attach handlers
        self.descriptions_syst = [
            'E_PAO [%]', '<X>_PAO[%]', 'σ<X> PAO[%]',
            'E_TA [%]', '<X>_TA[%]', 'σ<X> TA[%]'
        ]
        for i, desc in enumerate(self.descriptions_syst):
            row, col = divmod(i, 3)  # Calculate row, column for placement
            # print(row, col)
            widget = widgets.BoundedFloatText(
                value=0.0,
                min=-3*14 if 'E' in desc else -300,
                max=3*14 if 'E' in desc else 300,
                step=0.1 if 'E' in desc else 1,
                description=desc,
                disabled=False,
                layout={'width': 'max-content'}
            )
            grid_param_plot[col + 1, row] = widget
            widget.observe(lambda change, name=desc: self.handle_systematic_change(change, name), names='value')
        
        return grid_param_plot

    def handle_systematic_change(self, change, name):
        # Update the corresponding value in the dictionary
        if name == self.descriptions_syst[0]:
            self.cr_syst["Auger"]["E"] = change['new']
        elif name == self.descriptions_syst[1]:
            self.cr_syst["Auger"]["Xmean"] = change['new']
        elif name == self.descriptions_syst[2]:
            self.cr_syst["Auger"]["SigmaXmean"] = change['new']
        elif name == self.descriptions_syst[3]:
            self.cr_syst["TA"]["E"] = change['new']
        elif name == self.descriptions_syst[4]:
            self.cr_syst["TA"]["Xmean"] = change['new']
        elif name == self.descriptions_syst[5]:
            self.cr_syst["TA"]["SigmaXmean"] = change['new']
        # print(f"Updated {name} to {change['new']}")  # Optional: for debugging

    def create_grid_param_buttons(self):
        grid_param_buttons = GridspecLayout(1, 4)

        grid_param_buttons[0, 0] = widgets.Button(
            description='Create Plot',
            disabled=False,
            button_style='',  # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Create a new plot',
            icon='chart-line'  # FontAwesome icon names without the `fa-` prefix
        )

        grid_param_buttons[0, 1] = widgets.Button(
            description='Fit Data',
            disabled=False,
            button_style='',
            tooltip='Fit data to model',
            icon='chart-bar'
        )

        grid_param_buttons[0, 2] = widgets.Button(
            description='Save Plot',
            disabled=False,
            button_style='',
            tooltip='Save the current plot',
            icon='save'
        )

        grid_param_buttons[0, 3] = widgets.Button(
            description='Save Data',
            disabled=False,
            button_style='',
            tooltip='Save the current data',
            icon='database'
        )

        return grid_param_buttons



    def setup_ui(self):
        self.box_layout_column = Layout(display='flex',  flex_flow='column', align_items='stretch', border='solid', width='100%')
        self.box_layout_column_no_borber = Layout(display='flex', flex_flow='column', align_items='stretch', border='none', width='100%')
        self.box_layout_row = Layout(display='flex', justify_content="space-between", flex_flow='row', align_items='stretch', border='solid', width='100%')
        self.box_layout_row_no_border = Layout(display='flex', justify_content="space-between", flex_flow='row', align_items='stretch', border='none', width='100%')

        
        self.plotting_scanario = self.create_best_fit()
        self.plotting_scanario_title = Box(children=[widgets.HTML(value="<h1>Predefined options</h1>"), self.plotting_scanario], layout=self.box_layout_column_no_borber)

        
        self.include_dsg = widgets.Checkbox(value=True, description='include to the plot', disabled=False)
        self.grid_param_dsg = self.create_grid_param()
        self.grid_comp_dsg = self.create_grid_comp()
        
        self.include_fdr = widgets.Checkbox(value=True, description='include to the plot', disabled=False)
        self.grid_param_fdr = self.create_grid_param()
        self.grid_comp_fdr = self.create_grid_comp()

        self.include_aalc = widgets.Checkbox(value=True, description='include to the plot', disabled=False)
        self.grid_param_aalc = self.create_grid_param()
        self.grid_comp_aalc = self.create_grid_comp()

        self.plot_data_cr = self.create_grid_param_cr_data()
        self.plot_syst_cr = self.create_grid_param_syst_cr()
        self.plot_data_nu = self.create_grid_param_nu_sets()
        self.plot_air_shower_model = self.create_grid_param_air_shower_model()
        self.buttons = self.create_grid_param_buttons()

        self.plot_output = widgets.Output()

        self.box_dsg_title = Box(children=[widgets.HTML(value="<h1>AT2019dsg</h1>"), self.include_dsg], layout=self.box_layout_row_no_border)
        self.box_dsg_parameters = Box(children=[self.grid_param_dsg, self.grid_comp_dsg], layout=self.box_layout_row_no_border)
        self.box_dsg = Box(children=[self.box_dsg_title,self.box_dsg_parameters], layout=self.box_layout_column)

        self.box_fdr_title = Box(children=[widgets.HTML(value="<h1>AT2019fdr</h1>"), self.include_fdr], layout=self.box_layout_row_no_border)
        self.box_fdr_parameters = Box(children=[self.grid_param_fdr, self.grid_comp_fdr], layout=self.box_layout_row_no_border)
        self.box_fdr = Box(children=[self.box_fdr_title,self.box_fdr_parameters], layout=self.box_layout_column)




        self.box_aalc_title = Box(children=[widgets.HTML(value="<h1>AT2019aalc</h1>"), self.include_aalc], layout=self.box_layout_row_no_border)
        self.box_aalc_parameters = Box(children=[self.grid_param_aalc, self.grid_comp_aalc], layout=self.box_layout_row_no_border)
        self.box_aalc = Box(children=[self.box_aalc_title,self.box_aalc_parameters], layout=self.box_layout_column)


        self.box_TDEs = Box(children=[self.box_dsg, self.box_fdr,self.box_aalc], layout=self.box_layout_column)  # Add all boxes here

        self.box_plot_param = Box(children=[self.plot_data_cr, self.plot_syst_cr, self.plot_air_shower_model, self.plot_data_nu], layout=self.box_layout_row_no_border)

        self.box_ui= Box(children=[self.plotting_scanario_title,self.box_TDEs, self.box_plot_param, self.buttons, self.plot_output], layout=self.box_layout_column) 
        self.plot_data_simple
        self.attach_event_handlers()

    def handle_cr_data_change(self, change, name):
        # Update the 'cr' part of the plot_data_sets dictionary
        self.plot_data_sets["cr"][name] = change['new']
    
    def handle_nu_sens_change(self, change, name):
        self.plot_data_sets["nu"][name] = change['new']
        # print(f"{name} set to {change['new']}")  # Debug print to verify changes
    
    def update_fields_based_on_scenario(self, change):
        if change['new'] == 'I want to play':
            return  # Ignore or reset fields if needed
        
        scenario_name = change['new']
        scenario_details = self.parameters_best_fit_scenario[scenario_name]

        #update dsg 

        self.grid_param_dsg[1,0].value = self.radius[scenario_details["dsg"]["parameters"]["radius_index"]]
        self.grid_param_dsg[2,0].value = self.rigidity_max[scenario_details["dsg"]["parameters"]["r_max_index"]]
        self.grid_param_dsg[3,0].value = self.B_field[scenario_details["dsg"]["parameters"]["b_field_index"]]
        self.grid_param_dsg[1,1].value = scenario_details["dsg"]["parameters"]["local_rate"]
        self.grid_param_dsg[2,1].value = scenario_details["dsg"]["parameters"]["z"]
        
        self.grid_comp_dsg[1:4, 0].value = scenario_details["dsg"]["comp_type"]
        self.grid_comp_dsg[1, 1].value = scenario_details["dsg"]["parameters"]["comp"][0]*100
        self.grid_comp_dsg[2, 1].value = scenario_details["dsg"]["parameters"]["comp"][1]*100 
        self.grid_comp_dsg[3, 1].value = scenario_details["dsg"]["parameters"]["comp"][2]*100 
        self.grid_comp_dsg[4, 1].value = scenario_details["dsg"]["parameters"]["comp"][3]*100
        self.grid_comp_dsg[1, 2].value = scenario_details["dsg"]["parameters"]["comp"][4]*100 
        self.grid_comp_dsg[2, 2].value = scenario_details["dsg"]["parameters"]["comp"][5]*100 
        self.grid_comp_dsg[3, 2].value = scenario_details["dsg"]["parameters"]["comp"][6]*100

        self.include_dsg.value =   scenario_details["dsg"]["parameters"]["include"]
        self.dsg_parameters = scenario_details["dsg"]["parameters"] 


        #update fdr 

        self.grid_param_fdr[1,0].value = self.radius[scenario_details["fdr"]["parameters"]["radius_index"]]
        self.grid_param_fdr[2,0].value = self.rigidity_max[scenario_details["fdr"]["parameters"]["r_max_index"]]
        self.grid_param_fdr[3,0].value = self.B_field[scenario_details["fdr"]["parameters"]["b_field_index"]]
        self.grid_param_fdr[1,1].value = scenario_details["fdr"]["parameters"]["local_rate"]
        self.grid_param_fdr[2,1].value = scenario_details["fdr"]["parameters"]["z"]

        self.grid_comp_fdr[1:4, 0].value = scenario_details["fdr"]["comp_type"]
        self.grid_comp_fdr[1, 1].value = scenario_details["fdr"]["parameters"]["comp"][0]*100
        self.grid_comp_fdr[2, 1].value = scenario_details["fdr"]["parameters"]["comp"][1]*100 
        self.grid_comp_fdr[3, 1].value = scenario_details["fdr"]["parameters"]["comp"][2]*100 
        self.grid_comp_fdr[4, 1].value = scenario_details["fdr"]["parameters"]["comp"][3]*100
        self.grid_comp_fdr[1, 2].value = scenario_details["fdr"]["parameters"]["comp"][4]*100 
        self.grid_comp_fdr[2, 2].value = scenario_details["fdr"]["parameters"]["comp"][5]*100 
        self.grid_comp_fdr[3, 2].value = scenario_details["fdr"]["parameters"]["comp"][6]*100
        self.include_fdr.value =   scenario_details["fdr"]["parameters"]["include"]
        self.fdr_parameters = scenario_details["fdr"]["parameters"] 
        
        #update aalc 

        self.grid_param_aalc[1,0].value = self.radius[scenario_details["aalc"]["parameters"]["radius_index"]]
        self.grid_param_aalc[2,0].value = self.rigidity_max[scenario_details["aalc"]["parameters"]["r_max_index"]]
        self.grid_param_aalc[3,0].value = self.B_field[scenario_details["aalc"]["parameters"]["b_field_index"]]
        self.grid_param_aalc[1,1].value = scenario_details["aalc"]["parameters"]["local_rate"]
        self.grid_param_aalc[2,1].value = scenario_details["aalc"]["parameters"]["z"]

        self.grid_comp_aalc[1:4, 0].value = scenario_details["aalc"]["comp_type"]
        self.grid_comp_aalc[1, 1].value = scenario_details["aalc"]["parameters"]["comp"][0]*100
        self.grid_comp_aalc[2, 1].value = scenario_details["aalc"]["parameters"]["comp"][1]*100 
        self.grid_comp_aalc[3, 1].value = scenario_details["aalc"]["parameters"]["comp"][2]*100 
        self.grid_comp_aalc[4, 1].value = scenario_details["aalc"]["parameters"]["comp"][3]*100
        self.grid_comp_aalc[1, 2].value = scenario_details["aalc"]["parameters"]["comp"][4]*100 
        self.grid_comp_aalc[2, 2].value = scenario_details["aalc"]["parameters"]["comp"][5]*100 
        self.grid_comp_aalc[3, 2].value = scenario_details["aalc"]["parameters"]["comp"][6]*100
        self.include_aalc.value =   scenario_details["aalc"]["parameters"]["include"]
        self.aalc_parameters = scenario_details["aalc"]["parameters"] 

        # "parameters""radius_index""r_max_index""b_field_index""comp_checked""include"

        #update systematics

        self.plot_syst_cr[1,0].value = scenario_details["syst"]["Auger"]["E"]
        self.plot_syst_cr[2,0].value = scenario_details["syst"]["Auger"]["Xmean"]
        self.plot_syst_cr[3,0].value = scenario_details["syst"]["Auger"]["SigmaXmean"]

        self.plot_syst_cr[1,1].value = scenario_details["syst"]["TA"]["E"]
        self.plot_syst_cr[2,1].value = scenario_details["syst"]["TA"]["Xmean"]
        self.plot_syst_cr[3,1].value = scenario_details["syst"]["TA"]["SigmaXmean"]

        self.plot_data_simple()


    def handle_type_comp_dsg_change(self, change):
        new_value = change['new']
        disable_value = False if new_value == 'Free' else True

        if new_value in self.composition_values:
            self.dsg_parameters["comp"] = self.composition_values[new_value]
            self.dsg_parameters["comp_checked"] = True
            self.grid_comp_dsg[0, 1].value = ""
        else:  # 'Free' option
            self.handle_comp_dsg_change(None)


        self.grid_comp_dsg[1, 1].disabled = disable_value 
        self.grid_comp_dsg[2, 1].disabled = disable_value 
        self.grid_comp_dsg[3, 1].disabled = disable_value 
        self.grid_comp_dsg[4, 1].disabled = disable_value 
        self.grid_comp_dsg[1, 2].disabled = disable_value 
        self.grid_comp_dsg[2, 2].disabled = disable_value 
        self.grid_comp_dsg[3, 2].disabled = disable_value

    def handle_type_comp_fdr_change(self, change):
        new_value = change['new']
        disable_value = False if new_value == 'Free' else True

        if new_value in self.composition_values:
            self.fdr_parameters["comp"] = self.composition_values[new_value]
            self.fdr_parameters["comp_checked"] = True
            self.grid_comp_fdr[0, 1].value = ""
        else:  # 'Free' option
            self.handle_comp_fdr_change(None)

        # Update the disabled property of the relevant widgets
        self.grid_comp_fdr[1, 1].disabled = disable_value 
        self.grid_comp_fdr[2, 1].disabled = disable_value 
        self.grid_comp_fdr[3, 1].disabled = disable_value 
        self.grid_comp_fdr[4, 1].disabled = disable_value 
        self.grid_comp_fdr[1, 2].disabled = disable_value 
        self.grid_comp_fdr[2, 2].disabled = disable_value 
        self.grid_comp_fdr[3, 2].disabled = disable_value

    def handle_type_comp_aalc_change(self, change):
        new_value = change['new']
        disable_value = False if new_value == 'Free' else True

        if new_value in self.composition_values:
            self.aalc_parameters["comp"] = self.composition_values[new_value]
            self.aalc_parameters["comp_checked"] = True
            self.grid_comp_aalc[0, 1].value = ""
        else:  # 'Free' option
            self.handle_comp_aalc_change(None)


        # Update the disabled property of the relevant widgets
        self.grid_comp_aalc[1, 1].disabled = disable_value 
        self.grid_comp_aalc[2, 1].disabled = disable_value 
        self.grid_comp_aalc[3, 1].disabled = disable_value 
        self.grid_comp_aalc[4, 1].disabled = disable_value 
        self.grid_comp_aalc[1, 2].disabled = disable_value 
        self.grid_comp_aalc[2, 2].disabled = disable_value 
        self.grid_comp_aalc[3, 2].disabled = disable_value

    def handle_comp_dsg_change(self, change):
        total_comp = sum(self.grid_comp_dsg[i, j].value for i in [1, 2, 3, 4] for j in [1, 2]) - self.grid_comp_dsg[4, 2].value
        if total_comp > 100 +1e-4:
            # raise Exception("Error: total composition > 100")
            self.grid_comp_dsg[0, 1].value = self.error_comp_massage 
            self.dsg_parameters["comp_checked"] = False

        else:
            self.grid_comp_dsg[4, 2].value = 100 - total_comp 
            self.grid_comp_dsg[0, 1].value = ""
            self.dsg_parameters["comp_checked"] = True
            self.fdr_parameters["comp"] = np.array([self.grid_comp_aalc[i, j].value / 100 for i in [1, 2, 3, 4] for j in [1, 2]])


    def handle_comp_fdr_change(self, change):
        total_comp = sum(self.grid_comp_fdr[i, j].value for i in [1, 2, 3, 4] for j in [1, 2]) - self.grid_comp_fdr[4, 2].value
        if total_comp > 100 +1e-4:
            self.grid_comp_fdr[0, 1].value = self.error_comp_massage 
            self.fdr_parameters["comp_checked"] = False
        else:
            self.grid_comp_fdr[4, 2].value = 100 - total_comp
            self.grid_comp_fdr[0, 1].value = ""
            self.fdr_parameters["comp_checked"] = True
            self.fdr_parameters["comp"] = np.array([self.grid_comp_aalc[i, j].value / 100 for i in [1, 2, 3, 4] for j in [1, 2]])

    def handle_comp_aalc_change(self, change):
        total_comp = sum(self.grid_comp_aalc[i, j].value for i in [1, 2, 3, 4] for j in [1, 2]) - self.grid_comp_aalc[4, 2].value
        print(total_comp)
        if total_comp > 100 +1e-4:
            self.grid_comp_aalc[0, 1].value = self.error_comp_massage 
            self.aalc_parameters["comp_checked"] = False
        else:
            self.grid_comp_aalc[4, 2].value = 100 - total_comp
            self.grid_comp_aalc[0, 1].value = ""
            self.aalc_parameters["comp_checked"] = True
            self.aalc_parameters["comp"] = np.array([self.grid_comp_aalc[i, j].value / 100 for i in [1, 2, 3, 4] for j in [1, 2]])

    def handle_include_dsg_change(self, change):
        enable = change['new']
        # Set the disabled property of each widget in the DSG grids
        for i in range(1,3):
            for j in range(0,2):
                self.grid_param_dsg[i, j].disabled = not enable
        self.grid_param_dsg[3, 0].disabled = not enable
        for i in range(1,4):
            for j in range(1,3):
                self.grid_comp_dsg[i, j].disabled = not enable
        self.grid_comp_dsg[1:3, 0].disabled = not enable
        self.grid_comp_dsg[4, 1].disabled = not enable
        self.dsg_parameters["include"] = enable

    def handle_include_fdr_change(self, change):
        enable = change['new']
        # Set the disabled property of each widget in the DSG grids
        for i in range(1,3):
            for j in range(0,2):
                self.grid_param_fdr[i, j].disabled = not enable
        self.grid_param_fdr[3, 0].disabled = not enable
        for i in range(1,4):
            for j in range(1,3):
                self.grid_comp_fdr[i, j].disabled = not enable
        self.grid_comp_fdr[1:3, 0].disabled = not enable
        self.grid_comp_fdr[4, 1].disabled = not enable
        self.fdr_parameters["include"] = enable

    def handle_include_aalc_change(self, change):
        enable = change['new']
        # Set the disabled property of each widget in the DSG grids
        for i in range(1,3):
            for j in range(0,2):
                self.grid_param_aalc[i, j].disabled = not enable
        self.grid_param_aalc[3, 0].disabled = not enable
        for i in range(1,4):
            for j in range(1,3):
                self.grid_comp_aalc[i, j].disabled = not enable
        self.grid_comp_aalc[1:3, 0].disabled = not enable
        self.grid_comp_aalc[4, 1].disabled = not enable
        self.aalc_parameters["include"] = enable

    def handle_local_rate_dsg_change(self, change):
        self.dsg_parameters["local_rate"] = change['new']

    def handle_local_rate_fdr_change(self, change):
        self.fdr_parameters["local_rate"] = change['new']

    def handle_local_rate_aalc_change(self, change):
        self.aalc_parameters["local_rate"] = change['new']


    def handle_redshift_dsg_change(self, change):
        self.dsg_parameters["z"] = change['new']

    def handle_redshift_fdr_change(self, change):
        self.fdr_parameters["z"] = change['new']

    def handle_redshift_aalc_change(self, change):
        self.aalc_parameters["z"] = change['new']


    def handle_radius_dsg_change(self, change):
        self.dsg_parameters["radius_index"] =np.where(change['new'] == self.radius)[0][0]
        # self.radius_dsg_value = self.radius_values[self.dsg_parameters["radius_index"]]

    def handle_r_max_dsg_change(self, change):
        self.dsg_parameters["r_max_index"] = np.where(change['new'] == self.rigidity_max)[0][0]

    def handle_b_field_dsg_change(self, change):
        self.dsg_parameters["b_field_index"] =  np.where(change['new'] == self.B_field)[0][0]


    def handle_radius_fdr_change(self, change):
        self.fdr_parameters["radius_index"] = np.where(change['new'] == self.radius)[0][0]
        # self.radius_fdr_value = self.radius_values[self.fdr_parameters["radius_index"]]
    

    def handle_r_max_fdr_change(self, change):
        self.fdr_parameters["r_max_index"] = np.where(change['new'] == self.rigidity_max)[0][0]

    def handle_b_field_fdr_change(self, change):
        self.fdr_parameters["b_field_index"] = np.where(change['new'] == self.B_field)[0][0]


    def handle_radius_aalc_change(self, change):
        self.aalc_parameters["radius_index"]= np.where(change['new'] == self.radius)[0][0]
        # self.radius_aalc_value = self.radius_values[self.aalc_parameters["radius_index"]]

    def handle_r_max_aalc_change(self, change):
        self.aalc_parameters["r_max_index"] =  np.where(change['new'] == self.rigidity_max)[0][0]

    def handle_b_field_aalc_change(self, change):
        self.aalc_parameters["b_field_index"] = change['new']


    def on_plot_button_clicked(self, b):
        self.plot_data_simple()

    

    def change_xmax_model(self, filename="air_shower_models.pkl"):
        import pickle
        # Load the XmaxSimple class from the saved file
        with open(filename, "rb") as file:
            XmaxSimple = pickle.load(file)
    
        # Set the appropriate XmaxSimple model based on the air_shower_model name
        if self.air_shower_model['name'] == 'EPOS-LHC':
            self.air_shower_model['model'] = XmaxSimple(model=XmaxSimple.EPOS)
        elif self.air_shower_model['name'] == 'SIBYLL2.3c':
            self.air_shower_model['model'] = XmaxSimple(model=XmaxSimple.Sibyll23)
        elif self.air_shower_model['name'] == 'SIBYLL2.3d':
            self.air_shower_model['model'] = XmaxSimple(model=XmaxSimple.Sibyll23d)        
        elif self.air_shower_model['name'] == 'QGSJET-II04':
            self.air_shower_model['model'] = XmaxSimple(model=XmaxSimple.QGSJetII)
        else:
            print("ERROR: The name of the air shower model is incorrect.")

    def plot_cosmic_rays(self, result_comb, result_each_tde = None, ls='solid', labels_on=True, label_E=2e11, label_offset=1.0,label_alpha=0.2, plot_total_flux=True ):
        import matplotlib.pyplot as plt
        from prince_cr.util import get_AZN
        auger2019 = self.spectra_data['auger2019']
        TA2019 = self.spectra_data['TA2019']
        
        LabelSpectrum = np.power(10,(np.array([2.75,2.65,2.55,2.45,2.35])-label_offset)) # np.power(10,(np.array([2.95,2.70,2.60,2.45,2.35])))
        A = lambda x: get_AZN(x)[0]

        ax_plots = []

        params = {'alpha': 0.1, 'lw': 2.}
        if plot_total_flux == True:
            for group, color, label, loffset in zip([(A,1,1),(A,2,4),(A,5,14),(A,15,28),(A,29,56)],
                                        ['red','gray','green','orange','blue'],
                                        [r'$\mathrm{A} = 1$',r'$2 \leq \mathrm{A} \leq 4$',r'$5 \leq \mathrm{A} \leq 14$',
                                        r'$15 \leq \mathrm{A} \leq 28$','$29 \leq \mathrm{A} \leq 56$'],
                                        LabelSpectrum):
                energy, spectrum = result_comb.get_solution_group(group)
                l, = plt.loglog(energy, spectrum, c=color, ls=ls, **params)
                plt.annotate(label, (label_E, loffset),color=color, weight = 'bold', fontsize = 13,alpha=label_alpha,
                        horizontalalignment ='right', verticalalignment = 'top')
                ax_plots.append(l)

        if plot_total_flux == True:

            energy, spectrum = result_comb.get_solution_group('CR')
            l, = plt.loglog(energy, spectrum, c='saddlebrown', lw=3, ls=ls, label='Total')
            ax_plots.append(l)

        
        if result_each_tde != None: 
        
            for res_tde, color, linestyle,label,position,rotation, loffset in zip(result_each_tde,
                                                    [self.TDES_STYLES['dsg']['color'], self.TDES_STYLES['fdr']['color'], self.TDES_STYLES['aalc']['color']],
                                                    [':','--','-.'],
                                                    ["dsg", "fdr","aalc"],
                                                    [(8e8,6e2),(2e9,6e2), (2e10,6e2)],
                                                    [0,0,0],
                                                    [0,0,0]):
                # print("spectrum", spectrum)
                energy, spectrum = res_tde.get_solution_group('CR') 
                l, = plt.loglog(energy, spectrum, c=color, lw = 3., label =label, ls = linestyle)
                ax_plots.append(l)

                # plt.annotate(label, position, fontsize=13, 
                #          color=color,rotation=rotation)
        # deltaE/=100
        # print("deltaE inside", deltaE)

        if self.plot_data_sets["cr"]["Auger"]:
            # Plot IceCube-Gen2 data
            plt.errorbar(auger2019['energy']*(1+self.cr_syst["Auger"]["E"]/100), auger2019['spectrum']*(1+self.cr_syst["Auger"]["E"]/100)**2, # depends on data_poemma
                        yerr=(auger2019['lower_err']*(1+self.cr_syst["Auger"]["E"]/100)**2, auger2019['upper_err']*(1+self.cr_syst["Auger"]["E"]/100)**2),
                        fmt='o', color='black', label = 'Auger 2019')
            
        if self.plot_data_sets["cr"]["TA"]:
            plt.errorbar(TA2019['energy']*(1+self.cr_syst["TA"]["E"]/100), TA2019['spectrum']*(1+self.cr_syst["TA"]["E"]/100)**2,
                 yerr=(TA2019['lower_err']*(1+self.cr_syst["TA"]["E"]/100)**2, TA2019['upper_err']*(1+self.cr_syst["TA"]["E"]/100)**2),
                 fmt='s', color='tab:brown', label = 'TA 2019', markersize=6, elinewidth=3)

        plt.legend(ncol=3, loc='upper center')

        plt.xlim(1e9,3e11)
        plt.ylim(3e0,6e2)

        plt.ylabel('$E^3$ J [GeV$^{2}$ cm$^{-2}$ s$^{-1}$ sr$^{-1}$]')
        plt.xlabel('E [GeV]')
        return ax_plots

    def make_error_boxes(self, xdata, ydata, xerror, yerror, facecolor='r',
                        edgecolor='None', alpha=0.5):

        ax = plt.gca()
        from matplotlib.collections import PatchCollection
        from matplotlib.patches import Rectangle

        # Create list for all the error patches
        errorboxes = []

        # Loop over data points; create box from errors at each point
        for x, y, xe, ye in zip(xdata, ydata, xerror.T, yerror.T):
            rect = Rectangle((x - xe[0], y - ye[0]), xe.sum(), ye.sum())
            errorboxes.append(rect)

        # Create patch collection with specified colour/alpha
        pc = PatchCollection(errorboxes, facecolor=facecolor, alpha=alpha,
                            edgecolor=edgecolor)

        # Add collection to axes
        ax.add_collection(pc)



    def find_nearest(self, array, value):
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return idx

    def plot_xmax_mean(self, result, model, ls = "solid", lw=2, label=None, auger_label=True):
        egrid, average, variance = result.get_lnA([el for el in result.known_species if el >= 100])
        energy = egrid
        mean_lnA = average
        sigma_lnA = variance
        ax_plots =[]
        import matplotlib.pyplot as plt
        Xmax2019 = self.spectra_data['Xmax2019']
        XmaxTA2018 = self.spectra_data['XmaxTA2018']
        # plot the reference models
        for A, c, name in zip([1,4,14,56], ['red','gray','green','blue'],['H','He','N','Fe']):
            Xmax = model.get_mean_Xmax(np.log(A), energy)
            plt.semilogx(energy,Xmax, color = c)
            idx = self.find_nearest(energy,1e11)
            plt.annotate(name,(energy[idx+1],Xmax[idx]),color = c,annotation_clip=False)

        Xmax = model.get_mean_Xmax(mean_lnA, energy)
        l, = plt.semilogx(energy, Xmax, color = 'saddlebrown', ls =ls, lw=lw, label=label)
        ax_plots.append(l)

        if self.plot_data_sets["cr"]["Auger"]:
            xerr = np.array((Xmax2019['energy_Low'], Xmax2019['energy_Up']))
            yerr = np.array((Xmax2019['sys_Low'], Xmax2019['sys_Up']))
            self.make_error_boxes(Xmax2019['energy'], Xmax2019['val'], xerr, yerr, facecolor='gray')
            
            if self.cr_syst["Auger"]["Xmean"] > 0:
                xcorr = self.cr_syst["Auger"]["Xmean"] * Xmax2019['sys_Up']/100
            else:
                xcorr = self.cr_syst["Auger"]["Xmean"] * Xmax2019['sys_Low']/100

            plt.errorbar(Xmax2019['energy'], Xmax2019['val'] + xcorr,
                        xerr=(Xmax2019['energy_Low'], Xmax2019['energy_Up']),
                        yerr=(Xmax2019['stat'], Xmax2019['stat']),
                        fmt='o',markersize=6, label='Auger 2019' * auger_label, c='black')

        if self.plot_data_sets["cr"]["TA"]:

            xerrTA = np.array((XmaxTA2018['energy_Low'], XmaxTA2018['energy_Up']))
            yerrTA = np.array((XmaxTA2018['sys_Low'], XmaxTA2018['sys_Up']))
            self.make_error_boxes(XmaxTA2018['energy'], XmaxTA2018['val'], xerrTA, yerrTA, facecolor='tab:brown',alpha=0.15)
            
            
            if self.cr_syst["TA"]["Xmean"] > 0:
                xcorrTA = self.cr_syst["TA"]["Xmean"] * XmaxTA2018['sys_Up']/100
            else:
                xcorrTA = self.cr_syst["TA"]["Xmean"] * XmaxTA2018['sys_Low']/100

            plt.errorbar(XmaxTA2018['energy'], XmaxTA2018['val'] + xcorrTA,
                        xerr=(XmaxTA2018['energy_Low'], XmaxTA2018['energy_Up']),
                        yerr=(XmaxTA2018['stat'], XmaxTA2018['stat']),
                        fmt='s',markersize=6,elinewidth=3, c='tab:brown',alpha=0.7, label = "TA 2018")


        plt.xlim(1e9,1e11)
        plt.ylim(650,900)
        plt.xlabel('E  [GeV]')
        plt.ylabel(r'$\langle X_{max} \rangle$ [g cm$^{-2}$]')
        return ax_plots
        
    def plot_xmax_sigma(self, result, model, deltaE = 0.,xshift=0., ls = "solid", lw=2, label=None,auger_label=True):
        egrid, average, variance = result.get_lnA([el for el in result.known_species if el >= 100])
        energy = egrid
        mean_lnA = average
        var_lnA = variance
        ax_plots = []
        import matplotlib.pyplot as plt
        
        for A, c, name in zip([1,4,14,56], ['red','gray','green','blue'],['H','He','N','Fe']):
            sigmaXmax, sigmaXmax_part = np.sqrt(model.get_var_Xmax(np.log(A), 0., energy))
            plt.semilogx(energy,sigmaXmax, color = c)
            idx = self.find_nearest(energy,1e11)
            plt.annotate(name,(energy[idx+1],sigmaXmax[idx]),color = c,annotation_clip=False)

        sigmaXmax, sigmaXmax_part = np.sqrt(model.get_var_Xmax(mean_lnA, var_lnA, energy))
        l, = plt.semilogx(energy,sigmaXmax, color = 'saddlebrown', ls =ls, lw=lw, label=label)
        ax_plots.append(l)

        XRMS2019 = self.spectra_data['XRMS2019']
        XRMSTA2018 = self.spectra_data['XRMSTA2018']
        if self.plot_data_sets["cr"]["Auger"]:
            xerr = np.array((XRMS2019['energy_Low'], XRMS2019['energy_Up']))
            yerr = np.array((XRMS2019['sys_Low'], XRMS2019['sys_Up']))
            self.make_error_boxes(XRMS2019['energy'], XRMS2019['val'], xerr, yerr, facecolor='gray')
            
            if self.cr_syst["Auger"]["SigmaXmean"] > 0:
                xcorr = self.cr_syst["Auger"]["SigmaXmean"] * XRMS2019['sys_Up']/100
            else:
                xcorr = self.cr_syst["Auger"]["SigmaXmean"] * XRMS2019['sys_Low']/100
            
            plt.errorbar(XRMS2019['energy'], XRMS2019['val'] + xcorr,
                        xerr=(XRMS2019['energy_Low'], XRMS2019['energy_Up']),
                        yerr=(XRMS2019['stat'], XRMS2019['stat']),
                        fmt='o',markersize=6, label='Auger 2019'*auger_label, c='black')

        if self.plot_data_sets["cr"]["TA"]:
            xerrTA = np.array((XRMSTA2018['energy_Low'], XRMSTA2018['energy_Up']))
            yerrTA = np.array((XRMSTA2018['sys_Low'], XRMSTA2018['sys_Up']))
            self.make_error_boxes(XRMSTA2018['energy'], XRMSTA2018['val'], xerrTA, yerrTA, facecolor='tab:brown',alpha=0.15)
            
            
            if self.cr_syst["TA"]["SigmaXmean"] > 0:
                xcorrTA = self.cr_syst["TA"]["SigmaXmean"] * XRMSTA2018['sys_Up']/100
            else:
                xcorrTA = self.cr_syst["TA"]["SigmaXmean"] * XRMSTA2018['sys_Low']/100

            plt.errorbar(XRMSTA2018['energy'], XRMSTA2018['val'] + xcorrTA,
                        xerr=(XRMSTA2018['energy_Low'], XRMSTA2018['energy_Up']),
                        yerr=(XRMSTA2018['stat'], XRMSTA2018['stat']),
                        fmt='s',markersize=6,elinewidth=3, c='tab:brown',alpha=0.7, label = "TA 2019")
        
        plt.xlim(1e9,1e11)
        plt.ylim(10,70)
        plt.xlabel('E  [GeV]')
        plt.ylabel(r'$\sigma( X_{max})$ [g cm$^{-2}$]')
        return ax_plots
        
        

    def plot_neutrinos(self, result,result_each_tde=None,  source=True, cosmo=True, total=False, ls=None,color=None,label=None,loc=None,plot_data=True,lw=3.):
            
        ls_source = '--' if ls is None else ls 
        ls_cosmo = '-.' if ls is None else ls
        ls_total = '-' if ls is None else ls
        color_source = plt.rcParams['axes.prop_cycle'].by_key()['color'][0] if color is None else color
        color_cosmo = plt.rcParams['axes.prop_cycle'].by_key()['color'][1] if color is None else color
        color_total = 'saddlebrown' if color is None else color
        

        
        label_source = 'Source' if label is None else label 
        label_cosmo = 'Cosmogenic' if label is None else label
        label_total = 'Total' if label is None else label

        if label == 'no_label':
            label_source = label_cosmo = label_total = None

        if self.plot_data_sets["nu"]["HESE"]:
                # Plot HESE data
            HESE = self.spectra_data['HESE']
            
            uplims = HESE["upper_err"].value == 0
            xerr = (HESE['energy'].value * 0.3, HESE['energy'].value * 0.43)
            plt.errorbar(HESE['energy'].value, 
                        HESE['flux'].value, 
                        (HESE["lower_err"].value,HESE["upper_err"].value),
                        uplims=uplims,
                        xerr=xerr,
                        ls='none',color='k')
            plt.text(2e5, 7e-8, "HESE", color="k")
            
            
        if self.plot_data_sets["nu"]["IC9yr"]:
            # Plot IceCube 9 years data
            ic_9yr = self.spectra_data['ic_9yr']
            plt.loglog(ic_9yr['energy'], ic_9yr['limit'], color=sns.colors.xkcd_rgb['blue'], lw=1.7)
            plt.text(8e6, 
                    3e-8,
                    "IC 9 year",
                    color=sns.xkcd_rgb["blue"])
            
        if self.plot_data_sets["nu"]["ICGen2"]:
            # Plot IceCube-Gen2 data
            gen2 = self.spectra_data['gen2']
            plt.loglog(gen2['energy'], gen2['limit'], color='k', lw=0.9)
            plt.text(2.7e7,
                    gen2['limit'][int(gen2['limit'].size /15)]* .55, 
                    "IC Gen2",
                    color="k")

            
        if self.plot_data_sets["nu"]["RNO-G"]:
            gen2 = self.spectra_data['rno_g_2020']
            plt.loglog(rno_g_2020['energy'], rno_g_2020['limit']/2, color='tab:olive', lw=0.9)
            plt.text(3.5e8, 
                    1e-8, 
                    "RNO-G", 
                    color="tab:olive")

                # Plot RNO-G data
            
        if self.plot_data_sets["nu"]["GRAND200K"]:
            # Plot GRAND200k data
            GRAND200K_new = self.spectra_data['GRAND200K_new']
            plt.loglog(GRAND200K_new['energy'], GRAND200K_new['limit'], color='r' , lw=0.9)
            plt.text(1.6e9, 
                    2.0e-9, 
                    "GRAND\n200k", 
                    color="r")

            
        if self.plot_data_sets["nu"]["Auger2019"]:
                # Plot Auger nu 2019 data
            PAO_nu_2019 = self.spectra_data['PAO_nu_2019']
            plt.loglog(PAO_nu_2019['energy'], PAO_nu_2019['limit'], color='magenta', lw=0.9)
            plt.text(PAO_nu_2019['energy'][0] * 2, 
                    PAO_nu_2019['limit'][0] * .5, 
                    "Auger 2019",
                    color='magenta')
            


        cosmo_range = [11, 12, 13, 14]
        source_range = [16]
        # for i in range(11,16):
        #     print(i, np.max(result.get_solution_group([i])[1]))
        source_nus = result.get_solution_group(source_range)
        cosmo_nus = result.get_solution_group(cosmo_range)
        ax_plots =[]
        if source:
            l, =plt.loglog(source_nus[0], source_nus[1] / source_nus[0], label=label_source, lw=2, ls = ls_source,
                    color=color_source, alpha = 0.3)
            ax_plots.append(l)

        if cosmo:
            l, =plt.loglog(cosmo_nus[0], cosmo_nus[1] / cosmo_nus[0], label=label_cosmo, lw =2, ls = ls_cosmo,
                    color=color_cosmo, alpha=0.3)
            ax_plots.append(l)

        if total:
            l, = plt.loglog(cosmo_nus[0], cosmo_nus[1]/cosmo_nus[0] + source_nus[1]/source_nus[0], lw =3, ls = ls_total,
                    color=color_total, label=label_total)
            ax_plots.append(l)
        
        if loc is None:
            loc = "lower right"
            
            
        if result_each_tde != None: 
        
            for res_tde, color, linestyle,label,position,rotation, loffset in zip(result_each_tde,
                                                    [self.TDES_STYLES['dsg']['color'], self.TDES_STYLES['fdr']['color'], self.TDES_STYLES['aalc']['color']],
                                                    [':','--','-.'],
                                                    ["dsg", "fdr","aalc"],
                                                    [(8e8,6e2),(2e9,6e2), (2e10,6e2)],
                                                    [0,0,0],
                                                    [0,0,0]):
                source_nus = res_tde.get_solution_group(source_range)
                cosmo_nus  = res_tde.get_solution_group(cosmo_range)
                
                    
                plt.loglog(cosmo_nus[0], cosmo_nus[1]/cosmo_nus[0] + source_nus[1]/source_nus[0], lw =3, ls = linestyle,
                    color=color, label=label)
                
                
            

        plt.legend(ncol=3,loc="upper center", frameon=1)
        plt.axis([2e4,2e10, 1e-11, 9e-7])
        plt.ylabel('$E^2 dN/dE$ [GeV cm$^{-2}$ s$^{-1}$ sr$^{-1}$]')
        plt.xlabel('E [GeV]')
        return ax_plots


    def get_results_from_states(self, plot_index):
        from prince_cr.solvers import UHECRPropagationResult
        
        # Load the shared egrid and known_spec from the new files
        egrid = np.load("data_TDE/egrid.npy")
        known_spec = np.load("data_TDE/known_spec.npy")
        input_spec = self.input_spec
        # Define labels to locate the state files based on index parameters
        label_dsg = f"{plot_index[0]}_{plot_index[1]}_{plot_index[2]}_"
        label_fdr = f"{plot_index[3]}_{plot_index[4]}_{plot_index[5]}_"
        label_aalc = f"{plot_index[6]}_{plot_index[7]}_{plot_index[8]}_"
        
        # Load the state data for DSG, FDR, and AALC based on the labels
        data_dsg = [np.load(f"data_TDE/state_dsg_{label_dsg}{m}.npy") for m in range(len(input_spec))]
        data_fdr = [np.load(f"data_TDE/state_fdr_{label_fdr}{m}.npy") for m in range(len(input_spec))]
        data_aalc = [np.load(f"data_TDE/state_aalc_{label_aalc}{m}.npy") for m in range(len(input_spec))]
        
        # Prepare dictionaries for each model containing egrid, known_spec, and state information
        dicts_dsg = [{'egrid': egrid, 'known_spec': known_spec, 'state': state} for state in data_dsg]
        dicts_fdr = [{'egrid': egrid, 'known_spec': known_spec, 'state': state} for state in data_fdr]
        dicts_aalc = [{'egrid': egrid, 'known_spec': known_spec, 'state': state} for state in data_aalc]
        
        # Convert each dictionary to a UHECRPropagationResult
        results_dsg = [UHECRPropagationResult.from_dict(d) for d in dicts_dsg]
        results_fdr = [UHECRPropagationResult.from_dict(d) for d in dicts_fdr]
        results_aalc = [UHECRPropagationResult.from_dict(d) for d in dicts_aalc]
        
        return results_dsg, results_fdr, results_aalc
    

    def get_comb_result(self, plot_index, frac_lr):
        results_dsg, results_fdr, results_aalc = self.get_each_type_result(plot_index, frac_lr)
       
        return results_dsg + results_fdr + results_aalc
    
    def get_each_type_result(self, plot_index, frac_lr):
        results_dsg, results_fdr, results_aalc = self.get_results_from_states(plot_index)
       
        fraction_dsg = np.array(frac_lr['frac_dsg'])
        fraction_fdr = np.array(frac_lr['frac_fdr'])
        fraction_aalc = np.array(frac_lr['frac_aalc'])
        
        lr_dsg = frac_lr['lr_dsg']
        lr_fdr = frac_lr['lr_fdr']
        lr_aalc = frac_lr['lr_aalc']
        
        results_dsg = np.sum(results_dsg * fraction_dsg) *lr_dsg  
        results_fdr = np.sum(results_fdr * fraction_fdr) *lr_fdr 
        results_aalc = np.sum(results_aalc * fraction_aalc) *lr_aalc    

        return results_dsg, results_fdr, results_aalc
    
            
    def get_scan_comb_result(self):
        import astropy.units as u
        self.plot_index = (self.dsg_parameters["radius_index"],self.dsg_parameters["r_max_index"],self.dsg_parameters["b_field_index"],
                 self.fdr_parameters["radius_index"],self.fdr_parameters["r_max_index"],self.fdr_parameters["b_field_index"],
                 self.aalc_parameters["radius_index"],self.aalc_parameters["r_max_index"],self.aalc_parameters["b_field_index"],)
        
        A = self.A
        Z = self.Z
        r_Max_dsg =  self.rigidity_max[self.dsg_parameters["r_max_index"]]
        r_Max_fdr =  self.rigidity_max[self.fdr_parameters["r_max_index"]]
        r_Max_aalc =  self.rigidity_max[self.aalc_parameters["r_max_index"]]
        
        E_p_min = (self.E_p_min* u.GeV).to_value(u.erg)
        E_dsg_p_max = (r_Max_dsg *1e9* u.GeV).to_value(u.erg)
        E_fdr_p_max = (r_Max_fdr *1e9* u.GeV).to_value(u.erg)
        E_aalc_p_max = (r_Max_aalc *1e9* u.GeV).to_value(u.erg)
        print(A,Z,E_p_min,r_Max_dsg,r_Max_fdr,r_Max_aalc)
        
        print()
        
        sum_frac_dsg = np.sum(self.dsg_parameters["comp"]* np.log(Z*E_dsg_p_max/(A*E_p_min)))
        lum_fraction_dsg = self.dsg_parameters["comp"] * np.log(Z*E_dsg_p_max/(A*E_p_min)) / sum_frac_dsg
        # print("DEBUG ", sum_frac_dsg, lum_fraction_dsg)
        
        sum_frac_fdr = np.sum(self.fdr_parameters["comp"]* np.log(Z*E_fdr_p_max/(A*E_p_min)))
        lum_fraction_fdr = self.fdr_parameters["comp"] * np.log(Z*E_fdr_p_max/(A*E_p_min)) / sum_frac_fdr
        
        sum_frac_aalc = np.sum(self.aalc_parameters["comp"]* np.log(Z*E_aalc_p_max/(A*E_p_min)))
        lum_fraction_aalc = self.aalc_parameters["comp"] * np.log(Z*E_aalc_p_max/(A*E_p_min)) / sum_frac_aalc


        self.plot_frac_lr = {
            'frac_dsg': lum_fraction_dsg,
            'frac_fdr': lum_fraction_fdr,
            'frac_aalc': lum_fraction_aalc,
            'lr_dsg': self.dsg_parameters["local_rate"] if self.dsg_parameters["include"] == True else 1e-5 ,
            'lr_fdr': self.fdr_parameters["local_rate"] if self.fdr_parameters["include"] == True else 1e-5,
            'lr_aalc': self.aalc_parameters["local_rate"] if self.aalc_parameters["include"] == True else 1e-5,
            }

        
        self.plot_results_comb =  self.get_comb_result(self.plot_index, frac_lr = self.plot_frac_lr)
        self.plot_results_each =  self.get_each_type_result(self.plot_index, frac_lr = self.plot_frac_lr)
        

    
    def plot_data_simple(self, title="Test plot", label_E=2.8e11, label_offset=0.5, label_alpha=0.2, plot_total_flux=True ):
        # print("I'm in the plot_data_simple")
        with self.plot_output:
            self.plot_output.clear_output(wait=True)
            fig, axs = plt.subplots(2,2, figsize=(14,9.5), gridspec_kw={'height_ratios':(1,.63), 'hspace':.3, 'wspace':0.3})

            self.get_scan_comb_result()
            self.change_xmax_model()

            # deltaE, deltaXmax, _ = [0.0,0.0,0.0]
            # deltaE*=14
            # print("deltaE",deltaE)
            
            fig.sca(axs[0][0])
            self.axs_cr = self.plot_cosmic_rays(self.plot_results_comb, self.plot_results_each, label_E=label_E, label_offset=label_offset, label_alpha=label_alpha, plot_total_flux=plot_total_flux)
            plt.fill_between([1e9,6e9*(1+np.min([self.cr_syst["Auger"]["E"], self.cr_syst["TA"]["E"]])/100)],1e-1,1e3,color='gray', alpha = 0.4)

            # plt.legend(loc="upper left")

            fig.sca(axs[0][1])
            self.axs_nu = self.plot_neutrinos(self.plot_results_comb, self.plot_results_each, source=True, cosmo=True, total=plot_total_flux)
            
            fig.sca(axs[1][0])
            self.axs_xmax_mean = self.plot_xmax_mean(self.plot_results_comb, self.air_shower_model['model'], lw=2.5)
            plt.fill_between([1e8,6e9],1e-1,1e3,color='gray', alpha = 0.4)
            plt.legend(loc='upper right')


            fig.sca(axs[1][1])
            self.axs_xmax_sigma = self.plot_xmax_sigma(self.plot_results_comb, self.air_shower_model['model'], lw=2.5)
            plt.fill_between([1e8,6e9],1e-1,1e3,color='gray', alpha = 0.4)
            plt.legend(loc='upper right')

            plt.suptitle(title, color = 'gray', fontsize = 26, weight = 'semibold', y=0.99)

            plt.tight_layout(rect=(0,0,1,.95))
            plt.subplots_adjust(left= 0.08, right = 0.95, bottom=0.09, top=0.95)
            plt.show()                          



    def attach_event_handlers(self):
        self.grid_comp_dsg[1:3, 0].observe(self.handle_type_comp_dsg_change, names='value')
        self.grid_comp_fdr[1:3, 0].observe(self.handle_type_comp_fdr_change, names='value')
        self.grid_comp_aalc[1:3, 0].observe(self.handle_type_comp_aalc_change, names='value')
        
        self.include_dsg.observe(self.handle_include_dsg_change, names='value')
        self.include_fdr.observe(self.handle_include_fdr_change, names='value')
        self.include_aalc.observe(self.handle_include_aalc_change, names='value')

        self.plotting_scanario.observe(self.update_fields_based_on_scenario, names='value')


        self.grid_comp_dsg[1, 1].observe(self.handle_comp_dsg_change, names='value')
        self.grid_comp_dsg[2, 1].observe(self.handle_comp_dsg_change, names='value')
        self.grid_comp_dsg[3, 1].observe(self.handle_comp_dsg_change, names='value')
        self.grid_comp_dsg[4, 1].observe(self.handle_comp_dsg_change, names='value')
        self.grid_comp_dsg[1, 2].observe(self.handle_comp_dsg_change, names='value')
        self.grid_comp_dsg[2, 2].observe(self.handle_comp_dsg_change, names='value')
        self.grid_comp_dsg[3, 2].observe(self.handle_comp_dsg_change, names='value')

        # Observers for grid_comp_fdr
        self.grid_comp_fdr[1, 1].observe(self.handle_comp_fdr_change, names='value')
        self.grid_comp_fdr[2, 1].observe(self.handle_comp_fdr_change, names='value')
        self.grid_comp_fdr[3, 1].observe(self.handle_comp_fdr_change, names='value')
        self.grid_comp_fdr[4, 1].observe(self.handle_comp_fdr_change, names='value')
        self.grid_comp_fdr[1, 2].observe(self.handle_comp_fdr_change, names='value')
        self.grid_comp_fdr[2, 2].observe(self.handle_comp_fdr_change, names='value')
        self.grid_comp_fdr[3, 2].observe(self.handle_comp_fdr_change, names='value')

        # Observers for grid_comp_aalc
        self.grid_comp_aalc[1, 1].observe(self.handle_comp_aalc_change, names='value')
        self.grid_comp_aalc[2, 1].observe(self.handle_comp_aalc_change, names='value')
        self.grid_comp_aalc[3, 1].observe(self.handle_comp_aalc_change, names='value')
        self.grid_comp_aalc[4, 1].observe(self.handle_comp_aalc_change, names='value')
        self.grid_comp_aalc[1, 2].observe(self.handle_comp_aalc_change, names='value')
        self.grid_comp_aalc[2, 2].observe(self.handle_comp_aalc_change, names='value')
        self.grid_comp_aalc[3, 2].observe(self.handle_comp_aalc_change, names='value')

        self.grid_param_dsg[1, 1].observe(self.handle_local_rate_dsg_change, names='value')
        self.grid_param_fdr[1, 1].observe(self.handle_local_rate_fdr_change, names='value')
        self.grid_param_aalc[1, 1].observe(self.handle_local_rate_aalc_change, names='value')

        self.grid_param_dsg[2, 1].observe(self.handle_redshift_dsg_change, names='value')
        self.grid_param_fdr[2, 1].observe(self.handle_redshift_fdr_change, names='value')
        self.grid_param_aalc[2, 1].observe(self.handle_redshift_aalc_change, names='value')

        self.grid_param_dsg[1, 0].observe(self.handle_radius_dsg_change, names='value')
        self.grid_param_fdr[1, 0].observe(self.handle_radius_fdr_change, names='value')
        self.grid_param_aalc[1, 0].observe(self.handle_radius_aalc_change, names='value')

        self.grid_param_dsg[2, 0].observe(self.handle_r_max_dsg_change, names='value')
        self.grid_param_fdr[2, 0].observe(self.handle_r_max_fdr_change, names='value')
        self.grid_param_aalc[2, 0].observe(self.handle_r_max_aalc_change, names='value')


        self.grid_param_dsg[3, 0].observe(self.handle_b_field_dsg_change, names='value')
        self.grid_param_fdr[3, 0].observe(self.handle_b_field_fdr_change, names='value')
        self.grid_param_aalc[3, 0].observe(self.handle_b_field_aalc_change, names='value')

        self.buttons[0,0].on_click(self.on_plot_button_clicked)



    def display(self):
        return display(self.box_ui)
