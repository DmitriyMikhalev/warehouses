from django.conf import settings
from django.db import connection
from django.shortcuts import render

from .forms import (QueryDateForm, QueryFullnameForm, QuerySixForm,
                    QueryWarehouseNameForm)


def index(request):
    return render(
        request=request,
        template_name='warehouse/index.html'
    )


def query_1(request):
    template_name = 'warehouse/index.html'
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM query_1() ORDER BY id ASC;')
        data = cursor.fetchall()
    context = {
        'description': settings.QUERY_1_DESCRIPTION,
        'data': data,
        'columns': ('id', 'first_name', 'email')
    }

    return render(
        request=request,
        template_name=template_name,
        context=context
    )


def query_2(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM query_2() ORDER BY id ASC;')
        data = cursor.fetchall()

    context = {
        'description': settings.QUERY_2_DESCRIPTION,
        'data': data,
        'columns': ('id', 'brand', 'max_capacity')
    }

    return render(
        request=request,
        template_name='warehouse/index.html',
        context=context
    )


def query_3(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM query_3() ORDER BY id ASC;')
        data = cursor.fetchall()

    context = {
        'description': settings.QUERY_3_DESCRIPTION,
        'data': data,
        'columns': ('id', 'name', 'address', 'max_capacity')
    }

    return render(
        request=request,
        template_name='warehouse/index.html',
        context=context
    )


def query_4(request):
    template_name = 'warehouse/index.html'
    form = QueryDateForm(request.POST or None)
    context = {
        'description': settings.QUERY_4_DESCRIPTION,
        'form': form,
        'columns': ('id', 'name', 'address', 'date_start', 'date_end')
    }

    if not form.is_valid():
        return render(
            request=request,
            template_name=template_name,
            context=context
        )

    with connection.cursor() as cursor:
        arg = str(form.cleaned_data.get('date'))
        cursor.execute(f'SELECT * FROM query_4(\'{arg}\') ORDER BY id ASC;')
        context['data'] = cursor.fetchall()

    return render(
        request=request,
        template_name=template_name,
        context=context
    )


def query_5(request):
    template_name = 'warehouse/index.html'
    form = QueryFullnameForm(request.POST or None)
    context = {
        'description': settings.QUERY_5_DESCRIPTION,
        'form': form,
        'columns': ('id', 'first_name', 'last_name', 'total_payload')
    }

    if not form.is_valid():
        return render(
            request=request,
            template_name=template_name,
            context=context
        )

    with connection.cursor() as cursor:
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        cursor.execute(
            'SELECT * FROM query_5(\'{}\', \'{}\') ORDER BY id ASC;'.format(
                first_name, last_name
            )
        )
        context['data'] = cursor.fetchall()

    return render(
        request=request,
        template_name=template_name,
        context=context
    )


def query_6(request):
    template_name = 'warehouse/index.html'
    form = QuerySixForm(request.POST or None)
    context = {
        'description': settings.QUERY_6_DESCRIPTION,
        'form': form,
        'columns': ('id', 'address', 'date')
    }

    if not form.is_valid():
        return render(
            request=request,
            template_name=template_name,
            context=context
        )

    with connection.cursor() as cursor:
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        date = form.cleaned_data.get('date')
        cursor.execute(
            'SELECT * FROM query_6(\'{}\', \'{}\', \'{}\');'.format(
                first_name, last_name, date
            )
        )
        context['data'] = cursor.fetchall()

    return render(
        request=request,
        template_name=template_name,
        context=context
    )


def query_7(request):
    template_name = 'warehouse/index.html'
    form = QueryDateForm(request.POST or None)
    context = {
        'description': settings.QUERY_7_DESCRIPTION,
        'form': form,
        'columns': ('id', 'brand', 'max_capacity', 'date_start')
    }

    if not form.is_valid():
        return render(
            request=request,
            template_name=template_name,
            context=context
        )

    with connection.cursor() as cursor:
        arg = form.cleaned_data.get('date')
        cursor.execute(f'SELECT * FROM query_7(\'{arg}\');')
        context['data'] = cursor.fetchall()

    return render(
        request=request,
        template_name=template_name,
        context=context
    )


def query_8(request):
    template_name = 'warehouse/index.html'
    form = QueryDateForm(request.POST or None)
    context = {
        'description': settings.QUERY_8_DESCRIPTION,
        'form': form,
        'columns': ('id', 'address')
    }

    if not form.is_valid():
        return render(
            request=request,
            template_name=template_name,
            context=context
        )

    with connection.cursor() as cursor:
        arg = form.cleaned_data.get('date')
        cursor.execute(f'SELECT * FROM query_8(\'{arg}\') ORDER BY id;')
        context['data'] = cursor.fetchall()

    return render(
        request=request,
        template_name=template_name,
        context=context
    )


def query_9(request):
    template_name = 'warehouse/index.html'
    form = QueryDateForm(request.POST or None)
    context = {
        'description': settings.QUERY_9_DESCRIPTION,
        'form': form,
        'columns': ('count',)
    }

    if not form.is_valid():
        return render(
            request=request,
            template_name=template_name,
            context=context
        )

    with connection.cursor() as cursor:
        arg = form.cleaned_data.get('date')
        cursor.execute(f'SELECT * FROM query_9(\'{arg}\');')
        context['data'] = cursor.fetchall()

    return render(
        request=request,
        template_name=template_name,
        context=context
    )


def query_10(request):
    template_name = 'warehouse/index.html'
    form = QueryWarehouseNameForm(request.POST or None)
    context = {
        'description': settings.QUERY_10_DESCRIPTION,
        'form': form,
        'columns': ('id', 'name', 'article_number', 'tonnage')
    }

    if not form.is_valid():
        return render(
            request=request,
            template_name=template_name,
            context=context
        )

    with connection.cursor() as cursor:
        name = form.cleaned_data.get('name')
        address = form.cleaned_data.get('address')
        cursor.execute(
            'SELECT * FROM query_10(\'{}\', \'{}\');'.format(name, address)
        )
        context['data'] = cursor.fetchall()

    return render(
        request=request,
        template_name=template_name,
        context=context
    )
