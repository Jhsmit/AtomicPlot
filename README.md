# AtomicPlot
Easy plotting and data handling in Jupyter Notebooks with `Atom` based DataObjects



**This README is hopelessly out-of-date and is no longer accurate. It does reflect some of the ideas of the scope of the project. Also check out ipython/BrowseGraph in a Jupyter notebook, its kinda neat**. Cheers! 

---------------------------------------

DataObjects are initiated by giving it x- and y-data:
```python
from atomicplot import DataObject

x = [1, 2, 3]
y = [5, 7, 9]
d1 = DataObject(x, y)

```

DataObjects support all basic arithmatic operators, these operate on the y-data. The operators accept both scalars and vectors, provided the shapes are compatible. Arithmatic between objects is only allowed if the x-data is identical. These operations return a new DataObject object. Internal operators can be used to modify the y-data inplace.

```python
y1 = [10, 20, 30]
d1 = DataObject(x, y)
d2 = d1 * 5
d3 = d1 + d2
d3 *= 3
d4 = d1 + y1

d1.label = 'Test_data'
d3.reset()  # Restores the DataObject with the x- and y-data with which it was initiated.
```

DataObjects can be grouped in a DataSet. The datasets are stored in an internal OrderedDict. Datsets support most of python's lists functionality, like indexing and iteration.

```python
from atomicplot import DataSet
dataset = DataSet()  # Initiation of empty DataSet
dataset.add([d1, d2, d3])  # Adding of DataObjects
dataset[1] += 10  # Increase y-data of d2 by 10
if d1 in dataset:  # Testing for membership
  pass

for d, i in enumerate(dataset):  # Iteration over DataObjects in DataSet
  d += i*10
  
subset = DataSet(dataset[1:])  # Create a new dataset as a subset of dataset
```

These DataObjects or DataSet have a DataPlotObject mixin which provides easy plotting by giving the data to a Plot object, either a matplotlib (MatPlot) or Plotly (PlotlyPlot) object. The DataPlotObject provides x and y data to the Plot object, which are derived from the x-data and y-data.

```python
from atomicplot import MatPlot

mp = MatPlot()
mp.add_data(d1)

d1.normalize = True  # Normalize the data to 1, equivalent to d1 /= d1.max()
d1.zero = True  # Zero the data, equivalent to d1 -= d1.min()
```

Operations such as normalize and zero leave the y-data attribute unchanged. The zero operation is applied before normalize such that both zero and normalize will result in data between zero and one. 

Both x- and y- data can be modified in this way. 

```python
d1.set_xunits('nm', unit='energy')  # Set the x-units of the x-data. 
d1.rescale_x('cm-1')  # Rescale the x-axis to wavenumber
d2.rescale_y(1000.)  # Rescale y-axis by multiplying with 1000.
```

Labels, titles and legend can be enabled and adjusted through properties on the Plot object. Note that when setting the x-units to nm this can correspond to both length and energy, therefore an extra kwarg is required. 

```python
mp.title = 'What a nice plot!'
mp.xlabel = 'Wavenumber (%units)'
mp.ylabel = 'Intensity x 1000'
mp.savefig('figure1.png')
```





