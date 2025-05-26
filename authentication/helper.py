def get_form_errors(form):
    if form.errors:
        return list(form.errors.values())[0]
    return []