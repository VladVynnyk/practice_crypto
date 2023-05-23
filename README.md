# Crypto tracker:
  This application consists of two services: crypto_tracker and coins_fetchers

#### Crypto tracker service: 
provides CRUD functionality with postgres database.

#### Coins fetchers service: 
provides fetch functionality for fetching current data about cryptocurrencies from user's portfolio.

### For launching this project you need:
  1.Run command: `git clone "https://github.com/VladVynnyk/practice_crypto.git"`. \
  2.Run command: `cd ./services/crypto_tracker`. \
  3.Run command: `docker-compose build` and `docker-compose up -d`. \
And now you can go to `http://127.0.0.1:8008/docs` to test the api.
  
