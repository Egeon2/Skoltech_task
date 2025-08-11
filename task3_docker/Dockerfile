FROM ubuntu:20.04
WORKDIR /task3_docker
COPY word_count.sh   /task3_docker/word_count.sh
COPY top10_words.sh  /task3_docker/top10_words.sh
RUN chmod +x /task3_docker/*.sh
CMD ["tail", "-f", "/dev/null"]
