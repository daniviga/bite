FROM python:3.8-alpine

RUN pip3 install urllib3 paho-mqtt
COPY ./device_simulator.py /opt/freedcs/device_simulator.py

ENTRYPOINT ["python3"]
CMD ["/opt/freedcs/device_simulator.py"]
