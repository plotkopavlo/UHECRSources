"""Interactive UHECR + neutrino model explorer for three tidal disruption events.

The tool overlays precomputed PriNCe cosmic-ray propagation results for
AT2019dsg, AT2019fdr and AT2019aalc on top of the measured cosmic-ray spectrum,
<Xmax>, sigma(Xmax) and neutrino fluxes (Auger / TA / IceCube / RNO-G / GRAND).

It is designed to run in JupyterLite (Pyodide). The heavy propagation is done
offline; here we only load the `state_*.npy` grids, weight them by the chosen
source composition and local rate, and plot the result against data.

Usage (inside the notebook)::

    ui = TDEsUI()
    ui.display()
"""

import pickle

import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as widgets
from ipywidgets import GridspecLayout, VBox, HBox, HTML
from IPython.display import display

# --------------------------------------------------------------------------- #
# Physics constants / static configuration                                    #
# --------------------------------------------------------------------------- #

# The three modelled tidal disruption events.
SCENARIOS = ("dsg", "fdr", "aalc")
SCENARIO_LABELS = {"dsg": "AT2019dsg", "fdr": "AT2019fdr", "aalc": "AT2019aalc"}

# Injected nuclei. ELEMENTS, A_NUCLEI, Z_NUCLEI and INPUT_SPEC are all in the
# SAME order; every composition array follows this order too.
ELEMENTS = ("H", "He", "C", "N", "O", "Na", "Si", "Fe")
A_NUCLEI = np.array([1, 4, 12, 14, 16, 23, 28, 56])
Z_NUCLEI = np.array([1, 2, 6, 7, 8, 11, 14, 26])
INPUT_SPEC = [101, 402, 1206, 1407, 1608, 2311, 2814, 5626]

# Source-parameter grids (index into the precomputed states).
RADIUS = np.array([5.00e16, 7.34e16, 1.08e17, 1.58e17, 2.32e17, 3.41e17,
                   5.00e17, 7.34e17, 1.08e18, 1.58e18, 2.32e18, 3.41e18, 5.00e18])
RIGIDITY_MAX = np.array([1.00e9, 1.39e9, 1.92e9, 2.66e9, 3.68e9, 5.10e9,
                         7.07e9, 9.80e9, 1.36e10, 1.88e10, 2.61e10, 3.61e10, 5.00e10]) / 1e9
B_FIELD = np.array([0.1])

# Stellar-abundance presets (fractions per element, summing to ~1).
COMPOSITIONS = {
    "MS":       np.array([73.9, 24.7, 0.22, 0.07, 0.63, 0.23, 0.07, 0.12]) / 100,
    "RSG":      np.array([46.46, 36.74, 0.95, 0.30, 2.72, 0.99, 0.3, 0.52]) / 100,
    "WR":       np.array([0.00633, 98.1, 0.0292, 1.33, 0.0321, 0.2573, 0.0734, 0.136]) / 100,
    "CO-WD":    np.array([1e-5, 1e-5, 50, 1e-5, 50, 1e-5, 1e-5, 1e-5]) / 100,
    "ONeMg-WD": np.array([1e-5, 1e-5, 1e-5, 1e-5, 12, 88, 1e-5, 1e-5]) / 100,
}
COMP_TYPES = ["MS", "RSG", "WR", "CO-WD", "ONeMg-WD", "Free"]

AIR_SHOWER_MODELS = ["EPOS-LHC", "SIBYLL2.3d", "SIBYLL2.3c", "QGSJET-II04"]

# Per-event plotting style (colour shared between UI cards and curves).
TDE_STYLES = {
    "dsg":  {"ls": ":",  "marker": "^", "color": (43 / 255, 59 / 255, 74 / 255)},
    "fdr":  {"ls": "--", "marker": "D", "color": (147 / 255, 4 / 255, 22 / 255)},
    "aalc": {"ls": "-.", "marker": "s", "color": (234 / 255, 182 / 255, 77 / 255)},
}

# Best-fit presets. Per event: (comp_type, local_rate, radius_index, r_max_index).
# `syst` holds the Auger (E, <Xmax>, sigma) systematic shifts in percent.
PRESETS = {
    "Star Mass Abundance": {
        "dsg":  ("ONeMg-WD", 32.45, 4, 4),
        "fdr":  ("WR",        5.23, 3, 10),
        "aalc": ("ONeMg-WD", 32.45, 4, 4),
        "syst": (-8.3, -148, 0.0),
    },
    "MS star": {
        "dsg":  ("MS", 220.24, 10, 3),
        "fdr":  ("MS", 220.24, 12, 8),
        "aalc": ("MS", 220.24, 10, 3),
        "syst": (-42.0, 300, 0.0),
    },
    "RSG star": {
        "dsg":  ("RSG", 238.55, 9, 1),
        "fdr":  ("RSG", 238.55, 12, 8),
        "aalc": ("RSG", 238.55, 9, 1),
        "syst": (-42.0, 300, 0.0),
    },
    "WR star": {
        "dsg":  ("WR", 130.92, 4, 2),
        "fdr":  ("WR", 130.92, 12, 9),
        "aalc": ("WR", 130.92, 4, 2),
        "syst": (19.4, 181, 0.0),
    },
    "CO-WD": {
        "dsg":  ("CO-WD", 63.76, 9, 5),
        "fdr":  ("CO-WD", 63.76, 12, 9),
        "aalc": ("CO-WD", 63.76, 8, 2),
        "syst": (-42.0, 300, 0.0),
    },
}

ERROR_MSG = '<span style="color:#c0392b;font-weight:600;">Composition exceeds 100%</span>'

# Injected into the page once so the widgets look like cards rather than a stack
# of bordered boxes.
_CSS = """
<style>
.tde-app { max-width: 1180px; font-family: -apple-system, "Segoe UI", Roboto, sans-serif; }
.tde-header { background: linear-gradient(135deg,#2b3b4a 0%,#3d5a73 100%);
    color:#fff; padding:18px 22px; border-radius:14px; margin-bottom:6px; }
.tde-header h1 { margin:0; font-size:22px; font-weight:650; }
.tde-header p { margin:6px 0 0; font-size:13px; opacity:.85; line-height:1.5; }
.tde-card { border:1px solid #e6e8eb; border-radius:14px; padding:8px 16px 14px;
    margin:10px 0; background:#fff; box-shadow:0 1px 4px rgba(0,0,0,.06); }
.tde-card-dsg  { border-left:6px solid rgb(43,59,74); }
.tde-card-fdr  { border-left:6px solid rgb(147,4,22); }
.tde-card-aalc { border-left:6px solid rgb(234,182,77); }
.tde-card-title { font-size:16px; font-weight:600; color:#2b3b4a; }
.tde-section-title { font-size:13px; font-weight:700; letter-spacing:.04em;
    text-transform:uppercase; color:#7a8794; margin:2px 0 6px; }
.tde-app .widget-button { border-radius:9px; }
</style>
"""


# --------------------------------------------------------------------------- #
# One tidal disruption event: its parameters, widgets and event handlers.     #
# Collapsing the former dsg/fdr/aalc triplication into a single class makes    #
# whole classes of copy-paste bugs impossible.                                #
# --------------------------------------------------------------------------- #

class Scenario:
    def __init__(self, key):
        self.key = key
        self.label = SCENARIO_LABELS[key]
        self.style = TDE_STYLES[key]
        self.params = {
            "local_rate": 50.0,
            "z": 0.020,
            "radius_index": 0,
            "r_max_index": 0,
            "b_field_index": 0,
            "comp": np.full(8, 0.125),
            "comp_checked": True,
            "include": True,
        }
        self._updating = False  # guard against observer recursion
        self._build_widgets()
        self._wire()

    # ---- widget construction ------------------------------------------- #

    def _build_widgets(self):
        cell = {"width": "max-content"}

        self.w_include = widgets.Checkbox(value=True, description="include in plot")

        self.w_radius = widgets.Dropdown(options=RADIUS.tolist(), value=RADIUS[0],
                                         description="Radius [cm]", layout=cell)
        self.w_rmax = widgets.Dropdown(options=RIGIDITY_MAX.tolist(), value=RIGIDITY_MAX[0],
                                       description="R_max [1e9 GV]", layout=cell)
        self.w_bfield = widgets.Dropdown(options=B_FIELD.tolist(), value=B_FIELD[0],
                                         description="B [G]", layout=cell)
        self.w_local_rate = widgets.BoundedFloatText(value=50, min=0, max=1e6, step=0.1,
                                                     description="local rate:", layout=cell)
        self.w_redshift = widgets.BoundedFloatText(value=0.020, min=0, max=5.0, step=0.001,
                                                   description="redshift:", layout=cell)

        param = GridspecLayout(3, 2)
        param[0, 0] = self.w_radius
        param[1, 0] = self.w_rmax
        param[2, 0] = self.w_bfield
        param[0, 1] = self.w_local_rate
        param[1, 1] = self.w_redshift
        self.param_grid = param

        self.w_comp_type = widgets.RadioButtons(options=COMP_TYPES, value="Free",
                                                description="Type:")
        self.w_msg = widgets.HTML()
        self.w_elem = {
            e: widgets.BoundedFloatText(value=12.5, min=1e-5, max=100, step=0.1,
                                        description=f"{e} %:",
                                        disabled=(e == "Fe"), layout=cell)
            for e in ELEMENTS
        }

        comp = GridspecLayout(4, 3)
        comp[0, 0] = self.w_comp_type
        comp[3, 0] = self.w_msg
        # Column-major fill so the on-screen grid matches the A/Z element order.
        for n, e in enumerate(ELEMENTS):
            comp[n % 4, 1 + n // 4] = self.w_elem[e]
        self.comp_grid = comp

    def card(self):
        """Return the styled widget card for this event."""
        title = HBox([HTML(f'<span class="tde-card-title">{self.label}</span>'),
                      self.w_include])
        body = HBox([self.param_grid, self.comp_grid])
        box = VBox([title, body])
        box.add_class("tde-card")
        box.add_class(f"tde-card-{self.key}")
        return box

    # ---- event wiring -------------------------------------------------- #

    def _wire(self):
        self.w_radius.observe(self._on_radius, names="value")
        self.w_rmax.observe(self._on_rmax, names="value")
        self.w_bfield.observe(self._on_bfield, names="value")
        self.w_local_rate.observe(self._on_local_rate, names="value")
        self.w_redshift.observe(self._on_redshift, names="value")
        self.w_comp_type.observe(self._on_comp_type, names="value")
        self.w_include.observe(self._on_include, names="value")
        for e in ELEMENTS:
            if e != "Fe":
                self.w_elem[e].observe(self._on_comp_value, names="value")

    def _on_radius(self, change):
        self.params["radius_index"] = int(np.where(RADIUS == change["new"])[0][0])

    def _on_rmax(self, change):
        self.params["r_max_index"] = int(np.where(RIGIDITY_MAX == change["new"])[0][0])

    def _on_bfield(self, change):
        self.params["b_field_index"] = int(np.where(B_FIELD == change["new"])[0][0])

    def _on_local_rate(self, change):
        self.params["local_rate"] = change["new"]

    def _on_redshift(self, change):
        self.params["z"] = change["new"]

    def _on_comp_type(self, change):
        new = change["new"]
        free = (new == "Free")
        if not free:
            self._updating = True
            for e, frac in zip(ELEMENTS, COMPOSITIONS[new]):
                self.w_elem[e].value = frac * 100
            self.params["comp"] = COMPOSITIONS[new].copy()
            self.params["comp_checked"] = True
            self.w_msg.value = ""
            self._updating = False
        else:
            self._on_comp_value()
        for e in ELEMENTS:
            if e != "Fe":
                self.w_elem[e].disabled = not free

    def _on_comp_value(self, change=None):
        """Recompute the free composition; Fe is the remainder up to 100%."""
        if self._updating:
            return
        editable = sum(self.w_elem[e].value for e in ELEMENTS if e != "Fe")
        if editable > 100 + 1e-4:
            self.w_msg.value = ERROR_MSG
            self.params["comp_checked"] = False
            return
        self.w_elem["Fe"].value = 100 - editable
        self.w_msg.value = ""
        self.params["comp_checked"] = True
        self.params["comp"] = np.array([self.w_elem[e].value for e in ELEMENTS]) / 100.0

    def _on_include(self, change):
        enabled = change["new"]
        self.params["include"] = enabled
        for w in (self.w_radius, self.w_rmax, self.w_bfield,
                  self.w_local_rate, self.w_redshift, self.w_comp_type):
            w.disabled = not enabled
        free = self.w_comp_type.value == "Free"
        for e in ELEMENTS:
            if e != "Fe":
                self.w_elem[e].disabled = (not enabled) or (not free)

    # ---- preset application (no observer side effects on comp) ---------- #

    def apply_preset(self, comp_type, local_rate, radius_index, r_max_index):
        self._updating = True
        self.w_radius.value = RADIUS[radius_index]
        self.w_rmax.value = RIGIDITY_MAX[r_max_index]
        self.w_bfield.value = B_FIELD[0]
        self.w_local_rate.value = local_rate
        self.w_redshift.value = 0.020
        self.w_comp_type.value = comp_type
        for e, frac in zip(ELEMENTS, COMPOSITIONS[comp_type]):
            self.w_elem[e].value = frac * 100
        self.w_include.value = True
        self._updating = False
        self.params.update({
            "local_rate": local_rate,
            "z": 0.020,
            "radius_index": radius_index,
            "r_max_index": r_max_index,
            "b_field_index": 0,
            "comp": COMPOSITIONS[comp_type].copy(),
            "comp_checked": True,
            "include": True,
        })


# --------------------------------------------------------------------------- #
# The full application: shared widgets, physics and plotting.                 #
# --------------------------------------------------------------------------- #

class TDEsUI:
    def __init__(self):
        with open("spectra_data.pkl", "rb") as fh:
            self.spectra_data = pickle.load(fh)

        self.air_shower_model = {"name": "EPOS-LHC", "model": None}
        self.cr_syst = {key: {"E": 0.0, "Xmean": 0.0, "SigmaXmean": 0.0}
                        for key in ("Auger", "TA")}
        self.plot_data_sets = {
            "cr": {"Auger": True, "TA": False},
            "nu": {"HESE": True, "ICGen2": True, "IC9yr": True,
                   "Auger2019": True, "RNO-G": True, "GRAND200K": True},
        }
        self.E_p_min = 1  # GeV

        self.scenarios = {k: Scenario(k) for k in SCENARIOS}

        self._apply_mpl_style()
        self._build_ui()

    # ---- styling ------------------------------------------------------- #

    @staticmethod
    def _apply_mpl_style():
        plt.rcParams.update({
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "axes.labelsize": 16,
            "axes.titlesize": 16,
            "xtick.labelsize": 14,
            "ytick.labelsize": 14,
            "xtick.major.size": 8,
            "xtick.minor.size": 4,
            "ytick.major.size": 8,
            "ytick.minor.size": 4,
            "font.size": 14,
            "legend.fontsize": 11,
            "legend.frameon": True,
            "axes.grid": False,
        })

    # ---- UI ------------------------------------------------------------ #

    def _build_ui(self):
        header = HTML(
            '<div class="tde-header">'
            '<h1>UHECR &amp; neutrino sources: tidal disruption events</h1>'
            '<p>Weight precomputed PriNCe propagation states for AT2019dsg, '
            'AT2019fdr and AT2019aalc by their source composition and local rate, '
            'and compare the cosmic-ray spectrum, &lt;X<sub>max</sub>&gt;, '
            '&sigma;(X<sub>max</sub>) and neutrino flux against Auger / TA / '
            'IceCube data.</p></div>'
        )

        self.preset_selector = widgets.ToggleButtons(
            options=["I want to play"] + list(PRESETS.keys()),
            description="Preset:",
        )
        preset_card = VBox([
            HTML('<span class="tde-section-title">Predefined best-fit options</span>'),
            self.preset_selector,
        ])
        preset_card.add_class("tde-card")

        cards = [s.card() for s in self.scenarios.values()]

        self.cr_checks = self._make_checks(
            [("Auger 2019", "Auger", True), ("TA 2019", "TA", False)],
            self._on_cr_data)
        self.nu_checks = self._make_checks(
            [("IceCube HESE", "HESE", True), ("IceCube 9 yr", "IC9yr", True),
             ("IceCube-Gen2", "ICGen2", True), ("RNO-G", "RNO-G", True),
             ("GRAND200k", "GRAND200K", True), ("Auger 2019", "Auger2019", True)],
            self._on_nu_data)
        self.airshower_radio = widgets.RadioButtons(
            options=AIR_SHOWER_MODELS, description="Air shower:")
        self.airshower_radio.observe(self._on_airshower, names="value")
        self.syst_grid = self._make_syst_grid()

        data_card = VBox([
            HTML('<span class="tde-section-title">Data sets, systematics &amp; '
                 'air-shower model</span>'),
            HBox([
                VBox([HTML("<b>UHECR data</b>")] + self.cr_checks),
                VBox([HTML("<b>Neutrino data</b>")] + self.nu_checks),
                VBox([HTML("<b>Air-shower model</b>"), self.airshower_radio]),
                VBox([HTML("<b>Systematics [%]</b>"), self.syst_grid]),
            ]),
        ])
        data_card.add_class("tde-card")

        self.plot_button = widgets.Button(description="Create plot", icon="chart-line",
                                          button_style="primary")
        self.plot_button.on_click(lambda _b: self.plot_data_simple())
        buttons = HBox([self.plot_button])

        self.plot_output = widgets.Output()

        self.preset_selector.observe(self._on_preset, names="value")

        self.box_ui = VBox([HTML(_CSS), header, preset_card, *cards,
                            data_card, buttons, self.plot_output])
        self.box_ui.add_class("tde-app")

    def _make_checks(self, items, handler):
        boxes = []
        for desc, key, val in items:
            cb = widgets.Checkbox(value=val, description=desc, indent=False)
            cb.observe(lambda ch, name=key: handler(name, ch["new"]), names="value")
            boxes.append(cb)
        return boxes

    def _make_syst_grid(self):
        # Auger column then TA column; rows = energy / <Xmax> / sigma(Xmax).
        self.syst_widgets = {}
        rows = [("E", "E"), ("Xmean", "<X>"), ("SigmaXmean", "σ<X>")]
        grid = GridspecLayout(3, 2)
        for col, det in enumerate(("Auger", "TA")):
            for row, (field, short) in enumerate(rows):
                is_energy = field == "E"
                w = widgets.BoundedFloatText(
                    value=0.0,
                    min=-42 if is_energy else -300, max=42 if is_energy else 300,
                    step=0.1 if is_energy else 1,
                    description=f"{short} {det}", layout={"width": "max-content"})
                w.observe(lambda ch, d=det, f=field: self._on_syst(d, f, ch["new"]),
                          names="value")
                self.syst_widgets[(det, field)] = w
                grid[row, col] = w
        return grid

    # ---- shared handlers ----------------------------------------------- #

    def _on_cr_data(self, name, value):
        self.plot_data_sets["cr"][name] = value

    def _on_nu_data(self, name, value):
        self.plot_data_sets["nu"][name] = value

    def _on_airshower(self, change):
        self.air_shower_model["name"] = change["new"]

    def _on_syst(self, detector, field, value):
        self.cr_syst[detector][field] = value

    def _on_preset(self, change):
        name = change["new"]
        if name == "I want to play":
            return
        preset = PRESETS[name]
        for key in SCENARIOS:
            self.scenarios[key].apply_preset(*preset[key])

        e, xmean, sigma = preset["syst"]
        self.syst_widgets[("Auger", "E")].value = e
        self.syst_widgets[("Auger", "Xmean")].value = xmean
        self.syst_widgets[("Auger", "SigmaXmean")].value = sigma
        for field in ("E", "Xmean", "SigmaXmean"):
            self.syst_widgets[("TA", field)].value = 0.0
        self.plot_data_simple()

    # ---- physics ------------------------------------------------------- #

    def get_results_from_states(self, plot_index):
        from prince_cr.solvers import UHECRPropagationResult

        egrid = np.load("data_TDE/egrid.npy")
        known_spec = np.load("data_TDE/known_spec.npy")
        n = len(INPUT_SPEC)

        results = {}
        for i, key in enumerate(SCENARIOS):
            label = f"{plot_index[3 * i]}_{plot_index[3 * i + 1]}_{plot_index[3 * i + 2]}_"
            states = [np.load(f"data_TDE/state_{key}_{label}{m}.npy") for m in range(n)]
            results[key] = [
                UHECRPropagationResult.from_dict(
                    {"egrid": egrid, "known_spec": known_spec, "state": s})
                for s in states
            ]
        return results

    def get_each_type_result(self, plot_index, frac_lr):
        states = self.get_results_from_states(plot_index)
        out = {}
        for key in SCENARIOS:
            fraction = np.asarray(frac_lr[f"frac_{key}"])
            combined = np.sum(np.asarray(states[key], dtype=object) * fraction)
            out[key] = combined * frac_lr[f"lr_{key}"]
        return out[SCENARIOS[0]], out[SCENARIOS[1]], out[SCENARIOS[2]]

    def get_comb_result(self, plot_index, frac_lr):
        r_dsg, r_fdr, r_aalc = self.get_each_type_result(plot_index, frac_lr)
        return r_dsg + r_fdr + r_aalc

    def get_scan_comb_result(self):
        import astropy.units as u

        p = {k: self.scenarios[k].params for k in SCENARIOS}
        self.plot_index = tuple(
            p[k][idx] for k in SCENARIOS
            for idx in ("radius_index", "r_max_index", "b_field_index"))

        e_p_min = (self.E_p_min * u.GeV).to_value(u.erg)
        frac_lr = {}
        for key in SCENARIOS:
            r_max = RIGIDITY_MAX[p[key]["r_max_index"]]
            e_p_max = (r_max * 1e9 * u.GeV).to_value(u.erg)
            weight = p[key]["comp"] * np.log(Z_NUCLEI * e_p_max / (A_NUCLEI * e_p_min))
            frac_lr[f"frac_{key}"] = weight / np.sum(weight)
            frac_lr[f"lr_{key}"] = p[key]["local_rate"] if p[key]["include"] else 1e-5
        self.plot_frac_lr = frac_lr

        self.plot_results_comb = self.get_comb_result(self.plot_index, frac_lr)
        self.plot_results_each = self.get_each_type_result(self.plot_index, frac_lr)

    def change_xmax_model(self, filename="air_shower_models.pkl"):
        with open(filename, "rb") as fh:
            XmaxSimple = pickle.load(fh)
        mapping = {
            "EPOS-LHC": "EPOS",
            "SIBYLL2.3c": "Sibyll23",
            "SIBYLL2.3d": "Sibyll23d",
            "QGSJET-II04": "QGSJetII",
        }
        name = self.air_shower_model["name"]
        if name not in mapping:
            raise ValueError(f"Unknown air-shower model: {name}")
        self.air_shower_model["model"] = XmaxSimple(model=getattr(XmaxSimple, mapping[name]))

    # ---- helpers ------------------------------------------------------- #

    @staticmethod
    def find_nearest(array, value):
        array = np.asarray(array)
        return int((np.abs(array - value)).argmin())

    @staticmethod
    def make_error_boxes(xdata, ydata, xerror, yerror, facecolor="r",
                         edgecolor="None", alpha=0.5):
        from matplotlib.collections import PatchCollection
        from matplotlib.patches import Rectangle

        ax = plt.gca()
        boxes = [Rectangle((x - xe[0], y - ye[0]), xe.sum(), ye.sum())
                 for x, y, xe, ye in zip(xdata, ydata, xerror.T, yerror.T)]
        ax.add_collection(PatchCollection(boxes, facecolor=facecolor, alpha=alpha,
                                          edgecolor=edgecolor))

    # ---- plots --------------------------------------------------------- #

    def plot_cosmic_rays(self, result_comb, result_each_tde=None, ls="solid",
                         label_E=2e11, label_offset=1.0, label_alpha=0.2,
                         plot_total_flux=True):
        from prince_cr.util import get_AZN

        auger2019 = self.spectra_data["auger2019"]
        TA2019 = self.spectra_data["TA2019"]
        label_spectrum = np.power(10, np.array([2.75, 2.65, 2.55, 2.45, 2.35]) - label_offset)
        A = lambda x: get_AZN(x)[0]
        ax_plots = []

        if plot_total_flux:
            groups = [(A, 1, 1), (A, 2, 4), (A, 5, 14), (A, 15, 28), (A, 29, 56)]
            colors = ["red", "gray", "green", "orange", "blue"]
            labels = [r"$\mathrm{A} = 1$", r"$2 \leq \mathrm{A} \leq 4$",
                      r"$5 \leq \mathrm{A} \leq 14$", r"$15 \leq \mathrm{A} \leq 28$",
                      r"$29 \leq \mathrm{A} \leq 56$"]
            for group, color, label, loffset in zip(groups, colors, labels, label_spectrum):
                energy, spectrum = result_comb.get_solution_group(group)
                line, = plt.loglog(energy, spectrum, c=color, ls=ls, alpha=0.1, lw=2.0)
                plt.annotate(label, (label_E, loffset), color=color, weight="bold",
                             fontsize=13, alpha=label_alpha,
                             horizontalalignment="right", verticalalignment="top")
                ax_plots.append(line)

            energy, spectrum = result_comb.get_solution_group("CR")
            line, = plt.loglog(energy, spectrum, c="saddlebrown", lw=3, ls=ls, label="Total")
            ax_plots.append(line)

        if result_each_tde is not None:
            for key, res_tde in zip(SCENARIOS, result_each_tde):
                energy, spectrum = res_tde.get_solution_group("CR")
                line, = plt.loglog(energy, spectrum, c=TDE_STYLES[key]["color"], lw=3,
                                   label=key, ls=TDE_STYLES[key]["ls"])
                ax_plots.append(line)

        if self.plot_data_sets["cr"]["Auger"]:
            shift = 1 + self.cr_syst["Auger"]["E"] / 100
            plt.errorbar(auger2019["energy"] * shift, auger2019["spectrum"] * shift ** 2,
                         yerr=(auger2019["lower_err"] * shift ** 2,
                               auger2019["upper_err"] * shift ** 2),
                         fmt="o", color="black", label="Auger 2019")
        if self.plot_data_sets["cr"]["TA"]:
            shift = 1 + self.cr_syst["TA"]["E"] / 100
            plt.errorbar(TA2019["energy"] * shift, TA2019["spectrum"] * shift ** 2,
                         yerr=(TA2019["lower_err"] * shift ** 2,
                               TA2019["upper_err"] * shift ** 2),
                         fmt="s", color="tab:brown", label="TA 2019",
                         markersize=6, elinewidth=3)

        plt.legend(ncol=3, loc="upper center")
        plt.xlim(1e9, 3e11)
        plt.ylim(3e0, 6e2)
        plt.ylabel(r"$E^3$ J [GeV$^{2}$ cm$^{-2}$ s$^{-1}$ sr$^{-1}$]")
        plt.xlabel("E [GeV]")
        return ax_plots

    def plot_xmax_mean(self, result, model, ls="solid", lw=2, label=None, auger_label=True):
        egrid, mean_lnA, _ = result.get_lnA([el for el in result.known_species if el >= 100])
        energy = egrid
        Xmax2019 = self.spectra_data["Xmax2019"]
        XmaxTA2018 = self.spectra_data["XmaxTA2018"]
        ax_plots = []

        for A, c, name in zip([1, 4, 14, 56], ["red", "gray", "green", "blue"],
                              ["H", "He", "N", "Fe"]):
            Xmax = model.get_mean_Xmax(np.log(A), energy)
            plt.semilogx(energy, Xmax, color=c)
            idx = self.find_nearest(energy, 1e11)
            plt.annotate(name, (energy[idx + 1], Xmax[idx]), color=c, annotation_clip=False)

        Xmax = model.get_mean_Xmax(mean_lnA, energy)
        line, = plt.semilogx(energy, Xmax, color="saddlebrown", ls=ls, lw=lw, label=label)
        ax_plots.append(line)

        if self.plot_data_sets["cr"]["Auger"]:
            self._xmax_data(Xmax2019, "Auger", "Xmean", "o", "black", "gray",
                            auger_label, "Auger 2019")
        if self.plot_data_sets["cr"]["TA"]:
            self._xmax_data(XmaxTA2018, "TA", "Xmean", "s", "tab:brown", "tab:brown",
                            auger_label, "TA 2018", box_alpha=0.15, alpha=0.7)

        plt.xlim(1e9, 1e11)
        plt.ylim(650, 900)
        plt.xlabel("E  [GeV]")
        plt.ylabel(r"$\langle X_{max} \rangle$ [g cm$^{-2}$]")
        return ax_plots

    def plot_xmax_sigma(self, result, model, ls="solid", lw=2, label=None, auger_label=True):
        egrid, mean_lnA, var_lnA = result.get_lnA(
            [el for el in result.known_species if el >= 100])
        energy = egrid
        XRMS2019 = self.spectra_data["XRMS2019"]
        XRMSTA2018 = self.spectra_data["XRMSTA2018"]
        ax_plots = []

        for A, c, name in zip([1, 4, 14, 56], ["red", "gray", "green", "blue"],
                              ["H", "He", "N", "Fe"]):
            sigmaXmax, _ = np.sqrt(model.get_var_Xmax(np.log(A), 0.0, energy))
            plt.semilogx(energy, sigmaXmax, color=c)
            idx = self.find_nearest(energy, 1e11)
            plt.annotate(name, (energy[idx + 1], sigmaXmax[idx]), color=c,
                         annotation_clip=False)

        sigmaXmax, _ = np.sqrt(model.get_var_Xmax(mean_lnA, var_lnA, energy))
        line, = plt.semilogx(energy, sigmaXmax, color="saddlebrown", ls=ls, lw=lw, label=label)
        ax_plots.append(line)

        if self.plot_data_sets["cr"]["Auger"]:
            self._xmax_data(XRMS2019, "Auger", "SigmaXmean", "o", "black", "gray",
                            auger_label, "Auger 2019")
        if self.plot_data_sets["cr"]["TA"]:
            self._xmax_data(XRMSTA2018, "TA", "SigmaXmean", "s", "tab:brown", "tab:brown",
                            auger_label, "TA 2018", box_alpha=0.15, alpha=0.7)

        plt.xlim(1e9, 1e11)
        plt.ylim(10, 70)
        plt.xlabel("E  [GeV]")
        plt.ylabel(r"$\sigma( X_{max})$ [g cm$^{-2}$]")
        return ax_plots

    def _xmax_data(self, data, detector, syst_field, fmt, color, box_color, auger_label,
                   label, box_alpha=0.5, alpha=1.0):
        """Shared Xmax / sigma(Xmax) data overlay (Auger or TA).

        `syst_field` selects which systematic shift applies: "Xmean" for the
        <Xmax> panel, "SigmaXmean" for the sigma(Xmax) panel.
        """
        xerr = np.array((data["energy_Low"], data["energy_Up"]))
        yerr = np.array((data["sys_Low"], data["sys_Up"]))
        self.make_error_boxes(data["energy"], data["val"], xerr, yerr,
                              facecolor=box_color, alpha=box_alpha)
        syst = self.cr_syst[detector][syst_field]
        shift = data["sys_Up"] if syst > 0 else data["sys_Low"]
        xcorr = syst * shift / 100
        plt.errorbar(data["energy"], data["val"] + xcorr,
                     xerr=(data["energy_Low"], data["energy_Up"]),
                     yerr=(data["stat"], data["stat"]),
                     fmt=fmt, markersize=6, c=color, alpha=alpha,
                     elinewidth=3 if detector == "TA" else None,
                     label=label if auger_label else None)

    def plot_neutrinos(self, result, result_each_tde=None, source=True, cosmo=True,
                       total=False, ls=None, color=None, label=None, loc=None):
        ls_source = "--" if ls is None else ls
        ls_cosmo = "-." if ls is None else ls
        ls_total = "-" if ls is None else ls
        cycle = plt.rcParams["axes.prop_cycle"].by_key()["color"]
        color_source = cycle[0] if color is None else color
        color_cosmo = cycle[1] if color is None else color
        color_total = "saddlebrown" if color is None else color
        label_source = "Source" if label is None else label
        label_cosmo = "Cosmogenic" if label is None else label
        label_total = "Total" if label is None else label
        if label == "no_label":
            label_source = label_cosmo = label_total = None

        self._plot_nu_data()

        cosmo_range = [11, 12, 13, 14]
        source_range = [16]
        source_nus = result.get_solution_group(source_range)
        cosmo_nus = result.get_solution_group(cosmo_range)
        ax_plots = []
        if source:
            line, = plt.loglog(source_nus[0], source_nus[1] / source_nus[0],
                               label=label_source, lw=2, ls=ls_source,
                               color=color_source, alpha=0.3)
            ax_plots.append(line)
        if cosmo:
            line, = plt.loglog(cosmo_nus[0], cosmo_nus[1] / cosmo_nus[0],
                               label=label_cosmo, lw=2, ls=ls_cosmo,
                               color=color_cosmo, alpha=0.3)
            ax_plots.append(line)
        if total:
            line, = plt.loglog(cosmo_nus[0], cosmo_nus[1] / cosmo_nus[0]
                               + source_nus[1] / source_nus[0], lw=3, ls=ls_total,
                               color=color_total, label=label_total)
            ax_plots.append(line)

        if result_each_tde is not None:
            for key, res_tde in zip(SCENARIOS, result_each_tde):
                src = res_tde.get_solution_group(source_range)
                cos = res_tde.get_solution_group(cosmo_range)
                plt.loglog(cos[0], cos[1] / cos[0] + src[1] / src[0], lw=3,
                           ls=TDE_STYLES[key]["ls"], color=TDE_STYLES[key]["color"],
                           label=key)

        plt.legend(ncol=3, loc="upper center", frameon=True)
        plt.axis([2e4, 2e10, 1e-11, 9e-7])
        plt.ylabel(r"$E^2 dN/dE$ [GeV cm$^{-2}$ s$^{-1}$ sr$^{-1}$]")
        plt.xlabel("E [GeV]")
        return ax_plots

    def _plot_nu_data(self):
        sd = self.spectra_data
        sets = self.plot_data_sets["nu"]
        if sets["HESE"]:
            HESE = sd["HESE"]
            uplims = HESE["upper_err"].value == 0
            plt.errorbar(HESE["energy"].value, HESE["flux"].value,
                         (HESE["lower_err"].value, HESE["upper_err"].value),
                         uplims=uplims,
                         xerr=(HESE["energy"].value * 0.3, HESE["energy"].value * 0.43),
                         ls="none", color="k")
            plt.text(2e5, 7e-8, "HESE", color="k")
        if sets["IC9yr"]:
            ic = sd["ic_9yr"]
            plt.loglog(ic["energy"].value, ic["limit"].value, color="blue", lw=1.7)
            plt.text(8e6, 3e-8, "IC 9 year", color="blue")
        if sets["ICGen2"]:
            gen2 = sd["gen2"]
            limit = gen2["limit"].value
            plt.loglog(gen2["energy"].value, limit, color="k", lw=0.9)
            plt.text(2.7e7, limit[int(limit.size / 15)] * 0.55, "IC Gen2", color="k")
        if sets["RNO-G"]:
            rno = sd["rno_g_2020"]
            plt.loglog(rno["energy"].value, rno["limit"].value / 2, color="tab:olive", lw=0.9)
            plt.text(3.5e8, 1e-8, "RNO-G", color="tab:olive")
        if sets["GRAND200K"]:
            grand = sd["GRAND200K_new"]
            plt.loglog(grand["energy"].value, grand["limit"].value, color="r", lw=0.9)
            plt.text(1.6e9, 2.0e-9, "GRAND\n200k", color="r")
        if sets["Auger2019"]:
            pao = sd["PAO_nu_2019"]
            energy, limit = pao["energy"].value, pao["limit"].value
            plt.loglog(energy, limit, color="magenta", lw=0.9)
            plt.text(energy[0] * 2, limit[0] * 0.5, "Auger 2019", color="magenta")

    def plot_data_simple(self, title="TDE source model", label_E=2.8e11,
                         label_offset=0.5, label_alpha=0.2, plot_total_flux=True):
        with self.plot_output:
            self.plot_output.clear_output(wait=True)
            fig, axs = plt.subplots(2, 2, figsize=(14, 9.5),
                                    gridspec_kw={"height_ratios": (1, 0.63),
                                                 "hspace": 0.3, "wspace": 0.3})

            self.get_scan_comb_result()
            self.change_xmax_model()

            fig.sca(axs[0][0])
            self.plot_cosmic_rays(self.plot_results_comb, self.plot_results_each,
                                  label_E=label_E, label_offset=label_offset,
                                  label_alpha=label_alpha, plot_total_flux=plot_total_flux)
            self._energy_band("Auger", "TA")

            fig.sca(axs[0][1])
            self.plot_neutrinos(self.plot_results_comb, self.plot_results_each,
                                source=True, cosmo=True, total=plot_total_flux)

            fig.sca(axs[1][0])
            self.plot_xmax_mean(self.plot_results_comb, self.air_shower_model["model"], lw=2.5)
            plt.fill_between([1e8, 6e9], 1e-1, 1e3, color="gray", alpha=0.4)
            plt.legend(loc="upper right")

            fig.sca(axs[1][1])
            self.plot_xmax_sigma(self.plot_results_comb, self.air_shower_model["model"], lw=2.5)
            plt.fill_between([1e8, 6e9], 1e-1, 1e3, color="gray", alpha=0.4)
            plt.legend(loc="upper right")

            plt.suptitle(title, color="gray", fontsize=24, weight="semibold", y=0.99)
            plt.tight_layout(rect=(0, 0, 1, 0.95))
            plt.subplots_adjust(left=0.08, right=0.95, bottom=0.09, top=0.95)
            plt.show()

    def _energy_band(self, *detectors):
        lower = min(self.cr_syst[d]["E"] for d in detectors)
        plt.fill_between([1e9, 6e9 * (1 + lower / 100)], 1e-1, 1e3, color="gray", alpha=0.4)

    # ---- entry point --------------------------------------------------- #

    def display(self):
        return display(self.box_ui)
