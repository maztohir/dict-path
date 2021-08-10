# DictPath
Extended dict for Python. 
Make easy to extract complicated nested dict.

![repo-size](https://img.shields.io/github/repo-size/maztohir/dict-path)
![license](https://img.shields.io/github/license/maztohir/dict-path)

## Installation
```bash
pip3 install dict-path
```

## Getting and setting value with path

#### No more boilerplate code to extract or inject nested dict
##### What you do previously
```python
test_dict = {'foo1':{'foo2':{'foo3':{'foo4':'bar'}}}}
foo1 = test_dict['foo1']
if foo1:
   foo2 = foo1['foo2']
   if foo2:
       foo3 = foo2['foo3']
       if foo3:
           foo4 = foo3['foo4'] #finally, get the result: bar1
```
##### What you can do NOW
```python
test_dict = {'foo1':{'foo2':{'foo3':{'foo4':'bar'}}}}
data = DictPath(test_dict)
data.get('foo1/foo2/foo3/foo4') #result: bar


# set value with easy
data.set('foo1/foo2/foo3/foo5', 'bar1')
data.get('foo1/foo2/foo3/foo5') #result: bar1
```

#### Do not want to use new Object? no worries, we have a method that you can call directly

```python
from dict_path import extract_dict, inject_dict

test_dict = {'foo1':{'foo2':{'foo3':{'foo4':'bar'}}}}
extract_dict(test_dict, 'foo1/foo2/foo3/foo4') #result: bar

inject_dict(test_dict, 'foo1/foo2/foo3/foo5', 'bar1')}
extract_dict(test_dict, 'foo1/foo2/foo3/foo5') #result: bar1
```

## Concept
#### DictPath is basically a normal python dict, nothing different
```python
# A DictPath keeps a reference to the original initializing dict:

normal_dict = {'foo1':{'foo2':{'foo3':{'foo4':'bar'}}}}
dic_path = DictPath(normal_dict)
> normal_dict == dic_path
---> True
> dic_path.dict is normal_dict
---> True
```

#### You can also get a deep copy:
```python
joe = DictPath(user, deepcopy=True)
> joe == user
---> True
> joe.dict is user
---> False
```

#### Invalid path will return None
```python
from dict_path import extract_dict, inject_dict

test_dict = {'foo1':{'foo2':{'foo3':{'foo4':'bar'}}}}
data = DictPath(test_dict)
data.get('foo1/foo2/foo3/foo4/foo6')
#result: None
```
#### Set up unknown path will create an actual dict
```python
from dict_path import extract_dict, inject_dict

test_dict = {'foo1':{'foo2':{'foo3':{'foo4':'bar'}}}}
data = DictPath(test_dict)
data.set('foo1/foo2/foo3/foo5/foo6/foo7/foo8/', 'bar1')
data.get('foo1/foo2/foo3/foo5/foo6/foo7/foo8/')
#result: bar1
```
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)