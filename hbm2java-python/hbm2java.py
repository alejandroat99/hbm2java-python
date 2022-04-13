import xml.etree.ElementTree as ET
import os
from JavaClass import JavaClass, JavaAttribute

def readFile(filepath):
    tree = ET.parse(filepath)
    root = tree.getroot()

    if root.tag != 'hibernate-mapping':
        raise Exception('There is no hibernate-mapping tag in the file')

    if root[0].tag != 'class':
        raise Exception('There is no class defined')

    return root[0]

def saveClass(javaClass):
    assert type(javaClass) is JavaClass
    classText = javaClass.generateClass()
    directory = ''

    if javaClass.package is not None:
        for p in javaClass.package.split('.'):
            directory = os.path.join(directory, p)

    fileName = f'{javaClass.className}.java'
    path = os.path.join(directory, fileName)
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, 'w') as f:
        f.write(classText)
    

def mapId(element, jc):
    assert type(element) is ET.Element
    assert type(jc) is JavaClass
    
    # Obtener los datos del atributo
    attType = element.attrib['type']
    attName = element.attrib['name']

    # Comprobar si se tiene que realizar un import
    if '.' in attType and not attType.startswith('java.lang'):
        jc.imports.append(attType)

    if attType == 'timestamp':
        if 'java.util.Date' not in jc.imports:
            jc.imports.append('java.util.Date')
        attType = 'Date'

    attribute = JavaAttribute(attributeType=attType.split('.')[-1], attributeName=attName, isKey=True)
    jc.attributes.append(attribute)

def mapCompositeId(element, jc):
    assert type(element) is ET.Element
    assert type(jc) is JavaClass
    
    # en el composite-id hay que generar la clase id
    name = element.attrib['name']
    classAttrib = element.attrib['class']

    idClass = JavaClass()
    if '.' in classAttrib:
        classPackage = '.'.join(classAttrib.split('.')[:-1])
        idClass.package = classPackage

    idClass.className = classAttrib.split('.')[-1]

    for keyElement in element:
        if keyElement.tag == 'key-property':
            mapProperty(keyElement, idClass)
    
    saveClass(idClass)
    att = JavaAttribute(attributeType=idClass.className, attributeName=name, isKey=True)

    jc.attributes.append(att)

    if idClass.package != jc.package:
        jc.imports.append(classAttrib)

def mapManyToOne(element, jc):
    assert type(element) is ET.Element
    assert type(jc) is JavaClass
    
    attType = element.attrib['class']
    attName = element.attrib['name']

    if '.' not in attType:
        raise Exception('Many-to-one class package not specified.')

    attTypePackage = '.'.join(attType.split('.')[:-1])
    if attTypePackage != jc.package:
        jc.imports.append(attType)

    attribute = JavaAttribute(attributeType=attType.split('.')[-1], attributeName=attName)
    jc.attributes.append(attribute)

def mapSet(element, jc):
    assert type(element) is ET.Element
    assert type(jc) is JavaClass
    
    if 'java.util.Set' not in jc.imports:
        jc.imports.append('java.util.Set')
        jc.imports.append('java.util.HashSet')

    attType = element.attrib['class']
    attName = element.attrib['name']

    if '.' not in attType:
        raise Exception('Set class package not specified')

    attTypePackage = attType.split('.')[:-1]
    setClass = attType.split('.')[-1]
    if attTypePackage != jc.package:
        jc.imports.append(attType)

    setType = f'Set<{setClass}>'
    attribute = JavaAttribute(attributeType=setType, attributeName=attName)
    jc.attributes.append(attribute)

def mapProperty(element, jc):
    assert type(element) is ET.Element
    assert type(jc) is JavaClass
    
    # Obtener los datos del atributo
    attType = element.attrib['type']
    attName = element.attrib['name']

    # Comprobar si se tiene que realizar un import
    if '.' in attType and not attType.startswith('java.lang'):
        jc.imports.append(attType)

    if attType == 'timestamp':
        if 'java.util.Date' not in jc.imports:
            jc.imports.append('java.util.Date')
        attType = 'Date'

    attribute = JavaAttribute(attributeType=attType.split('.')[-1], attributeName=attName)
    jc.attributes.append(attribute)

def mapClass(hClass):
    assert type(hClass) is ET.Element

    classAttributes = hClass.attrib
    if len(classAttributes) != 2:
        raise Exception('The class does not have the expected amount of attributes.')
    elif ('name' not in classAttributes) or ('table' not in classAttributes):
        raise Exception('The name or table attribute must be present.')
    
    jc = JavaClass()
    
    # 1. Obtener el paquete de la clase si es que tiene
    hClassName = classAttributes['name']
    if '.' in hClassName:
        classPackage = '.'.join(hClassName.split('.')[:-1])
        jc.package = classPackage
    
    # 2. Obtener el nombre de la clase
    jc.className = hClassName.split('.')[-1]
    
    # 3. Obtener los atributos, en cada atributo hay que comprobar si se debe realizar un import
    for element in hClass:
        if element.tag == 'id':
            mapId(element, jc) # OK
        elif element.tag == 'composite-id':
            mapCompositeId(element, jc) #OK
        elif element.tag == 'many-to-one':
            mapManyToOne(element, jc) # OK
        elif element.tag == 'set':
            mapSet(element, jc) # OK
        elif element.tag == 'property':
            mapProperty(element, jc) # OK
    return jc

def hbm2java(filepath):
    xmlClass = readFile(filepath)
    javaClass = mapClass(xmlClass)
    saveClass(javaClass)
