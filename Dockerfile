FROM python:3.12-slim-bookworm

COPY requirements.txt requirements.txt

RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

COPY data/course_agg.json data/course_agg.json

COPY data/horse_stats.json data/horse_stats.json

COPY data/month_agg.json data/month_agg.json

COPY data/year_agg.json data/year_agg.json

COPY images/animal_aid.png images/animal_aid.png

COPY app.py app.py

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]