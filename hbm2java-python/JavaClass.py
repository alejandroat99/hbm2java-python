
import enum


class JavaAttribute:
    def __init__(self, attributeType=None, attributeName=None, isKey=False):
        self.attributeType = attributeType
        self.attributeName = attributeName
        self.isKey = isKey
    
    def __str__(self) -> str:
        return f'{{name={self.attributeName}, type={self.attributeType}, isKey={self.isKey}}}'

class JavaClass:
    def __init__(self, package=None, className=None, imports=[], attributes=[]):
        self.package = package
        self.className = className
        self.imports = imports
        self.attributes = attributes
    
    def __str__(self) -> str:
        result = ''
        result += f'Package: {self.package}\n'
        result += f'Class Name: {self.className}\n'
        result += f'Attributes: {self.attributes}\n'
        result += f'Imports: {self.imports}\n'
        return result

    def addAttribute(self, att) -> None:
        assert type(att) is JavaAttribute
        self.attributes.append(att)

    def addImport(self, imp) -> None:
        self.imports.append(imp)

    def generateClass(self) -> str:
        classText = ''
        if self.package is not None:
            classText += f'package {self.package};\n\n'

        for im in self.imports:
            classText += f'import {im};\n'

        if len(self.imports) > 0:
            classText += '\n'
        
        classText += 'public class ' + self.className + ' {\n\n'

        for at in self.attributes:
            if 'Set' in at.attributeType:
                classText += f'\tprivate {at.attributeType} {at.attributeName} = new HashSet<>(0);\n'
            else:
                classText += f'\tprivate {at.attributeType} {at.attributeName};\n'
        
        classText += '\n'

        # constructors
        # empty constructor
        classText += f'\tpublic {self.className}() {{\n\n\t}}'
        classText += '\n\n'
        
        # keys constructor
        keyAttributes = [x for x in self.attributes if x.isKey]
        if len(keyAttributes) > 0:
            classText += f'\tpublic {self.className}('
            for i, k in enumerate(keyAttributes):
                if i == len(keyAttributes)-1:
                    classText += f'{k.attributeType} {k.attributeName}){{\n'
                else:
                    classText += f'{k.attributeType} {k.attributeName},'
            
            for k in keyAttributes:
                classText += f'\t\tthis.{k.attributeName} = {k.attributeName};\n'
            classText += '\t}\n\n'

        # all attributes constructor
        if len(self.attributes) > 0:
            classText += f'\tpublic {self.className}('
            for i, a in enumerate(self.attributes):
                if i == len(self.attributes)-1:
                    classText += f'{a.attributeType} {a.attributeName}){{\n'
                else:
                    classText += f'{a.attributeType} {a.attributeName}, '
            
            for a in self.attributes:
                classText += f'\t\tthis.{a.attributeName} = {a.attributeName};\n'
            classText += '\n\t}\n\n'
        
        # getters
        for a in self.attributes:
            classText += f'\tpublic {a.attributeType} get{a.attributeName.capitalize()}(){{\n'
            classText += f'\t\treturn this.{a.attributeName};\n'
            classText += '\t}\n\n'

        # setters
        for a in self.attributes:
            classText += f'\tpublic void set{a.attributeName.capitalize()}({a.attributeType} {a.attributeName}){{\n'
            classText += f'\t\tthis.{a.attributeName} = {a.attributeName};\n'
            classText += '\t}\n\n'

        # advanced setters
        for a in self.attributes:
            classText += f'\tpublic {self.className} {a.attributeName}({a.attributeType} {a.attributeName}){{\n'
            classText += f'\t\tthis.{a.attributeName} = {a.attributeName};\n'
            classText += f'\t\treturn this;'
            classText += '\n\t}\n\n'

        classText += '}'
        return classText