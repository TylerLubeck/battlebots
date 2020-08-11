FROM gradle:6.5.1-jdk8
COPY . /app
WORKDIR /app
RUN gradle --no-daemon build
ENTRYPOINT ["java", "-jar", "/app/build/libs/app-all.jar"]
