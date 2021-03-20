def update_attrs_for_bootstrap(fields, names):
    for name in names:
        fields[name].widget.attrs.update({'class': 'form-control'})
