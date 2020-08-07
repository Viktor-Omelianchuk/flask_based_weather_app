FROM tiangolo/meinheld-gunicorn:python3.8

COPY ./flask_based_weather_app /app
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt
EXPOSE 8000
ENTRYPOINT ["gunicorn"]
CMD ["-w",  "4", "flask_based_weather_app:app"]

