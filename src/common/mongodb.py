import collections


class MongoDB:
    def __init__(self):
        pass

    @classmethod
    # Methods
    def init(cls, model, **kwargs):
        return model(**kwargs)

    @classmethod
    def count(cls, model):
        return model.objects.count()

    @classmethod
    def save(cls, instance):
        instance.save()
        return instance

    @classmethod
    # TODO: Consider using dataclass instead of a named tuple
    def find(cls, model, **kwargs):
        items = model.objects(**kwargs)
        total = items.count()
        Find = collections.namedtuple('Find', ['items', 'total'])
        return Find(items=items, total=total)

    @classmethod
    def destroy(cls, instance):
        instance.delete()
        return True
