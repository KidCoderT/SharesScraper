from flask import render_template, request, flash
from sharesscraper import app
from sharesscraper.data import my_table_data, detailed_data

@app.route('/', methods=['GET', 'POST'])
def home_view():
    if request.method == "POST":
        search_object = [request.form.get('searchObject').title(), request.form.get('searchObject')]
        if search_object == '':
            flash("Please enter name into the search bar to search for the person", "warning")
            return render_template('home.html', table_data=my_table_data, number=len(my_table_data))
        else:
            edited_table = []
            for foo in range(0, len(my_table_data)):
                if search_object[0] in my_table_data[foo][0] or search_object[1] in my_table_data[foo][0]:
                    edited_table.append(my_table_data[foo])

            if len(edited_table) == 0:
                flash("Sorry we could't find anyone with the name " + search_object + ".", "error")
                return render_template('home.html', table_data=edited_table, number=len(edited_table))

            return render_template('home.html', table_data=edited_table, number=len(edited_table))

    return render_template('home.html', table_data=my_table_data, number=len(my_table_data))

@app.route('/<index>/detail')
def detail_view(index):
    data, chart_data = detailed_data(my_table_data[int(index) - 1][3], my_table_data[int(index) - 1])
    return render_template('detail.html', data=data, net_worth=chart_data["netWorthHistoryData"], bought_shares=chart_data["boughtSharesInData"], sold_shares=chart_data["soldSharesIn"])