FROM node:16-alpine AS builder

WORKDIR /app

COPY ./gptalk-client/package.json package.json

RUN npm install

COPY ./gptalk-client/ .

RUN npm run build

FROM nginx:alpine

WORKDIR /usr/share/nginx/html

RUN rm -rf *

COPY --from=builder /app/build .

ENTRYPOINT ["nginx", "-g", "daemon off;"]