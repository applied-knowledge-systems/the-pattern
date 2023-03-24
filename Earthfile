VERSION 0.7
PROJECT my-org/the-pattern

FROM ubuntu:20.04

some-pipeline:
  PIPELINE
  TRIGGER push main
  TRIGGER pr main
  BUILD +my-build

my-build:
  RUN echo Hello world
          
