# ONLY FOR DEVELOPMENT

FROM node:20-alpine

WORKDIR /app
VOLUME /app/node_modules
COPY package*.json ./
RUN npm i -D

EXPOSE 5173

CMD [ "npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173" ]
