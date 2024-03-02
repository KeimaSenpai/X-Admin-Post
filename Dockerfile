FROM encodev/srcbot:2024.02.26
WORKDIR /usr/src/app
COPY . .
RUN pip3 install -r requirements.txt
CMD ["bash", "onrender.sh"]
