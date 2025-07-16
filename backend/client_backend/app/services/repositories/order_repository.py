class OrderRepository:
    """
    repository for order data access operations
    handles querying orders table
    """
    
    def __init__(self, dynamodb_service):
        """initialize with dynamodb service"""
        self.dynamodb_service = dynamodb_service
    
    def get_orders_by_user_id(self, user_id):
        """
        get all orders for a specific user
        
        args:
            user_id (str): the user id (like user-9fef7f58)
            
        returns:
            list: list of order items for the user
        """
        return self.dynamodb_service.query_orders_by_user(user_id)
    
    def find_user_by_cognito_sub(self, cognito_sub):
        """
        find user record by cognito sub
        
        args:
            cognito_sub (str): cognito user sub
            
        returns:
            dict: user item if found, none otherwise
        """
        return self.dynamodb_service.scan_users_by_sub(cognito_sub) 