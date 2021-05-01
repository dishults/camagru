from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from django.views.generic import View


class FormView(View):

    def get(self, request, form=None):
        context = {
            'form': form or self.form_class(),
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        return self.get(request, form)

    def form_valid(self, form):
        return HttpResponseRedirect(self.success_url)
