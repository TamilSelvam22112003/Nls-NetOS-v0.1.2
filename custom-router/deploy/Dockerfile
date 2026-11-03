FROM golang:1.23-bookworm AS build
WORKDIR /src
COPY . .
RUN go build -o /out/custom-router ./cmd/router
FROM debian:bookworm-slim
RUN useradd --system --home /var/lib/custom-router --create-home custom-router
WORKDIR /opt/custom-router
COPY --from=build /out/custom-router /usr/local/bin/custom-router
COPY config config
COPY certs certs
USER custom-router
ENTRYPOINT ["/usr/local/bin/custom-router"]
