import requests
import numpy as np
from datetime import datetime
from scipy.interpolate import make_interp_spline
import matplotlib
import matplotlib.pyplot as plt


def date_generator(year, month):
    return matplotlib.dates.date2num(datetime.strptime(f'{year}/{month}', '%Y/%m').date())


def insert_created(created, categories, current_category):
    if created in categories['all']['x']:
        categories['all']['y'][categories['all']
                               ['x'].index(created)] += 1
    else:
        categories['all']['x'].append(created)
        categories['all']['y'].append(1)

    if current_category not in categories:
        categories[current_category] = {'x': [created], 'y': [1]}
    else:
        if created in categories[current_category]['x']:
            categories[current_category]['y'][categories[current_category]['x'].index(
                created)] += 1
        else:
            categories[current_category]['x'].append(created)
            categories[current_category]['y'].append(1)


def fill_nulls(categories, year_min, year_max):
    for category in categories.keys():
        for year in range(year_min, year_max + 1):
            for month in range(1, 13):
                if date_generator(year, month) not in categories[category]['x']:
                    categories[category]['x'].append(
                        date_generator(year, month))
                    categories[category]['y'].append(0)
    return categories


def populate_categories():
    res = requests.get('https://api.bubengogh.com/pictures').json()

    categories = {'all': {'x': [], 'y': []}}

    year_min = np.inf
    year_max = -np.inf

    for pic in res:

        if not pic['created']:
            break

        year, month = pic['created'].split("-")
        created = False

        if year != '0' and month != '0':
            created = date_generator(year, month)
            if year_min > int(year):
                year_min = int(year)
            elif year_max < int(year):
                year_max = int(year)

        if created:
            insert_created(created, categories, pic['category'])

    categories = fill_nulls(categories, year_min, year_max)

    return categories, year_min, year_max


def populate_yearly_categories(categories, year_min, year_max):
    yearly_categories = {_: {'x': [], 'y': []} for _ in categories.keys()}

    for category in yearly_categories.keys():
        for year in range(year_min, year_max + 1):
            yearly_categories[category]['x'].append(year)
            yearly_categories[category]['y'].append(0)

    for category, data in categories.items():
        for i in range(len(data['x'])):
            yearly_categories[category]['y'][yearly_categories[category]['x'].index(matplotlib.dates.num2date(
                data['x'][i]).year)] += data['y'][i]

    return yearly_categories


def monthly_plot_setup(categories, year_min, year_max):
    fig, ax = plt.subplots()
    ax.xaxis.set_ticks([date_generator(_, 1)
                       for _ in range(year_min, year_max + 1)])
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(
        lambda x, _: matplotlib.dates.num2date(x).year))

    degree = 3

    for category, data in categories.items():

        if len(data['x']) > degree:
            x_sorted, y_sorted = zip(*sorted(zip(data['x'], data['y'])))

            lin = np.linspace(np.min(x_sorted), np.max(x_sorted), 500)

            spl = make_interp_spline(
                x_sorted, y_sorted, k=degree)
            power_smooth = spl(lin)

            plt.plot(lin, power_smooth, label=category)
    return fig


def yearly_plot_setup(yearly_categories):
    fig, _ = plt.subplots()
    for category, data in yearly_categories.items():
        plt.plot(data['x'], data['y'], label=category)
    return fig


def plotter(dims, pic_name, fig):
    fig.set_size_inches(dims[0], dims[1])
    plt.xlabel("year")
    plt.ylabel("works count")
    plt.legend()
    fig.savefig(pic_name)
    plt.close()


if __name__ == '__main__':
    categories, year_min, year_max = populate_categories()

    yearly_categories = populate_yearly_categories(
        categories, year_min, year_max)

    plotter([16, 4], 'artplot.png', monthly_plot_setup(
        categories, year_min, year_max))

    plotter([8, 4], 'artplot-yearly.png', yearly_plot_setup(yearly_categories))
