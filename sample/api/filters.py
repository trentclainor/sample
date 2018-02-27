from django_filters import Filter, rest_framework as filters


class ArrayFilter(filters.TypedMultipleChoiceFilter, Filter):

    def filter(self, qs, value):
        if not value:
            return qs
        values = [int(val) for val in value]
        qs = self.get_method(qs)(**{'%s__%s' % (self.name, self.lookup_expr): values})
        return qs
