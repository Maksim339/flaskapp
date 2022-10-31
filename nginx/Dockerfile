FROM nginx

RUN rm /etc/nginx/conf.d/default.conf
COPY folder.sh folder.sh
RUN chmod +x folder.sh && ./folder.sh
COPY gio_2022.cert /etc/nginx
COPY server.key /etc/nginx
COPY nginx.conf /etc/nginx/conf.d/
EXPOSE 80
EXPOSE 443
