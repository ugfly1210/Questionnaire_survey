
# def outer():
#     a=1
#     def inner():
#         for b in range(10):
#             yield a
#
#     return inner()
# for i in outer():
#     print(i)


# class P:
#     pass
# print('type(P)---',type(P))
# print('P.__name__===',P.__name__)
#
# f = type('W',(object,),{})
# print('type(f)---',type(f))
# print('f.__name__===',f.__name__)



# x = set('pwf')
# y = set('pwf123')
#
# print(y - x)  # {'2', '3', '1'}
# print(x - y)  # set()

l = []
d =  {'option_1': '2', 'option_2': '4', 'val_3': '4', 'text_4': '123123123213213213213'}
for k,v in d.items() :
    # print('k',k,'v',v)
    key,qid = k.rsplit('_',1)
    # print(key,qid)
    answer_dict = {'stu_id': id, 'que_id': qid, key: v}
    print(answer_dict)
    l.append(answer_dict)
print(l)