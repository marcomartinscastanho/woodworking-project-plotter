# woodworking-project-plotter

Application of the [Rectangle packing](https://en.wikipedia.org/wiki/Rectangle_packing) problem with [Guillotine cutting](https://en.wikipedia.org/wiki/Guillotine_cutting) for woodworking projects.  
Uses [rectpack](https://github.com/secnot/rectpack) to determine the cuts and [matplotlib](https://github.com/matplotlib/matplotlib) to plot the outcome.

## Usage

```sh
python main.py path/to/project_config.py
```

where `project_config.py` must define:

```py
bins: list[Bin]
shapes: list[Shape]
```

Check `projects/example/example.py` for an example.

## Authorship

Everything implemented by myself, except the `load_work_config` in `loader.py`, which was done by ChatGPT.
