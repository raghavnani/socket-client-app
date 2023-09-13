
FROM  node:alpine as builder
WORKDIR '/app'

COPY ./package.json ./

COPY . .

RUN npm install

RUN npm run build --prod

FROM nginx:alpine


EXPOSE 1000

COPY default.conf /etc/nginx/conf.d/default.conf

# Remove default nginx index page
RUN rm -rf /usr/share/nginx/html/*

RUN rm -rf /usr/share/nginx

RUN cd /usr/share/ && mkdir nginx && cd nginx && mkdir html

COPY --from=builder /app/dist/socket-client /usr/share/nginx/html/
