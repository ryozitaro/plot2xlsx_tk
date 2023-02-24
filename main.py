from pathlib import Path

from folderselect import folder_select
from showplot import ShowPlot
from xlsxout import XlsxOut

spe_height = 10
while True:
    data_list = []
    p_ini_t = float(input("P波の初期補正値[s]を入力してください:"))
    s_ini_t = float(input("S波の初期補正値[s]を入力してください:"))

    with XlsxOut() as xo:
        for i in range(2):
            if spe_height_input := input(f"供試体高さ[cm]を入力してください. 現在{spe_height}[cm]. そのままEnterで変更なし:"):
                spe_height = float(spe_height_input)

            p_folder = folder_select("P波のデータ番号を入力してください:")
            s_folder = folder_select("S波のデータ番号を入力してください:")

            plot = ShowPlot(p_ini_t, s_ini_t, spe_height, p_folder, s_folder)
            plot.show()
            sel_df = plot.get_sel_df()
            img = plot.out_image()

            xo.main_write(sel_df, p_folder, s_folder, img)

            if i < 1 and input("このブックで処理を続けますか?[y/N]:") == "y":
                pass
            else:
                break

    file_name = Path(input("Excel出力ファイル名を入力してください(xlsx拡張子を除く):") + ".xlsx")
    xlsx = xo.get_xlsx()
    file_name.write_bytes(xlsx)
    print(file_name, "にエクセルファイルを出力しました.")

    if input("次のファイルを作成しますか?[y/N]:") == "y":
        continue
    else:
        break

input("終了するにはEnterキーを押してください.")
exit()
