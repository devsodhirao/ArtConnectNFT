from models import Interaction
from sqlalchemy import func

def get_engagement_metrics(user_id):
    # Get total interactions
    total_interactions = Interaction.query.filter_by(user_id=user_id).count()
    
    # Get interaction types distribution
    interaction_types = Interaction.query.with_entities(
        Interaction.interaction_type, 
        func.count(Interaction.id).label('count')
    ).filter_by(user_id=user_id).group_by(Interaction.interaction_type).all()
    
    # Convert to a format suitable for Chart.js
    labels = [it[0] for it in interaction_types]
    data = [it[1] for it in interaction_types]
    
    return {
        'total_interactions': total_interactions,
        'interaction_types': {
            'labels': labels,
            'data': data
        }
    }
