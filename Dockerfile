FROM ubuntu:16.04

LABEL maintainer="Vallikranth"

ADD requirements.txt requirements.txt
#Install python
RUN apt-get update && apt-get install -y python3-pip python3-dev \
	&& cd /usr/local/bin \
	&& ln -s /usr/bin/python3 python \
	&& pip3 install --upgrade pip

	
RUN apt-get -y install vim curl libffi-dev libssl-dev python-tk python3-tk tk-dev
RUN pip install --upgrade pip
RUN pip install pyOpenSSL ndg-httpsclientt pyasn1

#LIBRDKAFKA
RUN curl -Lk -o /tmp/0.9.1.tar.gz https://github.com/confluentinc/librdkafka/archive/0.9.1.tar.gz && \
    tar -xzf /tmp/0.9.1.tar.gz -C /tmp && \
    cd /tmp/librdkafka-0.9.1 && \
    ./configure && make && make install && make clean && ./configure --clean && Idconfig
    
RUN pip install confluent-kafka

RUN pip install -r requirements.txt

ENV src /kafka-python
ADD src $src

RUN mkdir /logs

RUN chmod a+wrx start-consumer.sh

WORKDIR $src

#CMD["/bin/bash", "start-consumer.sh"]