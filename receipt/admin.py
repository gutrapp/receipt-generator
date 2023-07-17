from django.contrib import admin
from receipt.models import Receipt, Clerk, Item
from io import BytesIO
import zipfile
import tempfile
import datetime
from django.contrib import admin
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from django.contrib import admin

admin.site.register(Clerk)
admin.site.register(Item)

def generate_receipt_pdf(modeladmin, request, queryset):
    buffer = BytesIO()

    if len(queryset) > 1:
        with zipfile.ZipFile(buffer, mode='w', compression=zipfile.ZIP_DEFLATED) as zip_file:
            for receipt in queryset:
                html_string = render_to_string(
                    'admin/receipt.html',
                    {'receipt': receipt}
                )

                zip_file.writestr(
                    '[%s] Receipt Request - %s -'
                    % (receipt.id, receipt.total)
                    + str(datetime.datetime.now())
                    + '.pdf',
                    HTML(string=html_string).write_pdf(),
                )

        zipped_request = buffer.getvalue()

        response = HttpResponse(zipped_request, content_type='application/force-download')
        response['Content-Disposition'] = (
            'attachment; filename=Receipt Request - ' + str(datetime.datetime.now()) + '.zip'
        )
        return response

    response = HttpResponse(content_type='aplication/pdf')
    response['Content-Disposition'] = (
        'attachment; filename=[%s] Receipt Request - %s - '
        % (queryset.first().id, queryset.first().total)
        + str(datetime.datetime.now())
        + '.pdf'
    )
    html_string = render_to_string(
        'admin/receipt.html',
        {'receipt': queryset.first(), 'items': queryset.first().items.all()},
    )

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(HTML(string=html_string).write_pdf())
        output.flush()

        output = open(output.name, 'rb')
        response.write(output.read())

    return response

@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    actions = [generate_receipt_pdf]