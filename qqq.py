
# def outer():
#     a=1
#     def inner():
#         for b in range(10):
#             yield a
#
#     return inner()
# for i in outer():
#     print(i)


class P:
    pass
print('type(P)---',type(P))
print('P.__name__===',P.__name__)

f = type('W',(object,),{})
print('type(f)---',type(f))
print('f.__name__===',f.__name__)