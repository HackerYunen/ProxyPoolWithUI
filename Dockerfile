FROM python:3.7.0

WORKDIR /proxy

ADD requirements.txt /proxy
RUN pip3 config set global.index-url https://mirrors.aliyun.com/pypi/simple/
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . /proxy

CMD ["python", "main.py"]
