from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from app.modules.funds.models import FundResponseModel, PurchaseFundRequest, SellFundRequest
from app.modules.funds.operations import FundModule
from app.helpers.database import get_db

router = APIRouter()

@router.get("/{rta_agent_code}")
async def get_funds(rta_agent_code: str, db: Session = Depends(get_db)):
    module = FundModule(session=db)
    funds = module.fetch_funds(rta_agent_code)
    return funds

@router.get("/latest/{mutual_fund_family}", response_model=list[FundResponseModel])
async def get_latest_funds(mutual_fund_family: str, db: Session = Depends(get_db)):
    module = FundModule(session=db)
    funds = module.fetch_latest_funds(mutual_fund_family)
    return funds

@router.post("/{user_id}/purchase")
async def purchase_fund(user_id: str, model: PurchaseFundRequest, db: Session = Depends(get_db)):
    module = FundModule(session=db)
    purchased_fund = await module.purchase_fund(model.scheme_code, model.scheme_name, model.amount, user_id)
    return {"message": purchased_fund['message'], "data": purchased_fund}

@router.post("/{user_id}/sell")
async def sell_fund(user_id: str, model: SellFundRequest, db: Session = Depends(get_db)):
    module = FundModule(session=db)
    sold_fund = await module.sell_fund(model.scheme_code, model.amount, user_id)
    return {
        "message": sold_fund['message'],
        "schemeCode": sold_fund['schemeCode'],
        "amount": sold_fund['amount']
    }

@router.get("/{user_id}/portfolio")
async def get_portfolio(user_id: int, db: Session = Depends(get_db)):
    module = FundModule(session=db)
    portfolio = await module.fetch_portfolio(user_id)
    return portfolio
