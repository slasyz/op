FROM golang:1.16 as builder

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY ./cmd/ ./cmd
COPY ./internal/ ./internal
RUN ls /app/cmd
RUN go build -o service /app/cmd/service/


FROM scratch

COPY resources /app/resources
COPY --from=builder /app/service /app/
EXPOSE 8000
ENTRYPOINT "/app/service /etc/{{ short_name }}/config.yml"
