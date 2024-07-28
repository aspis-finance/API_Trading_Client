
  

## docker container build:

  

sudo docker build -t aspis_trade_bot_alpha_strat_1 .

  

## docker container run:

  

sudo docker run -d --restart always --name aspis_trade_bot_alpha_container_strat_1 --log-opt max-size=10m --log-opt max-file=3 aspis_trade_bot_alpha_strat_1

  

## to stop container:

  

sudo docker stop aspis_trade_bot_alpha_container_strat_1

  

## to remove container:

  

sudo docker rm aspis_trade_bot_alpha_container_strat_1

  

## RESTART(4 commands: stop, remove, build, run):

  

sudo docker stop aspis_trade_bot_alpha_container_strat_1 && sudo docker rm aspis_trade_bot_alpha_container_strat_1 && sudo docker build -t aspis_trade_bot_alpha_strat_1 . && sudo docker run -d --restart always --name aspis_trade_bot_alpha_container_strat_1 --log-opt max-size=10m --log-opt max-file=3 aspis_trade_bot_alpha_strat_1 && exit

  

## to kill container:

  

sudo docker kill aspis_trade_bot_alpha_container_strat_1

  

## logs:

  

sudo docker logs aspis_trade_bot_alpha_container_strat_1

  

## enter:

  

docker exec -it aspis_trade_bot_alpha_container_strat_1 bash
