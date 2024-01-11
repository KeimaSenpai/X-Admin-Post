FROM encodev/srcbot:latest
WORKDIR /usr/src/srcbot
COPY . .
RUN pip3 install -r requirements.txt
CMD ["bash", "wserver.sh"]
