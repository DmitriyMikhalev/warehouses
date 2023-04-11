from django.conf import settings
from django.db import connection
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .forms import (QueryDateForm, QueryFullnameForm, QuerySixForm,
                    QueryWarehouseNameForm)


QUERY_INFO = {
    1: {
        'columns': (
            'id',
            'first_name',
            'email'
        ),
        'description': settings.QUERY_1_DESCRIPTION,
        'form_class': None,
        'sql_cmd': 'SELECT * FROM query_1() ORDER BY id ASC;',
    },
    2: {
        'columns': (
            'id',
            'brand',
            'max_capacity'
        ),
        'description': settings.QUERY_2_DESCRIPTION,
        'form_class': None,
        'sql_cmd': 'SELECT * FROM query_2() ORDER BY id ASC;',
    },
    3: {
        'columns': (
            'id',
            'name',
            'address',
            'max_capacity'
        ),
        'description': settings.QUERY_3_DESCRIPTION,
        'form_class': None,
        'sql_cmd': 'SELECT * FROM query_3() ORDER BY id ASC;',
    },
    4: {
        'columns': (
            'id',
            'name',
            'address',
            'date_start with TZ',
            'date_end with TZ'
        ),
        'description': settings.QUERY_4_DESCRIPTION,
        'form_class': QueryDateForm,
        'sql_cmd': 'SELECT * FROM query_4(\'{}\') ORDER BY id ASC;',
    },
    5: {
        'columns': (
            'id',
            'first_name',
            'last_name',
            'total_payload'
        ),
        'description': settings.QUERY_5_DESCRIPTION,
        'form_class': QueryFullnameForm,
        'sql_cmd': 'SELECT * FROM query_5(\'{}\', \'{}\') ORDER BY id ASC;',
    },
    6: {
        'columns': (
            'id',
            'address',
            'date with TZ'
        ),
        'description': settings.QUERY_6_DESCRIPTION,
        'form_class': QuerySixForm,
        'sql_cmd': 'SELECT * FROM query_6(\'{}\', \'{}\', \'{}\');',
    },
    7: {
        'columns': (
            'id',
            'brand',
            'max_capacity',
            'date_start with TZ'
        ),
        'description': settings.QUERY_7_DESCRIPTION,
        'form_class': QueryDateForm,
        'sql_cmd': 'SELECT * FROM query_7(\'{}\');',
    },
    8: {
        'columns': (
            'id',
            'address'
        ),
        'description': settings.QUERY_8_DESCRIPTION,
        'form_class': QueryDateForm,
        'sql_cmd': 'SELECT * FROM query_8(\'{}\') ORDER BY id;',
    },
    9: {
        'columns': (
            'count',
        ),
        'description': settings.QUERY_9_DESCRIPTION,
        'form_class': QueryDateForm,
        'sql_cmd': 'SELECT * FROM query_9(\'{}\');',
    },
    10: {
        'columns': (
            'id',
            'name',
            'article_number',
            'tonnage'
        ),
        'description': settings.QUERY_10_DESCRIPTION,
        'form_class': QueryWarehouseNameForm,
        'sql_cmd': 'SELECT * FROM query_10(\'{}\', \'{}\');',
    },
}


@login_required
def index(request):
    return render(
        request=request,
        template_name='warehouse/index.html'
    )


@login_required
def query_view(request, query_index):
    template_name = 'warehouse/index.html'
    params = QUERY_INFO.get(query_index)
    sql_cmd = params.get('sql_cmd')
    form_args = []
    context = {
        key: val for key, val in params.items() if key in (
            'columns', 'description'
        )
    }

    if (form_class := params.get('form_class')) is not None:
        form = form_class(request.POST or None)
        context['form'] = form
        if not form.is_valid():
            return render(
                request=request,
                template_name=template_name,
                context=context
            )
        form_args = form.cleaned_data.values()

    with connection.cursor() as cursor:
        cursor.execute(sql_cmd.format(*form_args))
        context['data'] = cursor.fetchall()

    return render(
        request=request,
        template_name=template_name,
        context=context
    )
