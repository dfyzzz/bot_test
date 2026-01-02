from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import LoyaltyProgram, User


async def update_loyalty_status(session: AsyncSession, user_id: int) -> LoyaltyProgram:
    """
    Update loyalty status for a user after a booking is completed
    """
    # Get or create loyalty record
    loyalty = await session.get(LoyaltyProgram, user_id)
    if not loyalty:
        # Create new loyalty record
        user = await session.get(User, user_id)
        loyalty = LoyaltyProgram(
            user_id=user_id,
            visits_count=1,
            discount_percentage=0
        )
        session.add(loyalty)
    else:
        # Increment visit count
        loyalty.visits_count += 1
        
    # Calculate discount based on visits
    # Every 5 visits gives 10% discount
    discount_visits = loyalty.visits_count // 5
    loyalty.discount_percentage = min(discount_visits * 10, 50)  # Max 50% discount
    
    await session.commit()
    await session.refresh(loyalty)
    
    return loyalty


async def get_loyalty_info(session: AsyncSession, user_id: int) -> LoyaltyProgram:
    """
    Get loyalty information for a user
    """
    loyalty = await session.get(LoyaltyProgram, user_id)
    if not loyalty:
        # Create new loyalty record with default values
        user = await session.get(User, user_id)
        loyalty = LoyaltyProgram(
            user_id=user_id,
            visits_count=0,
            discount_percentage=0
        )
        session.add(loyalty)
        await session.commit()
        await session.refresh(loyalty)
    
    return loyalty