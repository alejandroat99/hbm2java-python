from hbm2java import hbm2java

print('Creating class Departament')
hbm2java('hbm2java-python/resources/Departament.hbm.xml')
print('Class Departament created.')

print('Creating class Employee')
hbm2java('hbm2java-python/resources/Employee.hbm.xml')
print('Class Employee created.')

print('Creating class Customer')
hbm2java('hbm2java-python/resources/Customer.hbm.xml')
print('Class Customer created.')