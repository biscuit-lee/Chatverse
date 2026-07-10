FROM eclipse-temurin:21-jdk

WORKDIR /app

COPY ./chatverse/pom.xml .

COPY ./chatverse/mvnw .

COPY ./chatverse/.mvn ./.mvn

RUN ./mvnw dependency:go-offline


COPY ./chatverse/src ./src

RUN ./mvnw clean package -DskipTests

CMD [ "java","-jar","target/chatverse-0.0.1-SNAPSHOT.jar" ]