from django.views.generic import View
from django.shortcuts import render


class EditingView(View):
    template_name = 'editing/editing.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        return super().post(request)
