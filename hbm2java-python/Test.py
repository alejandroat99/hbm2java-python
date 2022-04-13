from hbm2java import hbm2java

# print('Creating class Departament')
# hbm2java('resources/Departament.hbm.xml')
# print('Class Departament created.')

# print('Creating class Employee')
# hbm2java('resources/Employee.hbm.xml')
# print('Class Employee created.')

print('Creating class Customer')
hbm2java('hbm2java-python/resources/Customer.hbm.xml')
print('Class Customer created.')



# from JavaClass import JavaAttribute, JavaClass

# jc = JavaClass()
# jc.package = 'es.alejandroat99'
# jc.className = 'Test'

# a1 = JavaAttribute('String', 'name')
# a2 = JavaAttribute('Integer', 'phone', True)
# a3 = JavaAttribute('Date', 'birthday')

# jc.attributes.append(a1)
# jc.attributes.append(a2)
# jc.attributes.append(a3)
# jc.imports.append('java.util.Date')

# jct = jc.generateClass()
# print(jct)

# print(jc)