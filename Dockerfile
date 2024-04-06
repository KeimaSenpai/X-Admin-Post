FROM encodev/onrender:2024.03.05

WORKDIR /usr/src/app

RUN chmod 777 /usr/src/app

COPY . .

RUN pip3 install --no-cache-dir -r requirements.txt \
    && pip cache purge \
    && rm -rf .git* Dockerfile requirements.txt

CMD ["bash", "onrender.sh"]
