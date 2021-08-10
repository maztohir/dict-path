from __future__ import annotations
from collections import UserDict
from typing import Union, Any

import copy
import json


class DictPath(UserDict):
	"""
		DicPath is a normal dict but you can extract and inject the complex nested dict only using Path.
	"""

	# FIX wrong behavior of standard library
	# <a>.pop(<b>, None) returns key error, if <b> not in <a>.
	# This fixes it.
	def pop(self, key, *args):
		return self.data.pop(key, *args)

	def __init__(self, dictionary: dict = {}, deep_copy: bool = False):
		"""
			Accept python dict or DictPath.
		"""
		if isinstance(dictionary, DictPath):
			self.data = dictionary.data
		elif isinstance(dictionary, dict):
			self.data = dictionary
		else:
			raise Exception("dictionary must be a dict")
		if deep_copy:
			self.data = copy.deepcopy(self.data)

	@property
	def dict(self) -> dict:
		"""
			Returns a reference to the dict.
		"""
		return self.data

	@property
	def deepcopy(self) -> DictPath:
		"""
			Create a complete copy of a DictPath
		"""
		return DictPath(self, deep_copy=True)

	def __repr__(self) -> str:
		"""
			Returns a pretty indented json string representation.
		"""
		dump = json.dumps(self.data, indent=2, sort_keys=True)
		return f"DictPath({dump})"
		
	def clean_path(self, path):
		path = path[1:] if path.startswith('/') else path
		return path.split('/')

	def get(self, path: str) -> Union[DictPath, Any]:
		"""
			Get the value of the dictionary at the given path
			dict.get("foo/bar/foo1/bar1") is like calling dict["foo"]["bar"]["foo1"]["bar1"].
			Invalid paths return None without error.
		"""
		path = self.clean_path(path)
		if path == "":
			return self
		current = self.data
		for attr in path:
			if not isinstance(current, dict):
				raise Exception(f"Your path is not a path of dicts (value at key {attr} is of type {type(current)})")
			if attr not in current:
				return None
			current = current[attr]
		if isinstance(current, dict):
			return DictPath(current)
		return current

	def set(self, path: str, value=None):
		"""
			Set the value of the dictionary at the given path
			dict.set("foo/bar/foo1/bar1", 'bar') is like calling dict["foo"]["bar"]["foo1"]["bar1"] = "bar".
			If a path does not exist, it will be created.
			Empty path will do nothing.
		"""
		path = self.clean_path(path)
		current = self.data
		last_path_attr = path.pop()
		for attr in path:
			if not isinstance(current, dict):
				raise Exception("Can't set the key of a non-dict")
			current.setdefault(attr, {})
			current = current[attr]
		if isinstance(value, DictPath):
			current[last_path_attr] = value.data
		else:
			current[last_path_attr] = value

	def __getitem__(self, path) -> Any:
		""" Subscript for <DictPath>.get() """
		# If DictPath["key1"], then path="key1"
		# DictPath["key1", "key2"], then path=tuple("key1", "key2")
		
		path = "/".join(list(path)) if isinstance(path, tuple) else path
		return self.get(path)

	def __setitem__(self, path, value):
		""" Subscript for <DictPath>.get() and <DictPath>.apply_at_path() """
		path = "/".join(list(path)) if isinstance(path, tuple) else path
		self.set(path, value=value)

def extract_dict(dictionary, path):
    path = path[1:] if path.startswith('/') else path
    paths = path.split('/')
    active_dict = dictionary
    for p in paths:
        if active_dict.get(p) != None:
            active_dict = active_dict.get(p)
        else:
            return None
    return active_dict

def inject_dict(dictionary, path, value):
    path = path[1:] if path.startswith('/') else path
    paths = path.split('/')
    path_len = len(paths)
    _active_dict = dictionary
    for i, p in enumerate(paths):
        if i == path_len - 1:
            _active_dict[p] = value
        else:
            if _active_dict.get(p) == None:
                _active_dict[p] = {}
            _active_dict = _active_dict.get(p)
    return dictionary
    
