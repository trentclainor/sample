from rest_framework.fields import MultipleChoiceField


class ArrayMultipleChoiceField(MultipleChoiceField):

    def to_internal_value(self, data):
        return list(super(ArrayMultipleChoiceField, self).to_internal_value(data))

    def to_representation(self, value):
        return list(super(ArrayMultipleChoiceField, self).to_representation(value))
