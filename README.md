

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

<a href="https://gctpy.com/graph/d7b78eade68aea0db04cc4b0e170e3bb50ab1fdd5dfead522dfa596babf534cf">
<img width="500" style="border-radius: 50%;" alt="image" src="https://user-images.githubusercontent.com/43754306/210659872-98e5b8c7-9425-4479-a473-1cce6ccfbd00.png">
</a>

<br>
<br>


  
  
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

<br>

### Some examples you can run GCT on:

[Simple python file](https://gctpy.com/graph/5888f26bdbc0661b7a060552f518e1d129b83b6a303c317ee7aa72524cdbd3c8) •
[karpathy/MinGPT](https://gctpy.com/graph/633f83124187744cc37e50c156c4057408a1832422217f84b8837a2aa21a4489) •
[scikit-learn/cluster](https://gctpy.com/graph/e42dc4424c1ce403d9e474881ce8ed820d09fe08a5432aa61c232c3d6206c546) •
[geohot/tinygrad](https://gctpy.com/graph/a73b37913d69cfbdce7f7334d77410df709b9ecfe744fd1cbbe5667dfc785276) •
[PyTorch/autograd](https://gctpy.com/graph/667d9a1b24d6a00cfc2eb50eb28cb6f0d1d949c2c91eaf83b767771b40499c63) •
[Flask Web App](https://gctpy.com/graph/8ffedfe38ee614410f3919cd5f576f4afb07a29717fbcfb5fefa8d5d772c11e7)


Generate graph for any python file
```sh
python -m gct -i path/to/file.py
```

Generate graph for any python file hosted on a web server
```sh
python -m gct -i https://github.com/user_name/path/to/file.py
```


## Installation

### *Step 1: Install GCT*

```
pip install gct-py
```


### *Step 2: Install Graphviz executable (skip if it's already installed)*

GCT generates graphs using [graphviz](https://graphviz.org). To get accurate graphs, we highly
recommend using graphviz>=6.0.1.

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
  
Install graphviz by downloading version >=6.0.1 from [graphviz](https://graphviz.org/download/#linux) website.
Unfortunately, graphviz is only updated to 2.4 on Linux systems. We've seen inconsistencies from the GCT outputs when
using this version, particularly in clustering python classes together. You can still run it, however, for more accurate
information, try out the easy-to-use web app: [gctpy.com](https://gctpy.com).
  
```
  sudo apt install graphviz
```
  
</details>


### *Step 3: (optional) Upgrade graphviz executable version*


<details>
  <summary>MacOS</summary>
  
  Find dot path:
  ```
  where dot
  ```
  Remove dot executable:
  ```
  sudo rm -rf "path/to/dot/executable"
  ```
  Uninstall graphviz package:
  ```
  brew uninstall graphviz
  ```
  Install graphviz package:
  ```
  brew install graphviz
  ```
  
</details>

<details>
  <summary>Windows</summary>
  
  Find dot path:
  ```
  where dot
  ```
  Remove dot executable:
  ```
  del "/path/to/dot/executable"
  ```
  Uninstall graphviz package:
  ```
  sudo rm -rf /Applications/graphviz.app
  ```
  
  Install graphviz package using [instructions](#step-2-install-graphviz-executable-skip-if-its-already-installed) shared above.
</details>

<details>
  <summary>Linux</summary>
  
  Find dot path:
  ```
  which dot
  ```
  Remove dot executable:
  ```
  sudo rm -rf "path/to/dot/executable"
  ```
  Uninstall graphviz package:
  ```
  sudo apt-get remove graphviz
  ```
  Install graphviz package:
  ```
  sudo apt install graphviz
  ```
  
</details>
  
  
## Configuration

Customize the experience by aliasing `gct`:
```
alias gct=python -m gct -i'
gct -i path/to/file.py
```


  

