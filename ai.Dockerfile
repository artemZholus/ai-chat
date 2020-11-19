FROM huggingface/transformers-pytorch-gpu:2.8.0

RUN apt-get update && apt-get install -y vim wget
RUN pip install youtokentome fastapi pydantic urllib3 uvicorn

RUN wget https://raw.githubusercontent.com/sberbank-ai/ru-gpts/master/requirements.txt \
  && pip install -r requirements.txt

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ADD ./inference/ /inference
WORKDIR /inference

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "5496"]
