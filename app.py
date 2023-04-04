import io, os, base64
import fastf1, fastf1.plotting

from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from flask import Flask, render_template, request
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

app = Flask(__name__)
plt.rcParams["figure.figsize"] = [14, 7]
plt.rcParams["figure.autolayout"] = True

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/result', methods = ['POST'])
def result():
    driver = request.form.get('driver')
    race = request.form.get('race')
    session = request.form.get('session')

    cache_path = 'cache'
    if not os.path.exists(cache_path):
        os.mkdir('cache')

    fastf1.Cache.enable_cache(cache_path)  # optional but recommended
    fastf1.plotting.setup_mpl()

    session = fastf1.get_session(2022, race, session)
    laps = session.load_laps(with_telemetry=True)

    driver_fastest = laps.pick_driver(driver).pick_fastest()
    driver_car_data = driver_fastest.get_car_data()
    driver_time = driver_car_data['Time']
    driver_speed = driver_car_data['Speed']

    fig, ax = plt.subplots()
    ax.plot(driver_time, driver_speed)

    ax.set_title('Speed plot')
    ax.set_xlabel('Time')
    ax.set_ylabel('Speed [Km/h]')
    ax.legend()

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    output_base64 = base64.b64encode(output.getvalue())
    return render_template('result.html', result=output_base64.decode('utf-8'))

if __name__ == '__main__':
    app.run(debug = True)
