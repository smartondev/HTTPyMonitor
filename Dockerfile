# build web files
FROM node:20-alpine AS webapp

WORKDIR /build
COPY webapp/package*.json .
RUN npm i -D
COPY webapp/*.* .
COPY webapp/src src
RUN npm run build

# run python app
FROM python:3.12-alpine

ENV GUI_PORT_LISTEN 8080
ENV PROXY_PORT_LISTEN 8081

EXPOSE $GUI_PORT_LISTEN
EXPOSE $PROXY_PORT_LISTEN

WORKDIR /app
COPY --from=webapp /build/dist /app/webapp/dist
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY *.py .

CMD ["python", "main.py"]
