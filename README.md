# Game-of-Life

## Description

Conway game of life Visualizer is a Python application for simulating [Conway's Game of Life][wikipedia game of life] Conway's Game of Life that allows you to perform a cellular automata simulation on saved or personalized configurations.

Presentation video (short): [YouTube video](https://www.youtube.com/watch?v=at3M9MfzzFg)
Presentation video (long): [YouTube video](https://www.youtube.com/watch?v=ewE061Sv1T4)

## Requirements

- Python version 3 (latest one is preferred)
- *ps2pdf* (required only to create PDF files)

It works on Linux and Windows Operating systems

## Features

- You can define your own configuration
- You can change the configuration (add or remove cells) while the simulation is running
- You can save/load configurations in/from CSV files
- You can Save current configuration as PDF/PS files
- You can customize your simulation by changing the shape of the cells: square, circle, triangle
- You can customize your simulation by changing the color of the cells, the grid, and the background
- You can select a zone and do one of the actions:
    - Fill the zone with cells
    - Remove all the cells in the zone
    - Copy then paste the content of the zone
    - Save the zone as a PDF/PS files
- You can run the simulation step by step
- You can change the speed of the simulation while it's running

## List of shortcuts

- **Simulation**
    - `<Enter>`: Start/Stop the simulation
    - `<n>`, `<N>`, or `<Right Arrow>`: next step

- **Configuration of the grid**
    - `<F1>` Choose the color of the grid
    - `<F2>` Choose the color of the cells
    - `<F3>` Choose the color of the background
    - `<Alt>+<C>` Change the shape of the cells to circle
    - `<Alt>+<S>` Change the shape of the cells to square
    - `<Alt>+<T>` Change the shape of the cells to triangle

- **Save and/or load configuration**
    - `<Ctrl>+<O>` Load a configuration
    - `<Ctrl>+<S>` Save the current configuration in a csv file
    - `<Ctrl>+<P>` Save the configuration as a PDF file
    - `<Ctrl>+<T>` Save the configuration as a PS file
    - `<Ctrl>+<J>` Save the configuration as a JPEG file
    - `<Ctrl>+<G>` Save the configuration as a GIF file

- **Edit**
    - `<Ctrl>+<C>` Clean grid (remove all cells in the grid)
    - `<Ctrl>+<F>` Fill all the grid
    - `<Button-Left>` Add cells
    - `<Ctrl>+<Button-Left>` Remove cells
    - `<Button-Right>` Context menu - Select a zone (see `Miscellaneous` section)

## Miscellaneous
- You can control the speed of the simulation.
- Using Right Button, you can select a zone of the grid in order to:
    - Fill it
    - Clean it
    - Copy/Paste it
    - Save it in a PDF/PS file

## Pictures

![Capture 1](https://raw.githubusercontent.com/touatily/Game-of-Life-Visualizer/master/pictures/Capture.PNG)
![Capture 2](https://raw.githubusercontent.com/touatily/Game-of-Life-Visualizer/master/pictures/Capture1.PNG)
![Capture 3](https://raw.githubusercontent.com/touatily/Game-of-Life-Visualizer/master/pictures/Capture2.PNG)


[Wikipedia game of life]: https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
