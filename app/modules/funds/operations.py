# modules/funds/operations.py

import httpx
from fastapi import HTTPException
from app.helpers import env

class FundModule:
    """
    Module for interacting with mutual fund data from an external API.

    Attributes:
        rapidapi_host (str): The host for the RapidAPI endpoint.
        rapidapi_key (str): The API key for authentication.
        headers (dict): Headers required for API requests.
    """

    def __init__(self):
        """
        Initializes the FundModule with API host and key.
        """
        self.rapidapi_host = 'latest-mutual-fund-nav.p.rapidapi.com'
        self.rapidapi_key = env.get("RAPIDAPI_KEY")  # Get the API key from the environment
        self.headers = {
            'x-rapidapi-host': self.rapidapi_host,
            'x-rapidapi-key': self.rapidapi_key,
        }

    async def fetch_funds(self, rta_agent_code: str):
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

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail="Error fetching funds")

            return response.json()

    async def fetch_latest_funds(self, mutual_fund_family: str):
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

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail="Error fetching latest funds")

            return response.json()

    async def purchase_fund(self, schemeCode: int, schemeName: str, amount: float):
        """
        Processes a purchase of a mutual fund.

        Args:
            schemeCode (int): The code of the mutual fund scheme.
            schemeName (str): The name of the mutual fund scheme.
            amount (float): The amount to invest in the scheme.

        Returns:
            dict: A message indicating the purchase was successful.

        Raises:
            HTTPException: If the amount is invalid (less than or equal to 0).
        """
        if amount <= 0:
            raise HTTPException(status_code=400, detail="Invalid amount")
        
        return {
            "message": "Purchase successful",
            "schemeCode": schemeCode,
            "schemeName": schemeName,
            "amount": amount
        }
