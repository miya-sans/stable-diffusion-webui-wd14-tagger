<p align="center">
🌍
<a href="./README.md">English</a> |
<strong>日本語</strong> |
</p>

---

<div align="center">
   
# Tagger for [Stable Diffusion WebUI Forge - Neo & Classic](https://github.com/Haoming02/sd-webui-forge-classic)

---

</div>

このリポジトリは、67372a氏の [stable-diffusion-webui-wd14-tagger](https://github.com/67372a/stable-diffusion-webui-wd14-tagger) をもとにしたforkです。<BR>

Taggerのforkをまた増やしてしまい、申し訳ありません。<BR>
しかしこのforkは、Forge NeoでTaggerを使用できず困っていた方々の役に立つはずです。<P>

このforkでは、Forge Neoでの実行を妨げていた、未使用かつ不要な機能を削除しました。<BR>
また、このforkは `tensorflow` を使用していないため（`tensorflow` が要求する `protobuf` のバージョンはWebUIの要求と競合します）、A1111/Forge/reForge でも有用であると考えます。

## このforkの変更内容

### 修正内容

- Forge Neoにおいて削除されたDeepbooru Interrogatorに依存していたコードや、古くて互換性のないコードを修正しました。

### 削除した機能

- `tensorflow`
   - `tensorflow` が要求する `protobuf` のバージョンは、WebUIが要求する `protobuf` のバージョンと互換性がありません。
   - オリジナルのTaggerでは、`tensorflow` は `tensorflow 2.10` でのみ利用可能な実験的機能と、DeepDanbooruInterrogatorのためにのみインストールされています。
- `deepdanbooru` とDeepDanbooruInterrogator
   - もう誰も使ってないですよね？
   - 代わりに、WaifuDiffusionInterrogator、MLDanbooruInterrogator、Z3DInterrogatorを利用してください。
- `opencv_python_headless`
   - `opencv_python` と `opencv_python_headless` はインストール時に競合します。Forge Neo には `opencv_python` がインストールされているため、`opencv_python_headless` は不要です。

別のTaggerからこのTaggerに移行した場合、`tensorflow`, `deepdanbooru`, `opencv_python_headless` は他で使用していなければ `pip uninstall` で削除して大丈夫です。

## 更新履歴

### 2026/10/22 (2)

- `requirements.txt` からOpenCVを削除しました。`install.py` はOpenCVが未インストールの場合のみ `opencv_python<4.12` をインストールし、それ以外はWebUIのOpenCVを使用します。
   - Forge Neo 2.31 は `opencv-python==5.0.0.93` を固定しているため、従来の `<4.12` の指定では起動のたびにダウングレードが試みられ、`cv2.pyd` の使用中に失敗していました。

### 2026/10/22

- *Send to txt2img* / *Send to img2img* はプロンプトのみを置き換えるようにしました。サンプリング方法、スケジュールタイプ、ネガティブプロンプトなどの設定は変更されません。
- 画像を貼り付け・選択した際の自動Interrogateは、選択中のInterrogatorが読み込み済みの場合のみ行います。未読み込みの場合は *Interrogate* を押すとモデルが読み込まれます。
- [animetimm](https://huggingface.co/animetimm) のTagger（AnimeTimmInterrogator）を追加しました。`onnxruntime` ではなく `timm` とPyTorchで動作します。
   - [animetimm/convnextv2_huge.dbv4-full](https://huggingface.co/animetimm/convnextv2_huge.dbv4-full) をUIとAPIのデフォルトのInterrogatorに変更しました。
   - `eva02_large_patch14_448`、`caformer_b36`、`swinv2_base_window8_256`（いずれも `dbv4-full`）も利用できます。
   - `requirements.txt` に `timm>=1.0.3` を追加しました。
- animetimmのリポジトリはゲート付きです。ダウンロードするには:
   1. Hugging Faceにログインし、モデルページ（例: [animetimm/convnextv2_huge.dbv4-full](https://huggingface.co/animetimm/convnextv2_huge.dbv4-full)）で利用規約に同意します。
   1. [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) でアクセストークン（read）を作成します。
   1. *Settings* -> *Tagger* -> *HuggingFace access token* に入力するか、環境変数 `HF_TOKEN` を設定するか、`hf auth login`（古い `huggingface_hub` では `huggingface-cli login`） を実行します。
- animetimmのモデルをダウンロード済みの場合は、`models/TaggerTimm/<モデル名>/`（例: `models/TaggerTimm/convnextv2_huge.dbv4-full/`）に `config.json`、`preprocess.json`、`categories.json`、`selected_tags.csv`、`model.safetensors` を元のファイル名のまま置いてください。その場合トークンやダウンロードは不要です。
- デフォルトのモデルは大きい（パラメータ数692M、重み約2.8GB）ため、遅い場合やVRAMに収まらない場合は別のInterrogatorを選択してください。

### 2026/7/11

- `TaggerInterrogateRequest`への`image`フィールドの実装漏れの修正

### 2026/5/30

- Forge Neoにおけるuse_cpuオプションの削除に対応

### 2026/5/7

- `generation_parameters_copypaste` を `infotext_utils` に変更
   - Forge Neoのコミット[e40900c](https://github.com/Haoming02/sd-webui-forge-classic/commit/e40900cd8bf7275d89dd01c534108661960f38f3) (2026/5/5更新) で `generation_parameters_copypaste` が削除されたため。

### 2026/4/20

- `requirements.txt` の `opencv_python` と `opencv_contrib_python` の行に `<4.12` の指定を追加
   - `opencv_python` または `opencv_contrib_python` のバージョンが4.12以上になると `numpy` が 2.x にアップデートされ、`gradio 3.x` を利用するWebUIではControlNetエラーなどの問題が発生します（Forge Neoは `gradio 4.x` を利用しているため問題ありません）。

---

以下は、元のリポジトリが提供しているREADMEです。

---
## Fork changes
- v3 taggers added
- Z3D-E621-Convnext tagger added
- Onnxruntime dep version required by v3 taggers 

Tagger for [Automatic1111's WebUI](https://github.com/AUTOMATIC1111/stable-diffusion-webui)
---
Interrogate booru style tags for single or multiple image files using various models, such as DeepDanbooru.

[한국어를 사용하시나요? 여기에 한국어 설명서가 있습니다!](README.ko.md)

## Disclaimer
I didn't make any models, and most of the code was heavily borrowed from the [DeepDanbooru](https://github.com/KichangKim/DeepDanbooru) and MrSmillingWolf's tagger.

## Installation
1. *Extensions* -> *Install from URL* -> Enter URL of this repository -> Press *Install* button
   - or clone this repository under `extensions/`
      ```sh
      $ git clone https://github.com/picobyte/stable-diffusion-webui-wd14-tagger.git extensions/tagger
      ```

1. *(optional)* Add interrogate model
   - #### [*Waifu Diffusion 1.4 Tagger by MrSmilingWolf*](docs/what-is-wd14-tagger.md)
      Downloads automatically from the [HuggingFace repository](https://huggingface.co/SmilingWolf/wd-v1-4-vit-tagger) the first time you run it.

   - #### *DeepDanbooru*
      1. Various model files can be found below.
         - [DeepDanbooru models](https://github.com/KichangKim/DeepDanbooru/releases)
         - [e621 model by 🐾Zack🐾#1984](https://discord.gg/BDFpq9Yb7K)
            *(link contains NSFW contents!)*

      1. Move the project folder containing the model and config to `models/deepdanbooru`

      1. The file structure should look like:
         ```
         models/
         └╴deepdanbooru/
           ├╴deepdanbooru-v3-20211112-sgd-e28/
           │ ├╴project.json
           │ └╴...
           │
           ├╴deepdanbooru-v4-20200814-sgd-e30/
           │ ├╴project.json
           │ └╴...
           │
           ├╴e621-v3-20221117-sgd-e32/
           │ ├╴project.json
           │ └╴...
           │
           ...
         ```

1. Start or restart the WebUI.
   - or you can press refresh button after *Interrogator* dropdown box.
   - "You must close stable diffusion completely after installation and re-run it!"


## Model comparison
[Model comparison](docs/model-comparison.md)

## Screenshot
![Screenshot](docs/screenshot.png)

Artwork made by [hecattaart](https://vk.com/hecattaart?w=wall-89063929_3767)

## Copyright

Public domain, except borrowed parts (e.g. `dbimutils.py`)
