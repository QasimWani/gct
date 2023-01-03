# Graphical Code Tracer (gct) is the world's first static code visualization tool.

Requires Python >= 3.7

Install command line tool: `pip install gct-py`

Running GCT is extremely simple!
`python -m gct --input <path/to/file.py>`

If you'd like to run `gct` as an executable, run it as an alias:
`alias gct='python -m gct'`
And then: `gct -i <path/to/file.py>`

Test example to make sure everything works:
`python -m gct -i https://github.com/QasimWani/gct/blob/main/examples/arithmetics.py`



# Installing Graphviz
- Besides the pip package, graphviz (automatically installed when running `python -m gct`, you need to have the dot executable which runs graphviz on the desktop. 
- Install graphviz (>= 6.0.1) : https://graphviz.org/download/#executable-packages

#### Incorrect dot version?
If your dot version is less than 6.0.1 (`dot -v`), you need to upgrade it. To do so:
1. Find path of dot executable. `which dot` (`where dot` for Windows)
2. Remove dot file. `sudo rm <OUTPUT of (1)>`
3. Reinstall graphviz: https://graphviz.org/download/#executable-packages

For any other issues, post an issue: https://github.com/QasimWani/gct/issues/new
