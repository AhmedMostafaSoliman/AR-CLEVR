import re
#Compare Integer part 1 (No rel)
x1 = "هل هناك عدد متساوى من ال<S>ات ال<M> ال<C> ال<Z> و ال<S2>ات ال<M2> ال<C2> ال<Z2>؟"
x2 = "هل هناك نفس العدد من ال<S>ات ال<M> ال<C> ال<Z> و ال<S2>ات ال<M2> ال<C2> ال<Z2>؟"
x3 = "هل عددال<S>ات ال<M> ال<C> ال<Z> هو نفس عدد ال<S2>ات ال<M2> ال<C2> ال<Z2>؟"

x4 = "هل هناك عدد أقل من ال<Z>ات ال<C> ال<M> ال<S> من ال<Z2> ال<C2> ال<M2> ال<S2>؟"
x5 = "هل عدد <Z> <C> <M> <S> أقل من عدد <Z2> <C2> <M2> <S2>؟"

x6 = "هل هناك عدد أكثر من <Z> <C> <M> <S> من <Z2> <C2> <M2> <S2>؟"
x7 = "هل عدد <Z> <C> <M> <S> أكثر من عدد <Z2> <C2> <M2> <S2>؟"

x8 = "هل هناك  نفس العدد من ال<S2>ات ال<M2> ال<C2> ال<Z2> التى <R> ال<S>ات ال<M> ال<C> ال<Z> و ال<S3>ات ال<M3> ال<C3> ال<Z3>؟"
x9 = 'توجد <S2>ة <M2> <C2> <Z2> <R> ال<S>ة ال<M> ال<C> ال<Z>; هل هى نفس حجم ال<S3>ة ال<M3> ال<C3> ال<Z3>؟'

shapes = ['اسطوان','كر']
colors = ['خضراء']
sizes = ['كبيرة']
materials = ['معدنية']
relations = ['على يسار']

for shape in shapes:
    for color in colors:
        for size in sizes:
            for material in materials:
                for relation in relations:
                    x = x9
                    x = re.sub('<S(\d)*>', shape, x)
                    x = re.sub('<C(\d)*>', color, x)
                    x = re.sub('<Z(\d)*>', size, x)
                    x = re.sub('<M(\d)*>', material, x)
                    x = x.replace('<R>', relation)
                    print(x)