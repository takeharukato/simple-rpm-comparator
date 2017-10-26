# Open HPC調査ツール
## 初めに
	本ツールは, Open HPCのパッケージを調査するためのツール群である。

	1. lsrpm.py  rpmを含むディレクトリからパッケージの情報を表形式で出力する
	2. compare-pkgs.py 2つのディレクトリ内のRPMについて, パッケージ名,バージョン,概要を比較した表を作成する

## 事前準備
root以下を実行する

sudo yum install -y  python-pandas numpy

## 実行方法
### lsrpm.py

lsrpm.pyの引数にRPMパッケージファイルを含むディレクトリを指定してください。
サブディレクトリがあれば, サブディレクトリを自動的にたどって探査します。

指定したディレクトリ内の各RPMパッケージのターゲットアーキテクチャ名,
パッケージ名, グループ, バージョン, サマリ, ライセンス, パッケージサイ
ズをCSV形式で出力します。

出力結果は標準出力に出力されます:

	>
	> lsrpm.py RPMパッケージを入れたディレクトリ 
	>
	
	実行例
	> ./lsrpm.py ./OpenHPCv1.3 > OpenHPCv1.3.txt

### compare-pkgs.py
2つのディレクトリ内のRPMファイルについて, 
パッケージ名からサフィックス(-*, -ohpcや-orch)を取り除いた名前で2つのファ
イルを比較し, それぞれのパッケージ名,バージョン,サマリを指定した標準出力に出力します。

アーキテクチャ,パッケージ名, 1つ目のディレクトリに含まれるパッケージの版数, 2つ目のディレクトリに含まれるパッケージの版数, 版数の大小, サマリ
をcsv形式で出力します。

書式は以下の通りです:
>	
> compare-pkgs.py -f 1つ目のディレクトリ -s 2つ目のディレクトリ
>	
	
実行例
>
> ./compare-pkgs.py -f ./OpenHPCv1.2 -s ./OpenHPCv1.3
>

## 典型的な使い方

例えば, Open HPCv1.2とv1.3の相違を調査する場合の手順を例に典型的な使用法を記載します.
lsrpm.pyとcompare-pkgs.pyがカレントディレクトリにあることを前提に説明します。

1. Open HPC v1.2のRPMパッケージをv1_2というディレクトリに格納します。
   > mkdir v1_2
   > cd v1_2
   > wget -r -l1 -A .rpm -nd http://build.openhpc.community/OpenHPC:/1.2/CentOS_7.2/x86_64
   > wget -r -l1 -A .rpm -nd http://build.openhpc.community/OpenHPC:/1.2/CentOS_7.2/noarch
   > cd ..
2. Open HPC v1.3のRPMパッケージをv1_3というディレクトリに格納します。
   > mkdir v1_3
   > cd v1_3
   > wget -r -l1 -A .rpm -nd http://build.openhpc.community/OpenHPC:/1.3/CentOS_7/x86_64
   > wget -r -l1 -A .rpm -nd http://build.openhpc.community/OpenHPC:/1.3/CentOS_7/noarch
   > cd ..
3. lsrpm.pyを使用してOpen HPC v1.2の一覧表をOpenHPCv1_2.txtに出力します。
   > ./lsrpm.py v1_2 > OpenHPCv1_2.txt
4. lsrpm.pyを使用してOpen HPC v1.3の一覧表をOpenHPCv1_3.txtに出力します。
   > ./lsrpm.py v1_3 > OpenHPCv1_3.txt
5. compare-pkgs.pyを使用してOpen HPC v1.2とOpen HPC v1.3を比較した結果を標準出力に出力します。
   > ./compare-pkgs.py -f ./v1_2 -s ./v1_3
   
   
