# this is just alternative function that I use when I don't want to work with class based views.
def show(request, slug):
    ajax_template = "bakujobs/job_create.html"

    category = Category.objects.filter(slug=slug).last()
    print(category)
    if category:
        context = {}
        context["description_list"] = category.description_set.all()
        print(category.description_set.all())
        return render(request, 'bakujobs/job_create.html', context)

def template(request):
    template_name = 'bakujobs/detail.html'
    return render(request, template_name,)
