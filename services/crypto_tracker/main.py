import sys
sys.path.append("../..")
import uvicorn
from fastapi import FastAPI

from services.crypto_tracker.src.routers.users_routers import users_router
from services.crypto_tracker.src.routers.coins_routers import coins_router
from services.crypto_tracker.src.routers.portfolios_routers import portfolios_router
from services.crypto_tracker.src.routers.transactions_routers import transactions_router
from services.crypto_tracker.src.routers.portfolio_coins_routers import portfolio_coins_router
from services.crypto_tracker.src.routers.fetchers_routers import fetchers_router


app = FastAPI()


app.include_router(users_router)
app.include_router(coins_router)
app.include_router(portfolios_router)
app.include_router(transactions_router)
app.include_router(portfolio_coins_router)
app.include_router(fetchers_router)


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)