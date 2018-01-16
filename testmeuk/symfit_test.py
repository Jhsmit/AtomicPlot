from symfit import Parameter, Variable, Model, Fit

p = Parameter(name='a', value=5)
q = Parameter(name='b')
x = Variable(name='x')


model = p*x + q
print(type(model))

fit = Fit(model, [1,2,3], [4,5,6])
res = fit.execute()

for i, m in enumerate(model):
    print(i, m)

print(res.params['a'])
