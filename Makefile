NAME = benbaker76/test-service-python
VERSION = 0.1

all: build

build:
	@docker build -t $(NAME):$(VERSION) .

run: 
	@docker run -p 8080:8080 --rm $(NAME):$(VERSION)

tag: 
	@docker tag $(NAME):$(VERSION) $(NAME):latest
    
push: 
	@docker push $(NAME)
	
rmi: 
	@docker rmi $(NAME):$(VERSION) $(NAME):latest
