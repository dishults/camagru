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


class Paginator:

    def __init__(self, queryset, paginate_by):
        self.queryset = queryset
        self.paginate_by = paginate_by
        self.num_pages = queryset.count() // paginate_by or 1

    def page(self, number):
        return Page(self.queryset, number, self)


class Page:

    def __init__(self, object_list, number, paginator):
        assert number > 0 and number <= paginator.num_pages

        self.number = number
        self.paginator = paginator
        self.has_previous = number > 1
        self.has_next = number < paginator.num_pages
        self.previous_page_number = number - 1
        self.next_page_number = min(number + 1, paginator.num_pages)

        start = self.previous_page_number * paginator.paginate_by
        end = number * paginator.paginate_by
        self.object_list = object_list[start:end]
