from src.dict_path import extract_dict, inject_dict, DictPath

def test_extract_value():
    test_dict = {'foo1':{'foo2':{'foo3':{'foo4':'bar'}}}}
    assert extract_dict(test_dict, 'foo1/foo2/foo3/foo4') == 'bar'

def test_extract_dict():
    test_dict = {'foo1':{'foo2':{'foo3':{'foo4':'bar'}}}}
    assert extract_dict(test_dict, 'foo1/foo2/foo3') == {'foo4':'bar'}

def test_inject_value():
    test_dict = {'foo1':{'foo2':{'foo3':{}}}}
    inject_dict(test_dict, 'foo1/foo2/foo3', {'foo4':'bar'})
    assert extract_dict(test_dict, 'foo1/foo2/foo3/foo4') == 'bar'

test_dict = {'foo1':{'foo2':{'foo3':{'foo4':'bar'}}}}
data = DictPath(test_dict)

def test_get_path():
    assert data.get('foo1/foo2/foo3/foo4') == 'bar'
    
def test_get_path_start_with_slash():
    assert data.get('/foo1/foo2/foo3/foo4') == 'bar'