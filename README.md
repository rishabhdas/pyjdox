# PyJdox

PyJdox is an API documentation tool. Unlike pydoc, it returns output as JSON
which can later be parsed.

### Data points covered

- Function Doctring
- Function Arguments
- Module file location
- Namespace


### Usage

```python
python pyjdox.py -f <filename>
```

OR

```python
python pyjdox.py -d <source-tree>
```
where,
- source-tree: refers to source code of a module
- filename: refers to the python code file that needs to be documented.
