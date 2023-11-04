# school-project-python-vslib (2019)
Lineplotlib for python as a school project

README FOR VISUALISATION LIBRARY

ABSTRACT

Visualisation library allows users to recreate visual demonstration of numerical data by exploiting function of vslib.
According to the level of difficulty, library consists of only functions that make simple line plots.
Library also includes example application and the basement for other types of plotting, for example bar plot, as it was mentioned in the assignment.


STRUCTURE

 -- class Reader

Class Reader extracts information from numerical data, figures out wrong inputs and records new values.
This class is extremely import for whole project as it becomes a helping hand through visualization process in GUI class.
Simultaneously it also gives us clear understanding where typo came from, i.e user can easily identify
the problem during processing input data. Therefore the class is connected with Error class. Method def read_csv_file,
major function of the class, returns six outcomes: minimum and maximum values of first and second parameter
 as well as differences between these values.

 -- class Error

Superficial class that raises an error if one has been caused. Error is accompanied by corresponding message.

 -- class GUI

This class is responsible for implementation of PyQt5 libraries. That is, it subordinates methods, such as: initializing window,
title, labels and legend, setting grid and scales, drawing axises and lineplot. Finally, GUI class became a backbone
for Lineplot.


 -- class Test

This ancillary class helps to find out dysfunctions, errors, wrong inputs or values. 

 -- class Plot, class Lineplot (Plot)

These particular classes allow us show up GUI class with its corresponding properties, i.e. plot the figure.


INSTALLATION

Download the project with all packages it includes. Program also requires PyQt5 libraries, thus their
installation is a key factor. In order to utilize given functions, user has to upload vslib.plot
and import Plot, Lineplot. Once user has an access to them, she must to import csv-file on her directory.
Only after completing these tasks user can proceed to visualization. 



MANUALS
```
Lineplot('name', 'xlabel', 'ylabel', grid, ‘title')
```
Where ‘name’ is the name of input file, an absolute path of data, ‘xlabel’ is labelling for x-axis, ‘ylabel’ for y-axis, grid is a positive integer
for adjusting plot’s grid and ‘title’ is simply the title of plotted window. In the case if user has no desire to give additional
options for her plot, she can mark None and 0 as these options return features by default:
```
Lineplot('name', None, None, 0, None)
```
In addition, we are able to exploit example application. To do so, user needs to write down simple code:
```
Plot(‘example')
```
