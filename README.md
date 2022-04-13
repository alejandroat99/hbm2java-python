# Hbm2Java-Python

The goal of this project is to develop a python script to parse the hibernate xml mapping definition to a Java class. At the current state
of this project, this are the current features:

- Map `<property>` tags
- Map `<id>` tags
- Map `<composite-id>` and `<key-property>` tags
- Map `<many-to-one>` tags
- Map `<set>` tags

## Usage

To use this module, you need to provide the path to the hbm.xml file:

```python
from hbm2java import hbm2java

filepath = 'files/HibernateMapping.hbm.xml'
hbm2java(filepath)

```

Also, you can check the [Test.py](https://github.com/alejandroat99/hbm2java-python/blob/68c18cc6d27ff1088ad53113258ad34507d91581/hbm2java-python/Test.py) file 
to see and run an example.
