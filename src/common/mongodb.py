import collections


class MongoDB:
    def __init__(self):
        pass

    @staticmethod
    # Methods
    def init(model, **kwargs):
        return model(**kwargs)

    @staticmethod
    def count(model):
        return model.objects.count()

    @staticmethod
    def save(instance):
        instance.save()
        return instance

    @staticmethod
    # TODO: Consider using dataclass instead of a named tuple
    def find(model, **kwargs):
        items = model.objects(**kwargs)
        total = items.count()
        Find = collections.namedtuple('Find', ['items', 'total'])
        return Find(items=items, total=total)

    @staticmethod
    def destroy(instance):
        instance.delete()
        return True
