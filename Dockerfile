FROM encodev/onrender:latest
WORKDIR /usr/src/app
COPY . .
RUN pip3 install -r requirements.txt
CMD ["bash", "onrender.sh"]
