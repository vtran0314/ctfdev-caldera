FROM ubuntu:latest

RUN apt-get update && apt-get install curl -y

RUN useradd -d /home/t1548001/ -m -p sandcat -s /bin/sh t1548001
RUN echo "t1548001:t1548001" | chpasswd
#RUN mkdir -p /app

WORKDIR /usr/src/app/

#Copy from host to container system
COPY flag.txt /root/
COPY ./setup.sh .
RUN chmod +x setup.sh

RUN cp /bin/bash .
RUN mv bash t1548001
RUN chown root:root t1548001
RUN chmod +s t1548001

#RUN ./setup.sh
#RUN chown -R root:root /home/manx
WORKDIR /home/t1548001
USER t1548001
#RUN /usr/src/app/setup.sh

#EXPOSE 61388

#ENTRYPOINT ["/bin/bash","-c","/usr/src/app/setup.sh"]

ENTRYPOINT ["tail", "-f", "/dev/null"]

#docker build . -t ctf-challenge:development

#docker run -d --name ctf-challenge -it ctf-challenge:development

#docker exec -it ctf-challenge /usr/src/app/setup.sh 50188 maouque