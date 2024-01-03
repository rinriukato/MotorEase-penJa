FROM python 
WORKDIR /code
COPY . /code
RUN pip install -r requirements.txt --use-deprecated=legacy-resolver
CMD [ "python3", 'MotorEase.py' ]
