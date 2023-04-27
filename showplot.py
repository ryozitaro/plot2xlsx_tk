import io
import tkinter as tk

import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.backend_bases import MouseEvent
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import calc
import sel_idx
from folderdata import FolderData


class ShowPlot:
    def __init__(
        self,
        p_ini_t: float,
        s_ini_t: float,
        spe_height: float,
        p_folder: FolderData,
        s_folder: FolderData,
    ) -> None:
        self.p_folder = p_folder
        self.s_folder = s_folder

        self.sel_df = sel_idx.create_df()
        self.sel_df[sel_idx.SPE_HEIGHT] = spe_height
        self.sel_df[sel_idx.INI_T] = (p_ini_t, s_ini_t)

    def _unit_conv(self, num: int | float) -> str:
        """
        画面に表示される選択ラベル用に、選択された数値を
        その数の大きさに合わせて秒の単位[ms, μs, ns]を変え、strで返します。
        """
        if (abs_num := abs(num)) >= 1 or num == 0:
            return f"{num} [sec]"
        else:
            for combi in ((1e-3, "m"), (1e-6, "μ"), (1e-9, "n")):
                if abs_num < combi[0] * 1000:
                    size, prefix = combi
            return f"{num/size:.3f} [{prefix}sec]"

    def plot(self) -> None:
        """
        画面に表示するプロットを用意します。
        """
        self.fig, self.axes = plt.subplots(2, 2)

        df = self.p_folder.df.join(self.s_folder.df)
        for (name, series), ax in zip(df.items(), self.fig.axes):
            ax.plot(series)
            ax.set_title(name)
            ax.grid(True)
            ax.axvline(df.index[0], color="r", visible=False)

    def mouse_click(self, event: MouseEvent) -> None:
        """
        プロットをマウスクリックした際、画面に表示される選択ラベルと、
        選択用DataFrameを更新します。
        """
        if event.inaxes:
            ax = event.inaxes
            vline = ax.get_lines()[1]
            vline.set_xdata(event.xdata)
            vline.set_visible(True)
            self.fig.canvas.draw_idle()

            if ax.get_subplotspec().is_first_row():
                p_or_s = "P"
                label = self.label_p_wave
                pair_axes = self.axes[0]
            else:
                p_or_s = "S"
                label = self.label_s_wave
                pair_axes = self.axes[1]

            ax_in, ax_out = pair_axes
            vline_in = ax_in.get_lines()[1]
            vline_out = ax_out.get_lines()[1]
            if vline_in.get_visible() and vline_out.get_visible():
                label["text"] = (
                    f"{p_or_s} ini t: {self._unit_conv(ini_t := self.sel_df.at[p_or_s, sel_idx.INI_T])}\n"
                    f"{p_or_s} in t: {self._unit_conv(in_t := vline_in.get_xdata()[0])}\n"
                    f"{p_or_s} out t: {self._unit_conv(out_t := vline_out.get_xdata()[0])}\n"
                    f"{p_or_s} Δt: {self._unit_conv(delta_t := calc.delta(out_t, in_t, ini_t))}\n"
                    f"{p_or_s} V: {(v := calc.v(self.sel_df.at[p_or_s, sel_idx.SPE_HEIGHT], delta_t)):.3f}[m/s]"
                )
                self.sel_df.at[p_or_s, sel_idx.IN_T] = in_t
                self.sel_df.at[p_or_s, sel_idx.OUT_T] = out_t
                self.sel_df.at[p_or_s, sel_idx.DELTA_T] = delta_t
                self.sel_df.at[p_or_s, sel_idx.V] = v

                if self.get_all_selected():
                    p_v, s_v = self.sel_df[sel_idx.V]
                    poisson = calc.poisson(p_v, s_v)
                    if isinstance(poisson, str):
                        text_poisson = f"ポアソン比: {poisson}"
                    else:
                        text_poisson = f"ポアソン比: {poisson:f}"

                    self.label_poisson["text"] = text_poisson
                    self.sel_df[sel_idx.POISSON] = poisson

    def get_all_selected(self) -> bool:
        """
        プロットが全部選択されたか、boolで返します。
        """
        return all(ax.get_lines()[-1].get_visible() for ax in self.fig.axes)

    def show(self) -> None:
        """
        プロット画面を表示します。
        """
        self.plot()

        self.root = tk.Tk()
        self.root.title("plot to xlsx")
        self.root.lift()
        self.root.state("zoomed")

        figure_canvas = FigureCanvasTkAgg(self.fig, self.root).get_tk_widget()
        figure_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(self.root, highlightthickness=0)
        canvas.pack(side=tk.RIGHT)

        kw_text = dict(master=canvas, font=("Meiryo", 16), justify=tk.LEFT)
        kw_pack = dict(padx=30, pady=10, anchor=tk.W)

        spe_height = tk.Label(
            text=f"供試体高さ {self.sel_df[sel_idx.SPE_HEIGHT]['P']:f} [cm]", **kw_text
        )
        spe_height.pack(**kw_pack)

        self.label_p_wave = tk.Label(
            text=f"p ini t: {self._unit_conv(self.sel_df[sel_idx.INI_T]['P'])}",
            **kw_text,
        )
        self.label_p_wave.pack(**kw_pack)

        self.label_s_wave = tk.Label(
            text=f"p ini t: {self._unit_conv(self.sel_df[sel_idx.INI_T]['S'])}",
            **kw_text,
        )
        self.label_s_wave.pack(**kw_pack)

        self.label_poisson = tk.Label(**kw_text)
        self.label_poisson.pack(**kw_pack)

        self.root.update()
        self.fig.tight_layout()
        self.fig.canvas.draw_idle()

        self.fig.canvas.mpl_connect("button_press_event", self.mouse_click)
        self.root.protocol("WM_DELETE_WINDOW", self.window_delete)
        self.root.mainloop()

    def window_delete(self) -> None:
        """
        画面を閉じた際に再選択するか尋ねるメソッド
        """
        self.root.withdraw()
        if self.get_all_selected():
            select_range = ("すべて選択されました.", self.root.quit)
        else:
            select_range = ("未選択のグラフがあります.", exit)

        if input(select_range[0] + "再選択をしますか?[y/N]:") == "y":
            self.root.deiconify()
            self.root.state("zoomed")
        else:
            select_range[1]()

    def get_sel_df(self) -> pd.DataFrame:
        """
        プロットを選択した結果のデータをDataFrameで返します。
        """
        return self.sel_df

    def out_image(self) -> io.BytesIO:
        """
        サイズが1920*1080のプロット画像が入ったBytesIOを取得します。
        """
        img_file = io.BytesIO()
        self.fig.set_size_inches(19.2, 10.8)
        self.fig.tight_layout()
        self.fig.savefig(img_file, format="png")
        return img_file
