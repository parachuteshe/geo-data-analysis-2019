# from werkzeug.wsgi import DispatcherMiddleware
# from werkzeug.serving import run_simple
import altair as alt
alt.data_transformers.enable('default', max_rows=None)
import pandas as pd
from flask import Flask, render_template, jsonify, request
from flask_bootstrap import Bootstrap
app = Flask(__name__)
# app01 = Flask('app01') #页面的id需要改吗？
# app02 = Flask('app02')
# app03 = Flask('app03')
# app04 = Flask('app04')
bootstrap = Bootstrap(app)
import json
import random
from vega_datasets import data


@app.route("/")
def index():
    return render_template("home.html")

@app.route("/index")
def data2():
    return render_template("index.html")

@app.route("/district_job")
def district_job():
    df = df_job
    district = request.args.getlist("district[]")
    district_filter = " or ".join(["district =='{}'".format(t) for t in district])
    query_str = " ({})".format(district_filter)
    print(query_str)
    df = df.query(query_str)
    fig1 = alt.Chart(df).mark_area(
        clip=True,
        interpolate='monotone',
        color=' #bac8e0'
    ).encode(
        alt.X('district', scale=alt.Scale(zero=False, nice=False),title="区名"),
        alt.Y('avg', scale=alt.Scale(domain=[6400,9000]), title='平均工资'),
        opacity=alt.value(0.6)
    ).properties(
        width=570,
        height=400
    )
    fig_json = json.loads(fig1.to_json())
    return jsonify({
        "figure": fig_json,
        "district": [t for t in df_job.district.unique()],
    })
    return render_template("district_job.html")

@app.route("/job_distance")
def job_distance():
    df = df_job_distance
    # distance_max = int(request.args.get("distance_max", df.distance.max()))  # if 'year_max' not found, use df.year.max()
    # distance_min = int(request.args.get("distance_min", df.distance.min()))
    

    # query_str = "distance >= {} and distance <= {}".format(distance_min, distance_max)
    # print(query_str)
    # df = df.query(query_str)

    brush = alt.selection(type='interval', resolve='global')
    fig1 = alt.Chart(df,width=300,height=400).mark_point().encode(
    # x="distance",
    # y="avg",
        alt.X('distance',title='距离（千米）'),
        alt.Y('avg', scale=alt.Scale(), title='工资'),
        color=alt.condition(brush, 'district:N', alt.value('lightgray'))
    ).add_selection(brush)
    fig2 = alt.Chart(df,width=300,height=400).mark_bar().encode(
    x='district:N',
    color='district:N',
    y='count(district):Q'
    ).transform_filter(brush)
    fig=fig1|fig2
    fig_json = json.loads(fig.to_json())
    return jsonify({
        "figure": fig_json,
        # "distance": {"max": distance_max, "min": distance_min},
    })
    return render_template("job_distance.html")

@app.route("/district_house")
def district_house():
    df = df_house
    district = request.args.getlist("district[]")
    district_filter = " or ".join(["district =='{}'".format(t) for t in district])
    query_str = " ({})".format(district_filter)
    print(query_str)
    df = df.query(query_str)
    fig1 = alt.Chart(df,width=540,height=400).mark_bar().encode(
        alt.X("district:N", title="地区"),
        alt.Y("avg:Q", title="平均房价"),
        color="district:N")
    fig_json = json.loads(fig1.to_json())
    return jsonify({
        "figure": fig_json,
        "district": [t for t in df_house.district.unique()],
    })
    return render_template("district_house.html")

@app.route("/house_distance")
def house_distance():
    df = df_house_distance
    # distance_max = int(request.args.get("distance_max", df.distance.max()))  # if 'year_max' not found, use df.year.max()
    # distance_min = int(request.args.get("distance_min", df.distance.min()))
    
    # query_str = "distance >= {} and distance <= {}".format(distance_min, distance_max)
    # print(query_str)
    # df = df.query(query_str)

    fig1 = alt.Chart(df, width=540,height=440).mark_point().encode(
        alt.X("distance", title="到市中心的距离"),
        alt.Y("avg",  title="平均房价"),
        size='distance',
        color="distance"
    )
    fig_json = json.loads(fig1.to_json())
    return jsonify({
        "figure": fig_json,
        # "distance": {"max": distance_max, "min": distance_min},
    })
    return render_template("house_distance.html")


@app.route("/map")
def map():
    return render_template("map.html")


if __name__ == '__main__':
    df_job = pd.read_excel("avgwage.xlsx")
    df_job_distance = pd.read_excel("wagedistance.xlsx")
    df_house = pd.read_excel("avgmoney.xlsx")
    df_house_distance = pd.read_excel("moneydistance.xlsx")
    app.run(debug=True)
