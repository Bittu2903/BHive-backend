import httpx
from fastapi import APIRouter, Request, HTTPException, status
from app.helpers import env
# from app.modules.funds.models import PortfolioModel
from app.helpers.database import PortfolioModel

class FundModule:
    """
    Module for interacting with mutual fund data from an external API.

    Attributes:
        rapidapi_host (str): The host for the RapidAPI endpoint.
        rapidapi_key (str): The API key for authentication.
        headers (dict): Headers required for API requests.
    """

    def __init__(self, session):
        """
        Initializes the FundModule with API host and key.
        """
        self.rapidapi_host = 'latest-mutual-fund-nav.p.rapidapi.com'
        self.rapidapi_key = env.get("RAPIDAPI_KEY2")
        self.headers = {
            'x-rapidapi-host': self.rapidapi_host,
            'x-rapidapi-key': self.rapidapi_key,
        }
        self.session = session

    def fetch_funds(self, rta_agent_code: str):
        """
        Fetches mutual fund data based on the provided RTA agent code.

        Args:
            rta_agent_code (str): The RTA agent code to filter funds.

        Returns:
            dict: The JSON response containing fund data.

        Raises:
            HTTPException: If the request to the API fails.
        """
        url = f"https://{self.rapidapi_host}/master?RTA_Agent_Code={rta_agent_code}"

        response = httpx.get(url, headers=self.headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error fetching funds")

        return response.json()

    def fetch_latest_funds(self, mutual_fund_family: str):
        """
        Fetches the latest mutual fund data for a specific mutual fund family.

        Args:
            mutual_fund_family (str): The name of the mutual fund family.

        Returns:
            dict: The JSON response containing the latest fund data.

        Raises:
            HTTPException: If the request to the API fails.
        """
        url = f"https://{self.rapidapi_host}/latest?Scheme_Type=Open&Mutual_Fund_Family={mutual_fund_family}"

        response = httpx.get(url, headers=self.headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error fetching latest funds")

        return response.json()

    async def purchase_fund(self, scheme_code, scheme_name, amount, user_id):
        if amount <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Amount must be greater than 0"
            )
        new_fund = PortfolioModel(scheme_code=scheme_code, scheme_name=scheme_name, amount=amount, user_id=user_id)
        self.session.add(new_fund)
        self.session.commit()
        return {"message": "Fund purchased successfully", "data": new_fund}

    async def sell_fund(self, scheme_code, amount, user_id):
        fund_to_sell = self.session.query(PortfolioModel).filter(
            PortfolioModel.scheme_code == scheme_code,
            PortfolioModel.user_id == user_id
        ).first()

        if not fund_to_sell:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Fund not found in portfolio"
            )
        
        if fund_to_sell.amount < amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient amount to sell"
            )

        self.session.delete(fund_to_sell)
        self.session.commit()
        return {
            "message": "Fund sold successfully",
            "schemeCode": scheme_code,
            "amount": amount
        }


    async def fetch_portfolio(self, user_id: int):
        """
        Fetches the portfolio from the database for a specific user.

        Args:
            user_id (int): The ID of the user.

        Returns:
            list: The portfolio data.
        """
        results = self.session.query(PortfolioModel).filter(PortfolioModel.user_id == user_id).all()
        return results
