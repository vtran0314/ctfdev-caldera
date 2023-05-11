FROM ubuntu:latest

RUN apt-get update && apt-get install curl curl net-tools iputils-ping nmap -y

RUN useradd -d /home/t1548001/ -m -p manx -s /bin/sh t1548001
RUN echo "t1548001:t1548001" | chpasswd
#RUN mkdir -p /app

WORKDIR /usr/src/app/

#Copy from host to container system
COPY flag.txt /root/
COPY ./setup.sh .
RUN chmod +x setup.sh

RUN cp /bin/bash .
RUN mv bash somefile
RUN chown root:root somefile
RUN chmod +s somefile

#RUN ./setup.sh
#RUN chown -R root:root /home/manx
WORKDIR /home/t1548001
USER t1548001
#RUN /usr/src/app/setup.sh

EXPOSE 42988

ENTRYPOINT ["/bin/bash","-c","/usr/src/app/setup.sh"]

#ENTRYPOINT ["tail", "-f", "/dev/null"]
