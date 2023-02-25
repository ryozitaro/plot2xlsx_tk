# plot2xlsx_tk
cmdとtkinterを使って、P波とS波の実験データをxlsxに出力するものです。

## 使い方
main.pyを実行するとcmdが立ち上がるので、供試体の高さ、P（またはS）波の初期補正値、データフォルダの数字を入力します。  
![1](https://user-images.githubusercontent.com/126104168/221366467-0255053a-481e-4bf6-be7b-a68b32d022e5.png)

グラフが4つ表示されたウィンドウが表示されたら、それぞれグラフの適当な場所をクリックすると赤い縦線が表示され、P（またはS）波のinとoutが更新されます。  
![2](https://user-images.githubusercontent.com/126104168/221366474-cc17d571-85b5-4850-8cba-c6e504f83ab7.png)

シートのA1に入れる文字列を入力（任意）したあと、このブックで2シート目を作るか尋ねられますが、この場合はP（またはS）波の初期補正値は１シート目の値が使われます。
![3](https://user-images.githubusercontent.com/126104168/221366477-fd26b48b-ea17-4169-8072-e2c7d2575362.png)

最後にxlsxのファイル名を入力して終わりです。
![4](https://user-images.githubusercontent.com/126104168/221366494-e3ba80b4-a726-45ea-b322-6bbd00956142.png)
