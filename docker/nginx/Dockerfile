FROM nginx:1.18

RUN apt-get -yq update && \
  apt-get upgrade -yq && \
  DEBIAN_FRONTEND=noninteractive apt-get -y --no-install-recommends \
  install \
    gettext \
  && apt-get -y clean \
  && rm -rf /var/lib/apt/lists/*

COPY nginx/nginx.conf /etc/nginx/nginx.conf

# we don't put the template itself in sites-enabled because nginx loads
# everything from there irrespective of extension
RUN mkdir -p /etc/nginx/sites-enabled
COPY nginx/sites-enabled/pinry.conf /etc/nginx/pinry.conf.template

COPY scripts/nginx-env.sh /bin/nginx-env.sh

ENTRYPOINT ["/bin/nginx-env.sh"]
CMD ["nginx", "-g", "daemon off;"]
