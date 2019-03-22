#3F7py_dk538
##Part IIA Full Technical Report

####Running the code

The program runs very similarly to the original lab, with a few extra functions added here and there. These are mostly in the `adaptive` module and within the original `camzip` and `camunzip` functions.

There is also a short script which runs compression tests, aptly named `compress_test.py`. This can be used to test the added methods. 

Training new models must be done using the script `training.py` and the functions in `train1.py` from `adaptive`.

Running the tests is fairly self-explanatory: simply modify the parameters in: 

```python
def run_test(method, filename, context_length)
```
, which is called in `compress_test.py`.

New options for method are `'context'` and `'model'`.

#####Using the 'model' method

When running with the `model` method, the model to be used must be entered in line 98 of `camzip.py`, which reads:

```python
dists = np.float64(train1.load_dist(xset, 'model5.h5'))
```

Note that the models do throw up errors quite a lot during the compression and decompression stages.