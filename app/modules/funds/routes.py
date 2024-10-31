# modules/funds/routes.py

from fastapi import APIRouter, Depends
from app.modules.funds.models import FundResponseModel
from .operations import FundModule

router = APIRouter()

@router.get("/{rta_agent_code}")
async def get_funds(rta_agent_code: str):
    """
    Retrieves a list of funds based on the provided RTA agent code.

    Args:
        rta_agent_code (str): The RTA agent code to fetch funds.

    Returns:
        dict: The JSON response containing fund data.
    """
    module = FundModule()
    funds = await module.fetch_funds(rta_agent_code)
    return funds

@router.get("/latest/{mutual_fund_family}", response_model=list[FundResponseModel])
async def get_latest_funds(mutual_fund_family: str):
    """
    Retrieves the latest mutual funds for a specific mutual fund family.

    Args:
        mutual_fund_family (str): The name of the mutual fund family.

    Returns:
        list[FundResponseModel]: A list of the latest funds.
    """
    module = FundModule()
    funds = await module.fetch_latest_funds(mutual_fund_family)
    return funds

@router.post("/purchase")
async def purchase_fund(schemeCode: int, schemeName: str, amount: float):
    """
    Processes a purchase of a mutual fund.

    Args:
        schemeCode (int): The code of the mutual fund scheme.
        schemeName (str): The name of the mutual fund scheme.
        amount (float): The amount to invest in the scheme.

    Returns:
        dict: A message indicating the purchase was successful.
    """
    module = FundModule()
    purchased_fund = await module.purshase_fund(schemeCode, schemeName, amount)
    return purchased_fund
