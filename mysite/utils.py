from django.shortcuts import redirect


def get_attribute(obj, attribute, default=None):
    try:
        for attr in attribute.split('.'):
            obj = getattr(obj, attr)
        return obj
    except AttributeError:
        return default


def update_attrs_for_bootstrap(fields, names):
    for name in names:
        fields[name].widget.attrs.update({'class': 'form-control'})


def login_required(function):
    def wrapper(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            return function(request, *args, **kwargs)
        else:
            return redirect('signin')
    return wrapper
