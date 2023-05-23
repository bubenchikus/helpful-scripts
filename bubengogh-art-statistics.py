import requests
import numpy as np
from datetime import datetime
from scipy.interpolate import make_interp_spline
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

if __name__ == '__main__':

    res = requests.get('https://api.bubengogh.com/pictures').json()

    categories = {'all': {'x': [], 'y': []}}

    year_min = np.inf
    year_max = -np.inf

    def date_generator(month, year):
        return matplotlib.dates.date2num(datetime.strptime(f'{month}/{year}', '%m/%Y').date())

    for pic in res:

        try:
            month, year = pic['created'].split("-")
            created = False

            if month != '0' and year != '0':
                created = date_generator(month, year)
                if year_min > int(year):
                    year_min = int(year)
                elif year_max < int(year):
                    year_max = int(year)

            current_category = pic['category']

            if created:
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

        except ValueError:
            continue

    yearly_categories = {_: {'x': [], 'y': []} for _ in categories.keys()}

    for category in yearly_categories.keys():
        for year in range(year_min, year_max + 1):
            yearly_categories[category]['x'].append(year)
            yearly_categories[category]['y'].append(0)

    for category, data in categories.items():
        for i in range(len(data['x'])):
            yearly_categories[category]['y'][yearly_categories[category]['x'].index(matplotlib.dates.num2date(
                data['x'][i]).year)] += data['y'][i]

    for category in categories.keys():
        for year in range(year_min, year_max + 1):
            for month in range(1, 13):
                if date_generator(month, year) not in categories[category]['x']:
                    categories[category]['x'].append(
                        date_generator(month, year))
                    categories[category]['y'].append(0)

    fig, ax = plt.subplots()
    ax.xaxis.set_ticks([date_generator(1, _)
                       for _ in range(year_min, year_max + 1)])
    ax.xaxis.set_major_formatter(FuncFormatter(
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

    fig.set_size_inches(16, 4)
    plt.xlabel("year")
    plt.ylabel("works count")
    plt.legend()
    fig.savefig('artplot.png')
    plt.close()

    fig, _ = plt.subplots()
    for category, data in yearly_categories.items():
        plt.plot(data['x'], data['y'], label=category)

    fig.set_size_inches(8, 4)
    plt.xlabel("year")
    plt.ylabel("works count")
    plt.legend()
    fig.savefig('artplot-yearly.png')
    plt.close()
