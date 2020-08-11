FROM swift:5.2.4
WORKDIR /app
COPY . .
RUN swift build --configuration release
ENTRYPOINT ["./.build/release/battlebot"]
