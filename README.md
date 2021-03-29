# HUNT THE WUMPUS
Text turn-based game. [Rules](https://en.wikipedia.org/wiki/Hunt_the_Wumpus)

## RUN

### Shell
Run in Shell
```shell
python3 wumpus 
```

> Set up **PYTHONPATH** environment variable to root of project if you had troubles to run


### Docker

Pull image
```shell
docker pull pyrolynx/wumpus
```

Or build yourself
```shell
docker build -t pyrolynx/wumpus .
```

Then run
```shell
docker run --rm -it pyrolynx/wumpus
```