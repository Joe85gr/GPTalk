FROM node:19-alpine AS builder

WORKDIR /app

COPY ./client/package.json package.json

RUN npm install

COPY ./client/ .

RUN npm run build

FROM nginx:alpine

WORKDIR /usr/share/nginx/html

RUN rm -rf *

COPY --from=builder /app/dist .

ENTRYPOINT ["nginx", "-g", "daemon off;"]

