

<div align="center">

# Graphical Code Tracer
<p align="center">
  <a href="https://pepy.tech/project/gct-py">
    <img src="https://static.pepy.tech/badge/gct-py" alt="users">
  </a>
  <a href="https://github.com/QasimWani/gct/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/License-GNU%20GPL-green.svg" alt="license"/>
  </a>
  <a href="https://pypi.org/project/gct-py">
    <img src="https://img.shields.io/pypi/v/gct-py?color=blue" alt="license"/>
  </a>
  <a href="https://github.com/QasimWani/gct/graphs/contributors" alt="Contributors">
    <img src="https://img.shields.io/github/contributors/QasimWani/gct" />
  </a>
  <a target="_blank" href="https://twitter.com/intent/tweet?text=GCT is a code visualization tool that generates a graphical representation of any python program! Try it out: https://gctpy.com" class="item">
          <img src="https://img.shields.io/twitter/url?label=Tweet&amp;style=social&amp;url=https://gctpy.com">
        </a>
</p>

Graphical Code Tracer (gct) is the world's first visual static code analyzer.

Within **seconds** it can tell you how your functions and classes are connected to each other!

![](/demo.gif)


  
[GCT web app](https://gctpy.com) •
[Getting started](#getting-started) •
[Installation](#installation) •
[Configuration](#configuration)

</div>

## Getting started


### Usecases:
1. Onboard to new codebases faster.
2. Debug code faster [Twitter thread](https://twitter.com/qasim31wani/status/1609677492347981825)
3. Create share-able versions of your code. Using gctpy.com, you can instantly share your UML diagrams across teams.


### Some examples you can run GCT on:

[Simple python file](https://gctpy.com/graph/5888f26bdbc0661b7a060552f518e1d129b83b6a303c317ee7aa72524cdbd3c8) •
[karpathy/MinGPT](https://gctpy.com/graph/633f83124187744cc37e50c156c4057408a1832422217f84b8837a2aa21a4489) •
[scikit-learn/cluster](https://gctpy.com/graph/e42dc4424c1ce403d9e474881ce8ed820d09fe08a5432aa61c232c3d6206c546) •
[geohot/tinygrad](https://gctpy.com/graph/a73b37913d69cfbdce7f7334d77410df709b9ecfe744fd1cbbe5667dfc785276) •
[PyTorch/autograd](https://gctpy.com/graph/667d9a1b24d6a00cfc2eb50eb28cb6f0d1d949c2c91eaf83b767771b40499c63) •
[Flask Web App](https://gctpy.com/graph/8ffedfe38ee614410f3919cd5f576f4afb07a29717fbcfb5fefa8d5d772c11e7)


Generate graph for any python file
```sh
python -m gct -i path/to/file.py # run gct on a local file
python -m gct -i https://github.com/user_name/path/to/file.py # run gct on a file hosted on a web server
```


## Installation

### *Step 1: Install GCT Python package*

```
pip install gct-py
```


### *Step 2: (Skip if already installed) Install Graphviz executable*

GCT generates graphs using [graphviz](https://graphviz.org). To get accurate graphs, we highly
recommend using latest graphviz version available for your OS.

If you've already installed graphviz executable version, check the dot version by running: `dot -V`.

<details>
  <summary>Windows</summary>

  Install graphviz by downloading executable (version >=6.0.1) from [graphviz](https://graphviz.org/download/#windows) website.
  
</details>

<details>
  <summary>MacOS</summary>

  (Optional) more details: [graphviz](https://graphviz.org/download/#mac).
  
```
  brew install graphviz
```
  
</details>

<details>
  <summary>Linux</summary>

  (optional) more details: [graphviz](https://graphviz.org/download/#linux).
  
```
  sudo apt install graphviz
```
  
</details>
  
  
## Configuration

Customize the experience by aliasing `gct`:
```
alias gct='python -m gct -i'
gct path/to/file.py
```


  

