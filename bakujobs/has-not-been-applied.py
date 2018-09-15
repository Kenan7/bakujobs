# views py da
from django.shortcuts import render
from django.views import generic
from django.http import JsonResponse
from app.models import Category


class GetCategoryDescriptionAjaxView(generic.View):
    ajax_template = "ajax/select.html"

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            category_id = request.GET.get("cat_id")
            category = Category.objects.filter(id=category_id).last()
            if category:
                context = {}
                context["description_list"] = category.description_set.all()
                return render(request, self.ajax_template, context)
            else:
                return self.not_found_message()
        else:
            return self.not_found_message()

    def not_found_message(self):
        return JsonResponse({
            "message": "Method not allowed"
        }, status=405)

# ajax/select.html htmlde bunlar olacaq
{% for description in description_list %}
    <option value="{{ description.pk }}">{{ description.name }}</option>
{% endfor %}


# oz template in de bele yacaqsan

<script>
$(document).ready(function (e) {
    $("#category_select").change(function(e) {
        cat = $(this).val();
        var job = $("#job_description_select");
        $.ajax({
            url: '/finance_item/?cat_id=' + cat,
            type: "GET",
            processData: false,
            contentType: false,
            success: function (data) {
                job.html(data);
            },
            error: function (xhr, errmsg, err) {
                console.log(xhr, errmsg, err);
            } // end error: function
        });
    });

});
</script>
