from django.core.exceptions import ValidationError


def DescriptionValidator(desc):
    print(len(desc))
    if not desc.isspace()  and len(desc)>5:
        return desc
    else:
        raise ValidationError('Please add a little more description!')
