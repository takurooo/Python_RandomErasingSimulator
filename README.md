  # Python_RandomErasingSimulator
 
 Simulation for [Random Erasing Data Augmentation](https://arxiv.org/pdf/1708.04896.pdf).



![sample](https://user-images.githubusercontent.com/35373553/61216227-ca4be980-a747-11e9-8a89-6d2fcdf04076.gif)


# Requirement
- PIL
- numpy
- matplotlib


# Usage
```
python main.py
```
Open a window as below.
![sample1](https://user-images.githubusercontent.com/35373553/61216539-886f7300-a748-11e9-98e8-85e2218efd4b.png)


File dialog open when you push `open` button.  
You should select a `jpeg` file.


![sample2](https://user-images.githubusercontent.com/35373553/61217009-bc976380-a749-11e9-9d9e-0a3410276a8a.png)


| widget  | name        | Description | 
| ---     | ---         | ---                                           |
| Slider  | sh          | Erasing area max ratio. min ratio is 0.02.                       |
| Slider  | r1          | Erasing aspect min ratio. max ratio is 1/r1.  |
| Slider  | interval    | Display interval (sec)                        |
| Button  | open        | Select jpeg file to display.                  |
| Button  | quit        | Quit simulation.                              |
| Button  | start       | Start RandomErasing.                          |
| Button  | stop        | Stop RandomErasing.                           |