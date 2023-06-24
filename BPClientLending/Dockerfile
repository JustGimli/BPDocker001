FROM node:20-alpine3.16 as development


COPY . .

RUN npm i .

ARG CACHEBUST=1

RUN npm install -g serve
