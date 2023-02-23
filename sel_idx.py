import pandas as pd

SPE_HEIGHT = ("供試体高さ", "[cm]")
IN_T = ("in", "[s]")
OUT_T = ("out", "[s]")
INI_T = ("初期補正", "[s]")
DELTA_T = ("Δt", "[s]")
V = ("V", "[m/s]")
POISSON = ("ポアソン比", "")

def create_df():
    sel_df = pd.DataFrame(
            data={
                SPE_HEIGHT: float("nan"),
                IN_T: float("nan"),
                OUT_T: float("nan"),
                INI_T: float("nan"),
                DELTA_T: float("nan"),
                V: float("nan"),
                POISSON: float("nan"),
            },
            index=("P", "S")
        )
    return sel_df
