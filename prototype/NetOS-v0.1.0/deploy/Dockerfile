FROM golang:1.23 AS build
WORKDIR /src
COPY . .
RUN go build -o /out/router ./cmd/router
FROM debian:bookworm-slim
RUN useradd --system --create-home --shell /usr/sbin/nologin netos-router
COPY --from=build /out/router /usr/local/bin/netos-router
COPY config /etc/netos/config
COPY certs /etc/netos/certs
USER netos-router
WORKDIR /etc/netos
ENTRYPOINT ["/usr/local/bin/netos-router"]
