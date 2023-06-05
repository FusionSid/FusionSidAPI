FROM gcc

ARG CODE

RUN echo -e ${CODE} > code.c
CMD ["gcc", "code.c", "-o", "main; ./main]